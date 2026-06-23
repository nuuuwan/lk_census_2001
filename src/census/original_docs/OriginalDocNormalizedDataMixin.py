import os
from functools import cached_property

from utils import JSONFile, Log

log = Log("OriginalDocNormalizedDataMixin")


class OriginalDocNormalizedDataMixin:

    @cached_property
    def normalized_data_path(self):
        return os.path.join(self.dir_data, "normalized_data.json")

    def normalize_row(self, row):

        region_id = row["region_id"]
        if not region_id.startswith("LK"):
            return None

        if region_id == "LK":
            region_id = "LK-from-source"

        values_from_values = {}
        pct_values_from_pct_values = {}
        total_from_source = None
        for k, v in row["values"].items():
            if k in ["region_id", "region_name"]:
                continue
            elif "-pct" in k:
                pct_values_from_pct_values[k] = v / 100.0
            elif "total" in k:
                total_from_source = v
            else:
                values_from_values[k] = v

        if values_from_values:
            total = sum(values_from_values.values())
            values = values_from_values
        elif pct_values_from_pct_values and total_from_source:
            values = {
                k.replace("-pct", ""): int(round(v * total_from_source, 0))
                for k, v in pct_values_from_pct_values.items()
            }
            total = total_from_source
        else:
            log.warning(
                f"Could not normalize row for {region_id}: {row['values']}"
            )
            return None

        if total != total_from_source:
            log.warning(
                f"Total mismatch for {region_id}:"
                + f" {total} != {total_from_source}"
            )

        pct_values = {k: round(v / total, 4) for k, v in values.items()}

        return dict(
            region_id=row["region_id"],
            region_name=row["region_name"],
            values=values,
            total=total,
            total_from_source=total_from_source,
            pct_values=pct_values,
        )

    def build_normalized_by_region(self, data_list):
        normalized_data_list = [self.normalize_row(row) for row in data_list]
        normalized_data_list = [
            row for row in normalized_data_list if row is not None
        ]
        normalized_data_file = JSONFile(self.normalized_data_path)
        normalized_data_file.write(normalized_data_list)
        log.debug(
            f"Wrote {len(normalized_data_list)} rows to {normalized_data_file}"
        )
        return normalized_data_list

    def build_normalized(self, force=True):
        normalized_data_file = JSONFile(self.normalized_data_path)
        if normalized_data_file.exists and not force:
            log.debug(f"{normalized_data_file} exists")
            return self.get_normalized_data_list()

        data_list = self.get_data_list()
        if not data_list:
            log.warning(f"No data list found for {self.doc_id}")
            return None

        if "region_id" in data_list[0]:
            return self.build_normalized_by_region(data_list)

        log.warning(
            f"Data list does not contain 'region_id' for {self.doc_id}"
        )
        return None

    def get_normalized_data_list(self):
        normalized_data_file = JSONFile(self.normalized_data_path)
        if not normalized_data_file.exists:
            return None
        return normalized_data_file.read()
