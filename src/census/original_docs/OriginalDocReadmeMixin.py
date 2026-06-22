import json
import os
import random

from utils_future import File, JSONFile, Log, Time, TimeFormat

log = Log("OriginalDocReadmeMixin")


class OriginalDocReadmeMixin:
    GLOBAL_README_PATH = "README.md"

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

    def build_readme(self):
        lines = (
            [f"# {self.name}", ""]
            + self.lines_for_data_types()
            + self.lines_for_example()
        )
        readme_file = File(self.readme_file_path())
        readme_file.write("\n".join(lines))
        log.info(f"Wrote {readme_file}")

    @classmethod
    def build_global_readme(cls):
        docs = cls.list()
        time_str = TimeFormat.TIME.format(Time.now())
        time_str = time_str.replace(" ", "_").replace("-", "--")
        n_datasets = len(docs)
        lines = [
            "# Sri Lanka 🇱🇰  - Census of Population and Housing 2001",
            "",
            "![CPH](https://img.shields.io/badge/CPH-2001-blue)",
            f"![LastUpdated](https://img.shields.io/badge/last_updated-{time_str}-green)",
            "",
            f"**{n_datasets}** Datasets on"
            + " Population and Housing by Country and District.",
            "",
        ]

        for i_doc, doc in enumerate(docs, start=1):
            lines.append(f"{i_doc:02d}. [{doc.name}]({doc.dir_data})")

        lines.append("")

        readme_file = File(cls.GLOBAL_README_PATH)
        readme_file.write("\n".join(lines))
        log.info(f"Wrote {readme_file}")
