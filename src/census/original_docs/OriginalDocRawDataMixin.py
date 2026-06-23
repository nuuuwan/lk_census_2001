import os
from functools import cached_property

import camelot

from utils_future import JSONFile, Log

log = Log("OriginalDocRawDataMixin")

DIR_DATA = "data"


class OriginalDocRawDataMixin:
    @cached_property
    def dir_data(self):
        dir_data = os.path.join(DIR_DATA, f"{self.doc_id}")
        os.makedirs(dir_data, exist_ok=True)
        return dir_data

    @cached_property
    def raw_data_file_path(self):
        return os.path.join(self.dir_data, "raw_data.json")

    def clean_empty_cols(self, data_list):
        n_rows = len(data_list)
        n_cols = len(data_list[0])

        cols_to_n_non_null_cells = {}
        for i_row in range(n_rows):
            for i_col in range(n_cols):
                cell = str(data_list[i_row][i_col]).strip()
                if cell != "":
                    cols_to_n_non_null_cells[i_col] = (
                        cols_to_n_non_null_cells.get(i_col, 0) + 1
                    )
        null_cols = [
            i_col
            for i_col in range(n_cols)
            if cols_to_n_non_null_cells.get(i_col, 0) < n_rows / 2
        ]

        for i_row in range(n_rows):
            for i_col in reversed(null_cols):
                del data_list[i_row][i_col]

        return data_list

    def is_seperated_row(self, row):
        cleaned_rows = [str(cell).strip() for cell in row]
        non_empty_cells = sum(1 for cell in cleaned_rows if cell)
        if cleaned_rows[0] != "" and non_empty_cells == 1:
            return True
        return False

    def clean_seperated_rows(self, data_list):
        n_rows = len(data_list)

        for i_row in range(n_rows):
            if self.is_seperated_row(data_list[i_row]):
                data_list[i_row + 1][0] = (
                    str(data_list[i_row][0]).strip()
                    + " "
                    + str(data_list[i_row + 1][0]).strip()
                )
        data_list = [
            data for data in data_list if not self.is_seperated_row(data)
        ]
        return data_list

    def clean_raw_data_list(self, data_list):
        data_list = self.clean_empty_cols(data_list)
        data_list = self.clean_seperated_rows(data_list)
        return data_list

    def build_raw_data(self, force=True) -> list:
        json_file = JSONFile(self.raw_data_file_path)
        if json_file.exists and not force:
            log.debug(f"{json_file} exists")
            return json_file.read()

        pdf_path = self.download_pdf()
        tables = camelot.read_pdf(pdf_path, pages="all", flavor="stream")
        if not tables:
            log.warning(f"No tables found in {pdf_path}")
            json_file.write([])
            return []

        df = max(tables, key=lambda t: len(t.df)).df
        data_list = df.values.tolist()
        data_list = self.clean_raw_data_list(data_list)
        if len(data_list) < 10:
            raise ValueError(f"Not enough rows in raw data: {len(data_list)}")

        json_file.write(data_list)
        log.debug(f"Wrote {len(data_list)} rows -> {json_file}")
        return data_list
