import os
import re
from functools import cached_property

from census.original_docs.OriginalDocDataConstanstsMixin import \
    OriginalDocDataConstanstsMixin
from census.original_docs.RegionUtils import RegionUtils
from utils_future import File, JSONFile, Log

log = Log("OriginalDocDataMixin")


class OriginalDocDataMixin(OriginalDocDataConstanstsMixin):

    @cached_property
    def data_file_path(self):
        return os.path.join(self.dir_data, "data.json")

    def split_raw_header_and_raw_data_rows(self, raw_rows):
        for i_row, row in enumerate(raw_rows):
            if (
                "sri lanka" in str(row[0]).lower()
                or "total" in str(row[0]).lower()
            ):
                return raw_rows[:i_row], raw_rows[i_row:]
        raise ValueError("Could not find header/data split in raw rows")

    def clean_header_item(self, item):
        item = str(item).strip()
        if not item:
            return None
        item = item.lower()
        item = "".join(c for c in item if c.isalnum() or c.isspace())
        item = re.sub(r"\s+", " ", item)
        item = item.replace(" ", "-")
        return item

    def build_headers(self, header_rows):
        n_rows = len(header_rows)
        n_cols = len(header_rows[0])
        headers = []
        for i_cols in range(n_cols):
            items = [
                self.clean_header_item(header_rows[i_row][i_cols])
                for i_row in range(n_rows)
            ]
            items = [item for item in items if item]
            header = "-".join(items)

            headers.append(header)

        if len(headers) > 0:
            headers[0] = "district"
        return headers

    def parse_float(self, value):
        value = str(value).strip()
        if value in ["-", ""]:
            return 0
        value = value.replace(",", "")
        try:
            return float(value)
        except ValueError:
            log.warning(f"Could not parse float from {value}")
            return None

    def parse_raw_data_row(self, data, headers) -> dict:
        values = {}
        region_id, region_name = None, None
        for i_header, header in enumerate(headers):
            if header == "district":
                region_id, region_name = RegionUtils.parse(data[i_header])
                continue

            value = data[i_header]
            values[header] = self.parse_float(value)

        if len(headers) != len(values.keys()) + 1:
            raise ValueError(
                f"Header/data length mismatch: {len(headers)} headers vs "
                + f"{len(values.keys())} values"
            )

        if region_id:
            data = dict(
                region_id=region_id,
                region_name=region_name,
                values=values,
            )
            return data

        return None

    def parse_raw_data_by_district(self):
        raw_rows = JSONFile(self.raw_data_file_path).read()
        raw_header_rows, raw_data_rows = (
            self.split_raw_header_and_raw_data_rows(raw_rows)
        )

        headers = self.get_custom_headers() or self.build_headers(
            raw_header_rows
        )
        log.debug(f"{headers=}")

        if len(headers) == 0:
            log.warning(f"No header rows found in raw data for {self.doc_id}")
            return

        data_list = []
        for raw_data_row in raw_data_rows:
            data = self.parse_raw_data_row(raw_data_row, headers)
            if data:
                data_list.append(data)

        if len(data_list) == 0:
            log.warning(f"No data rows parsed for {self.doc_id}")
            return

        data_file = JSONFile(self.data_file_path)
        data_file.write(data_list)
        log.debug(f"Wrote {len(data_list)} rows to {data_file}")

    def is_by_district(self):
        raw_data_content = File(self.raw_data_file_path).read().lower()
        return (
            "colombo" in raw_data_content
            and "gampaha" in raw_data_content
            and "kalutara" in raw_data_content
        )

    def build_data(self, force=True):
        data_file = JSONFile(self.data_file_path)
        if data_file.exists and not force:
            log.debug(f"{data_file} exists")
            return data_file.read()

        if self.is_by_district():
            return self.parse_raw_data_by_district()
        log.warning(f"Unknown doc_id format for parsing: {self.doc_id}")
