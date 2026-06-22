import json
import os
import random

from utils_future import File, JSONFile, Log

log = Log("OriginalDocReadmeMixin")


class OriginalDocReadmeMixin:
    def readme_file_path(self) -> list[str]:
        return os.path.join(self.dir_data, "README.md")

    def lines_for_data_types(self) -> list[str]:
        lines = ["## File Formats", ""]
        for label, file_name in [
            ("📄 JSON Data", self.data_file_path),
            ("📄 Raw JSON Data from Original", self.raw_data_file_path),
            ("📜 Original PDF", self.pdf_file_path),
        ]:
            lines.extend(
                [
                    f"- [{label}](../../{file_name})",
                ]
            )
        lines.append("")
        return lines

    def lines_for_example(self) -> list[str]:
        random.seed(0)
        data_file = JSONFile(self.data_file_path)
        if data_file.exists:
            data_list = data_file.read()
            random.shuffle(data_list)
            data = data_list[0]
            json_output = json.dumps(data, indent=4)
            return [
                "## Example JSON Row",
                "",
                "```json",
                json_output,
                "```",
                "",
            ]
        return []

    def readme_build(self):
        lines = (
            [f"# {self.name}", ""]
            + self.lines_for_data_types()
            + self.lines_for_example()
        )
        readme_file = File(self.readme_file_path())
        readme_file.write("\n".join(lines))
        log.info(f"Wrote {readme_file}")
