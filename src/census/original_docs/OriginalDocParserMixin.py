import os
from functools import cached_property

import camelot

from utils_future import JSONFile, Log

log = Log("OriginalDocParserMixin")

DIR_DATA = "data"
_MIN_NUMERICS_DATA_ROW = (
    2  # a row is a data row if it has >= this many numeric cells
)
_TITLE_CELL_CHARS = 45  # single-cell rows longer than this are page titles


class OriginalDocParserMixin:
    @cached_property
    def dir_data(self):
        dir_data = os.path.join(DIR_DATA, f"{self.doc_id}")
        os.makedirs(dir_data, exist_ok=True)
        return dir_data

    def json_file_path(self):
        return os.path.join(self.dir_data, "data.json")

    # ------------------------------------------------------------------
    # row classification helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_numeric(s: str) -> bool:
        s = s.strip().replace(",", "")
        if not s or s == "-":
            return False
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def _non_empty(row: list) -> list:
        return [str(v).strip() for v in row if str(v).strip()]

    @staticmethod
    def _numeric_count(row: list) -> int:
        return sum(
            1 for v in row if OriginalDocParserMixin._is_numeric(str(v))
        )

    @staticmethod
    def _is_data_row(row: list) -> bool:
        return (
            OriginalDocParserMixin._numeric_count(row)
            >= _MIN_NUMERICS_DATA_ROW
        )

    @staticmethod
    def _is_title_row(row: list) -> bool:
        """Page title/subtitle: single non-empty cell that is very long."""
        ne = OriginalDocParserMixin._non_empty(row)
        return len(ne) == 1 and len(ne[0]) > _TITLE_CELL_CHARS

    @staticmethod
    def _is_group_label_row(row: list) -> bool:
        """Group label: exactly one non-empty non-numeric cell, no numeric values."""
        ne = OriginalDocParserMixin._non_empty(row)
        return (
            len(ne) == 1
            and not OriginalDocParserMixin._is_numeric(ne[0])
            and not OriginalDocParserMixin._is_data_row(row)
        )

    # ------------------------------------------------------------------
    # column-header construction
    # ------------------------------------------------------------------

    @staticmethod
    def _build_column_headers(header_rows: list) -> list:
        """
        Combine multi-row headers column-by-column.
        Cell values longer than _TITLE_CELL_CHARS are skipped (they are page
        titles that bled into a header row alongside real column labels).
        Duplicate names are disambiguated by appending _2, _3, ...
        """
        if not header_rows:
            return []
        n_cols = max(len(r) for r in header_rows)
        raw = []
        for c in range(n_cols):
            parts = []
            for row in header_rows:
                val = str(row[c]).strip() if c < len(row) else ""
                if val and val not in parts and len(val) <= _TITLE_CELL_CHARS:
                    parts.append(val)
            raw.append(" ".join(parts))

        seen: dict = {}
        headers = []
        for h in raw:
            if h not in seen:
                seen[h] = 1
                headers.append(h)
            else:
                seen[h] += 1
                headers.append(f"{h}_{seen[h]}")
        return headers

    # ------------------------------------------------------------------
    # header / body split
    # ------------------------------------------------------------------

    @classmethod
    def _split_rows(cls, all_rows: list) -> tuple:
        """
        Return (header_rows, body_rows).

        Strategy (two-pass):
          1. Find the first row that has >= _MIN_NUMERICS_DATA_ROW numeric cells.
          2. If that row's col 0 is non-empty the label is self-contained, so
             everything before it (minus page titles) is a header row.
          3. If col 0 is empty the label comes from a preceding group-label row.
             Scan backward for the last single-cell row before the data row;
             that row and everything after it go into the body.
        """
        first_data_idx = next(
            (i for i, r in enumerate(all_rows) if cls._is_data_row(r)), None
        )
        if first_data_idx is None:
            return [], []

        pre = all_rows[:first_data_idx]
        first_col_populated = bool(all_rows[first_data_idx][0])

        if first_col_populated:
            header_rows = [r for r in pre if not cls._is_title_row(r)]
            body_rows = all_rows[first_data_idx:]
        else:
            # Find the last group-label row in the pre-data section
            last_group_in_pre = next(
                (
                    i
                    for i in range(len(pre) - 1, -1, -1)
                    if cls._is_group_label_row(pre[i])
                ),
                None,
            )
            if last_group_in_pre is not None:
                header_rows = [
                    r
                    for r in pre[:last_group_in_pre]
                    if not cls._is_title_row(r)
                ]
                body_rows = all_rows[last_group_in_pre:]
            else:
                header_rows = [r for r in pre if not cls._is_title_row(r)]
                body_rows = all_rows[first_data_idx:]

        return header_rows, body_rows

    # ------------------------------------------------------------------
    # public API
    # ------------------------------------------------------------------

    def parse_pdf(self) -> list:
        json_file = JSONFile(self.json_file_path())
        if json_file.exists:
            log.debug(f"{json_file} exists")
            return json_file.read()

        pdf_path = self.download_pdf()
        tables = camelot.read_pdf(pdf_path, pages="all", flavor="stream")
        if not tables:
            log.warning(f"No tables found in {pdf_path}")
            json_file.write([])
            return []

        df = max(tables, key=lambda t: len(t.df)).df
        all_rows = [[str(v).strip() for v in row] for _, row in df.iterrows()]

        header_rows, body_rows = self._split_rows(all_rows)
        col_headers = self._build_column_headers(header_rows)
        label_key = (
            col_headers[0] if col_headers and col_headers[0] else "row_label"
        )
        log.debug(f"Columns: {col_headers}  label_key={label_key!r}")

        # --- build output rows ------------------------------------------
        rows = []
        current_group = ""
        for values in body_rows:
            if self._is_group_label_row(values):
                current_group = self._non_empty(values)[0]
                continue
            if not self._is_data_row(values):
                continue

            label_parts = [current_group] if current_group else []
            row_dict: dict = {}
            for header, val in zip(col_headers, values):
                if not val:
                    continue
                if self._is_numeric(val):
                    if header:
                        row_dict[header] = val
                else:
                    label_parts.append(val)

            row_dict[label_key] = " ".join(label_parts).strip()
            rows.append(row_dict)

        json_file.write(rows)
        log.info(f"Wrote {len(rows)} rows -> {json_file}")
        return rows
