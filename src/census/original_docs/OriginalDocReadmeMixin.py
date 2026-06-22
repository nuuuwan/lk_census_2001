import os

from utils_future import File, Log

log = Log("OriginalDocReadmeMixin")


class OriginalDocReadmeMixin:
    def readme_file_path(self) -> str:
        return os.path.join(self.dir_data, "README.md")

    def readme_build(self):
        lines = [f"# {self.name}"]
        readme_file = File(self.readme_file_path())
        readme_file.write("\n".join(lines))
        log.info(f"Wrote {readme_file}")
