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

    def clean_raw_data(self, data):
        non_empty_rows = [item for item in data if str(item).strip()]
        return non_empty_rows

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
        data_list = [self.clean_raw_data(data) for data in data_list]
        json_file.write(data_list)
        log.debug(f"Wrote {len(data_list)} rows -> {json_file}")
        return data_list
