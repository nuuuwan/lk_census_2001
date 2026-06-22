import os

from utils_future import JSONFile, Log

log = Log("OriginalDocMetadataMixin")


class OriginalDocMetadataMixin:
    METADATA_FILE_PATH = os.path.join("data", "metadata.json")

    @classmethod
    def write_metadata(cls, original_docs):
        os.makedirs(cls.DIR_ORIGINAL_DATA, exist_ok=True)
        metadata = [doc.__dict__ for doc in original_docs]
        metadata_file = JSONFile(cls.METADATA_FILE_PATH)
        metadata_file.write(metadata)
        log.info(f"Wrote {len(original_docs)} docs to {metadata_file}")

    @classmethod
    def read_metadata(cls):
        metadata_file = JSONFile(cls.METADATA_FILE_PATH)
        if not metadata_file.exists:
            log.warning(f"Metadata file {metadata_file} does not exist")
            return []
        metadata = metadata_file.read()
        return metadata
