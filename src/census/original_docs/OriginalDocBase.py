import os
from dataclasses import dataclass
from functools import cache, cached_property

from utils_future import JSONFile


@dataclass
class OriginalDocBase:
    name: str
    url: str

    def __str__(self) -> str:
        return f"📄 OriginalDoc({self.name, self.url})"

    @classmethod
    def get_long_doc_id_from_name(cls, name: str) -> str:
        long_doc_id = "".join(c for c in name if c.isalnum() or c.isspace())
        long_doc_id = long_doc_id.strip().replace(" ", "-").lower()
        return long_doc_id

    @cached_property
    def long_doc_id(self) -> str:
        return self.get_long_doc_id_from_name(self.name)

    @classmethod
    @cache
    def get_long_doc_id_to_doc_id(cls):
        return JSONFile(
            os.path.join(
                "src", "census", "original_docs", "LONG_DOC_ID_TO_DOC_ID.json"
            )
        ).read()

    @cached_property
    def long_doc_id_to_doc_id(self):
        return self.get_long_doc_id_to_doc_id()

    @classmethod
    def get_doc_id_from_name(cls, name: str) -> str:
        long_doc_id = cls.get_long_doc_id_from_name(name)
        long_doc_id_to_doc_id = cls.get_long_doc_id_to_doc_id()
        return long_doc_id_to_doc_id.get(long_doc_id, None)

    @cached_property
    def doc_id(self) -> str:
        return self.get_doc_id_from_name(self.name)

    @cached_property
    def short_name(self) -> str:
        return self.doc_id.replace("-", " ").title()
