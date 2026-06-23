import os
from functools import cached_property

from utils_future import JSONFile


class OriginalDocDataConstanstsMixin:
    CUSTOM_HEADER_MAP_PATH = os.path.join(
        "src", "census", "original_docs", "CUSTOM_HEADER_MAP.json"
    )

    @cached_property
    def custom_header_map(self):
        custom_header_map_file = JSONFile(self.CUSTOM_HEADER_MAP_PATH)
        custom_header_map = custom_header_map_file.read()
        custom_header_map = dict(
            sorted(custom_header_map.items(), key=lambda x: x[0])
        )
        custom_header_map_file.write(custom_header_map)
        return custom_header_map_file.read()

    def get_custom_headers(self):
        custom_header = self.custom_header_map.get(self.doc_id, None)
        if custom_header is None:
            raise ValueError(
                f"Custom header not found for doc_id: {self.doc_id}"
            )
        if sorted(list(set(custom_header))) != sorted(custom_header):
            raise ValueError(
                f"Custom header for doc_id: {
                    self.doc_id} contains duplicate values"
            )

        return custom_header
