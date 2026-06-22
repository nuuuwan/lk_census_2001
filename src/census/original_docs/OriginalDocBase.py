from dataclasses import dataclass
from functools import cached_property


@dataclass
class OriginalDocBase:
    name: str
    url: str

    def __str__(self) -> str:
        return f"📄 OriginalDoc({self.name, self.url})"

    @cached_property
    def doc_id(self) -> str:
        doc_id = "".join(c for c in self.name if c.isalnum() or c.isspace())
        doc_id = doc_id.strip().replace(" ", "-").lower()
        return doc_id
