from dataclasses import dataclass


@dataclass
class OriginalDocBase:
    name: str
    url: str

    def __str__(self) -> str:
        return f"📄 OriginalDoc({self.name, self.url})"
