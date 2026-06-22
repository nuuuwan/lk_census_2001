import os
from dataclasses import dataclass
from functools import cached_property

from utils_future import JSONFile


@dataclass
class OriginalDocBase:
    name: str
    url: str

    def __str__(self) -> str:
        return f"📄 OriginalDoc({self.name, self.url})"

    @cached_property
    def long_doc_id(self) -> str:
        doc_id = "".join(c for c in self.name if c.isalnum() or c.isspace())
        doc_id = doc_id.strip().replace(" ", "-").lower()
        return doc_id

    @cached_property
    def short_name_map(self):
        return JSONFile(
            os.path.join(
                "src", "census", "original_docs", "SHORT_NAME_MAP.json"
            )
        ).read()

    @cached_property
    def doc_id(self) -> str:
        short_name_map = self.short_name_map
        if self.long_doc_id not in short_name_map:
            raise ValueError(f"Missing short name for {self.long_doc_id}")
        return short_name_map[self.long_doc_id]

    @cached_property
    def short_name(self) -> str:
        return self.doc_id.replace("-", " ").title()
