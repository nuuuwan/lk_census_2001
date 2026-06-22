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
        for label, file_path in [
            ("📄 JSON Data", self.data_file_path),
            ("📄 TSV Data", self.tsv_file_path),
            ("📄 Raw JSON Data from Original", self.raw_data_file_path),
            ("📜 Original PDF", self.pdf_file_path),
        ]:
            if os.path.exists(file_path):
                lines.extend(
                    [
                        f"- [{label}](../../{file_path})",
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

    def lines_for_source(self) -> list[str]:
        return [
            "## Source",
            "",
            f"- *[{self.url}]({self.url})*",
            "",
        ]

    @staticmethod
    def lines_for_header() -> list[str]:
        time_str = TimeFormat.DATE.format(Time.now())
        time_str = time_str.replace(" ", "_").replace("-", "--")
        return [
            "![CPH](https://img.shields.io/badge/CPH-2001-blue)",
            f"![LastUpdated](https://img.shields.io/badge/last_updated-{time_str}-green)",
            "",
        ]

    @staticmethod
    def lines_for_footer() -> list[str]:
        return [
            "![Maintainer]"
            + "(https://img.shields.io/badge/maintainer-nuuuwan-red)",
            "![MadeWith](https://img.shields.io/badge/made_with-python-blue)",
            "[![License: MIT]"
            + "(https://img.shields.io/badge/License-MIT-yellow.svg)]"
            + "(https://opensource.org/licenses/MIT)",
            "",
        ]

    def build_readme(self):
        lines = (
            [f"# {self.name}", ""]
            + self.lines_for_header()
            + self.lines_for_data_types()
            + self.lines_for_example()
            + self.lines_for_source()
            + self.lines_for_footer()
        )
        readme_file = File(self.readme_file_path())
        readme_file.write("\n".join(lines))
        log.info(f"Wrote {readme_file}")

    @classmethod
    def build_global_readme(cls):
        docs = cls.list()

        n_datasets = len(docs)
        lines = (
            [
                "# Sri Lanka 🇱🇰  - Census of Population and Housing 2001",
                "",
            ]
            + cls.lines_for_header()
            + [
                f"**{n_datasets}** Datasets on"
                + " Population and Housing by Country and District.",
                "",
            ]
        )

        for i_doc, doc in enumerate(docs, start=1):
            lines.append(f"{i_doc:02d}. [{doc.short_name}]({doc.dir_data})")

        url = (
            "https://www.statistics.gov.lk"
            + "/Population/StaticalInformation/CPH2001"
        )
        lines.append("")
        lines.append(f"*[{url}]({url})*")
        lines.append("")
        lines.extend(cls.lines_for_footer())

        readme_file = File(cls.GLOBAL_README_PATH)
        readme_file.write("\n".join(lines))
        log.info(f"Wrote {readme_file}")
