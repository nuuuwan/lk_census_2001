#!/usr/bin/env python3
"""
Build the root README.md from the template in data/README.md.

Changes applied:
- Output goes to the repo root README.md
- CSV filenames in headings become links: [name.csv](data/name.csv)
- Source PDF filenames become links: [name.pdf](original_data/name.pdf)
- Relative path ../original_data/README.md -> original_data/README.md
- Full data tables embedded under each section (regenerated from the CSVs)
"""

import glob
import re
from pathlib import Path

import pandas as pd

WORK_DIR = Path("/Users/nuwansenaratna/Not-Dropbox/_CODING/py/lk_census_2001")
TEMPLATE = WORK_DIR / "data" / "README.md"
OUTPUT = WORK_DIR / "README.md"
DATA_DIR = WORK_DIR / "data"
ORIG_DIR = WORK_DIR / "original_data"

# Map bare PDF stem (from **Source:** lines) to actual filename on disk.
_PDF_CACHE: dict[str, str] = {}


def _build_pdf_cache():
    for p in ORIG_DIR.glob("*.pdf"):
        _PDF_CACHE[p.name] = p.name


def pdf_link(name: str) -> str:
    """Return a markdown link for a PDF filename, or a backtick-quoted name."""
    if name in _PDF_CACHE:
        return f"[{name}](original_data/{name})"
    return f"`{name}`"


def df_to_md(df: pd.DataFrame) -> str:
    """Convert a DataFrame to a GitHub-flavoured markdown table string."""
    cols = list(df.columns)
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join(["---"] * len(cols)) + " |"
    rows = []
    for _, row in df.iterrows():
        cells = []
        for v in row:
            if pd.isna(v):
                cells.append("")
            else:
                cells.append(str(v))
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep] + rows)


def process_chunk(chunk: str) -> str:
    """Apply all per-section transformations to a text chunk."""

    # 1. Fix relative path to original_data README
    chunk = chunk.replace(
        "../original_data/README.md", "original_data/README.md"
    )

    # 2. Link CSV filenames in headings:  ### `name.csv`  →  ### [name.csv](data/name.csv)
    def csv_heading_link(m):
        name = m.group(1)
        return f"### [{name}](data/{name})"

    chunk = re.sub(r"###\s+`([^`]+\.csv)`", csv_heading_link, chunk)

    # 3. Link PDF filenames in **Source:** lines:
    #    **Source:** `name.pdf`  →  **Source:** [name.pdf](original_data/name.pdf)
    def source_link(m):
        name = m.group(1)
        return f"**Source:** {pdf_link(name)}"

    chunk = re.sub(r"\*\*Source:\*\*\s+`([^`]+\.pdf)`", source_link, chunk)

    # 4. Embed data table: remove any existing #### Data block, then re-add
    chunk = re.sub(r"\n#### Data\n[\s\S]*$", "", chunk)

    csv_m = re.search(r"###\s+\[([^]]+\.csv)\]", chunk)
    if csv_m:
        csv_name = csv_m.group(1)
        csv_path = DATA_DIR / csv_name
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            md_table = df_to_md(df)
            chunk = chunk.rstrip("\n") + "\n\n#### Data\n\n" + md_table + "\n"

    return chunk


def main():
    _build_pdf_cache()

    text = TEMPLATE.read_text()

    # Fix top-level heading
    text = re.sub(
        r"^# Data Directory.*",
        "# Sri Lanka Census of Population and Housing 2001",
        text,
        count=1,
    )

    # Split on section separators and process each chunk
    sections = re.split(r"(\n---\n)", text)
    output_parts = [process_chunk(s) for s in sections]

    OUTPUT.write_text("".join(output_parts))
    print(f"Written: {OUTPUT}")


if __name__ == "__main__":
    main()
