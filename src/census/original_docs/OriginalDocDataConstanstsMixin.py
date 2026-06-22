import os
from functools import cached_property

from utils_future import JSONFile


class OriginalDocDataConstanstsMixin:
    CUSTOM_HEADER_MAP_PATH = os.path.join(
        "src", "census", "original_docs", "CUSTOM_HEADER_MAP.json"
    )

    @cached_property
    def custom_header_map(self):
        return JSONFile(self.CUSTOM_HEADER_MAP_PATH).read()

    def get_custom_headers(self):
        return self.custom_header_map.get(self.doc_id, None)
