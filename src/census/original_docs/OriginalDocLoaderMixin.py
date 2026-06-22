import os
from functools import cached_property

from utils_future import JSONFile, Log

log = Log("OriginalDocLoaderMixin")


class OriginalDocLoaderMixin:

    @cached_property
    def metadata_file_path(self):
        return os.path.join(self.dir_data, "metadata.json")

    def write_metadata(self):
        metadata_file = JSONFile(self.metadata_file_path)
        metadata_file.write(
            dict(
                name=self.name,
                url=self.url,
            )
        )
        log.info(f"Wrote {metadata_file}")

    @classmethod
    def list(cls):
        docs = []
        for data_dir_name in os.listdir("data"):
            data_dir = os.path.join("data", data_dir_name)
            if not os.path.isdir(data_dir):
                continue
            metadata_file = JSONFile(os.path.join(data_dir, "metadata.json"))
            if not metadata_file.exists:
                raise ValueError(f"Missing metadata.json in {data_dir}")

            metadata = metadata_file.read()
            doc = cls(name=metadata["name"], url=metadata["url"])
            docs.append(doc)
        log.debug(f"Loaded {len(docs)} docs")
        return docs
