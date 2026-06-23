import os
from functools import cached_property

from utils_future import JSONFile, Log, TSVFile

log = Log("OriginalDocTSVMixin")


class OriginalDocTSVMixin:
    @cached_property
    def tsv_file_path(self):
        return os.path.join(self.dir_data, "data.tsv")

    def to_tsv_data(self, data: dict) -> dict:
        return (
            dict(
                region_id=data["region_id"],
                region_name=data["region_name"],
            )
            | data["values"]
        )

    def build_tsv(self):
        data_file = JSONFile(self.data_file_path)
        if data_file.exists:
            data_list = data_file.read()
            tsv_data_list = [self.to_tsv_data(data) for data in data_list]
            tsv_file = TSVFile(self.tsv_file_path)
            tsv_file.write(tsv_data_list)
            log.debug(f"Wrote {tsv_file}")
