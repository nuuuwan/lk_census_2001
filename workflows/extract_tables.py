#!/usr/bin/env python3
"""
Extract district-level data tables from Sri Lanka Census 2001 PDFs.
Saves extracted tables as CSVs in the data/ directory.
"""

import glob
import os
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd
import pdfplumber

WORK_DIR = Path("/Users/nuwansenaratna/Not-Dropbox/_CODING/py/lk_census_2001")
ORIG_DIR = WORK_DIR / "original_data"
DATA_DIR = WORK_DIR / "data"

# District names, longest first to avoid partial matches
DISTRICTS = [
    "Nuwara Eliya",
    "Anuradhapura",
    "Polonnaruwa",
    "Kilinochchi",
    "Mullaitivu",
    "Hambantota",
    "Trincomalee",
    "Batticaloa",
    "Moneragala",
    "Ratnapura",
    "Kurunegala",
    "Colombo",
    "Gampaha",
    "Kalutara",
    "Kandy",
    "Matale",
    "Galle",
    "Matara",
    "Jaffna",
    "Mannar",
    "Vavuniya",
    "Ampara",
    "Puttalam",
    "Badulla",
    "Kegalle",
    "Sri Lanka",
]
# "Total" is a standalone row key (Total - 18 Districts, Total (18 districts), etc.)
AREA_PAT = re.compile(
    r"^(" + "|".join(re.escape(d) for d in DISTRICTS) + r"|Total)"
    r"(?:\([a-z]+\))?"  # optional footnote marker like (a)
    r"(?:\s*[-–]\s*\d+\s*(?:Districts?)?)?"  # "- 18 Districts"
    r"(?:\s*\(\d+\s*districts?\))?"  # "(18 districts)"
    r"\s*",
    re.IGNORECASE,
)


# ── helpers ──────────────────────────────────────────────────────────────────


def cluster_rows(words, y_tol=5):
    """Cluster a list of word dicts into row groups by y-coordinate."""
    rows = defaultdict(list)
    for w in words:
        y = round(w["top"])
        assigned = False
        for ry in rows:
            if abs(ry - y) <= y_tol:
                rows[ry].append(w)
                assigned = True
                break
        if not assigned:
            rows[y].append(w)
    return {
        y: sorted(ws, key=lambda w: w["x0"]) for y, ws in sorted(rows.items())
    }


def get_text_lines(pdf_path):
    """Return all stripped text lines from all pages of a PDF."""
    lines = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            t = page.extract_text(x_tolerance=3)
            if t:
                for ln in t.split("\n"):
                    lines.append(ln.strip())
    return lines


def is_data_line(line):
    """True if line starts with a known area name and contains at least one digit."""
    return bool(AREA_PAT.match(line)) and bool(re.search(r"\d", line))


def parse_data_line(line):
    """
    Parse a line that starts with a district/total name.
    Returns (area_label, [values]) where values are strings (no commas).
    """
    m = AREA_PAT.match(line)
    if not m:
        return None
    label = m.group(0).strip().rstrip("-–").strip()
    label = re.sub(
        r"\s*\(\d+\s*districts?\)", "", label, flags=re.IGNORECASE
    ).strip()
    rest = line[m.end() :]
    nums = re.findall(r"-?[\d,]+\.?\d*", rest)
    values = [n.replace(",", "") for n in nums]
    return label, values


# ── column-name detection ────────────────────────────────────────────────────


def detect_col_centers(data_rows_words, left_boundary):
    """
    Identify numeric column x-centers from data rows.
    data_rows_words: list of word-lists (one per row).
    left_boundary: x0 threshold beyond which words are column values.
    """
    xs = []
    for row in data_rows_words:
        for w in row:
            if w["x0"] <= left_boundary:
                continue
            txt = w["text"].replace(",", "").lstrip("-")
            if re.fullmatch(r"\d+\.?\d*", txt):
                cx = (w["x0"] + w["x1"]) / 2
                xs.append(cx)
    if not xs:
        return []
    xs.sort()
    clusters = [[xs[0]]]
    for x in xs[1:]:
        if x - clusters[-1][-1] <= 18:
            clusters[-1].append(x)
        else:
            clusters.append([x])
    return [sum(c) / len(c) for c in clusters]


def build_col_names(header_rows_words, col_centers, left_boundary, tol=35):
    """
    For each column center collect nearby header words, grouped by row.
    Uses only the last 2 rows (closest to data) per column, joined top-to-bottom.
    """
    # bucket: {col_idx: {y: [words]}}
    buckets = defaultdict(lambda: defaultdict(list))
    for row in header_rows_words:
        if not row:
            continue
        y = round(row[0]["top"])
        for w in row:
            cx = (w["x0"] + w["x1"]) / 2
            if cx <= left_boundary:
                continue
            if col_centers:
                dists = [abs(cx - cc) for cc in col_centers]
                idx = dists.index(min(dists))
                if dists[idx] <= tol:
                    buckets[idx][y].append(w["text"])
    names = []
    for i in range(len(col_centers)):
        col_rows = buckets.get(i, {})
        if not col_rows:
            names.append(f"col_{i+1}")
            continue
        # Use last 2 rows only, joined top-to-bottom
        sorted_ys = sorted(col_rows.keys())[-2:]
        words = []
        for y in sorted_ys:
            words.extend(col_rows[y])
        name = " ".join(words).strip()
        name = re.sub(r"\s+", " ", name).strip("()./")
        names.append(name if name else f"col_{i+1}")
    return names
    return names


def dedupe_names(names):
    """Make column names unique by appending _2, _3, etc."""
    seen = {}
    result = []
    for n in names:
        if n not in seen:
            seen[n] = 0
            result.append(n)
        else:
            seen[n] += 1
            result.append(f"{n}_{seen[n]+1}")
    return result


def get_col_names_from_pdf(pdf_path, first_data_line_idx, all_text_lines):
    """
    Use word-coordinate approach on the first page to extract column names.
    Only uses the header rows that are closest to the data (within 80px) to
    avoid picking up title/subtitle words that span the full page width.
    Returns list of column names (excluding the district column).
    """
    with pdfplumber.open(str(pdf_path)) as pdf:
        page = pdf.pages[0]
        words = page.extract_words(x_tolerance=3, y_tolerance=3)

    row_clusters = cluster_rows(words)
    page_width = page.width

    # Estimate left boundary from leftmost words
    all_x0 = [w["x0"] for w in words if w["x0"] < 300]
    left_margin = min(all_x0) if all_x0 else 50
    left_boundary = left_margin + 110  # district names ~110px wide

    all_ys = sorted(row_clusters.keys())
    first_data_y = None
    for y in all_ys:
        row_text = " ".join(w["text"] for w in row_clusters[y])
        if is_data_line(row_text):
            first_data_y = y
            break

    if first_data_y is None:
        return []

    data_rows_words = [row_clusters[y] for y in all_ys if y >= first_data_y][
        :10
    ]
    col_centers = detect_col_centers(data_rows_words, left_boundary)
    if not col_centers:
        return []

    # Only use header rows within 80px of first data row (the real sub-headers)
    # AND exclude rows whose words span > 70% of the page width (title rows)
    close_header_rows = []
    for y in all_ys:
        if y >= first_data_y:
            break
        if (first_data_y - y) > 80:
            continue
        row = row_clusters[y]
        if not row:
            continue
        row_span = row[-1]["x1"] - row[0]["x0"]
        if row_span > 0.70 * page_width:
            continue  # skip wide title rows
        close_header_rows.append(row)

    raw_names = build_col_names(
        close_header_rows, col_centers, left_boundary, tol=35
    )
    return dedupe_names(raw_names)


# ── simple table extractor ───────────────────────────────────────────────────


def extract_simple(pdf_path, csv_stem=None):
    """
    Extract a standard 1-row-per-district table.
    Returns a pandas DataFrame or None.
    """
    lines = get_text_lines(pdf_path)

    data = []
    for ln in lines:
        if is_data_line(ln):
            parsed = parse_data_line(ln)
            if parsed:
                label, values = parsed
                data.append([label] + values)

    if not data:
        return None

    # Normalise row lengths (pad short rows)
    max_len = max(len(r) for r in data)
    data = [r + [None] * (max_len - len(r)) for r in data]

    n_val_cols = max_len - 1

    # Use manual override if available, else auto-detect
    if csv_stem and csv_stem in COLUMN_OVERRIDES:
        override = COLUMN_OVERRIDES[csv_stem]
        val_cols = (
            override + [f"col_{i+1}" for i in range(len(override), n_val_cols)]
        )[:n_val_cols]
    else:
        first_data_idx = next(
            i for i, ln in enumerate(lines) if is_data_line(ln)
        )
        col_names = get_col_names_from_pdf(pdf_path, first_data_idx, lines)
        if len(col_names) >= n_val_cols:
            val_cols = col_names[:n_val_cols]
        else:
            val_cols = col_names + [
                f"col_{i+1}" for i in range(len(col_names), n_val_cols)
            ]

    cols = ["district"] + val_cols
    df = pd.DataFrame(data, columns=cols)
    df = df.replace("-", pd.NA)
    return df


# ── p11d1 special extractor ──────────────────────────────────────────────────
# Structure: district name alone on a row, then sub-rows:
#   Both sexes <values>
#   Male       <values>
#   Female     <values>

SEX_SUBROW_PAT = re.compile(r"^(Both sexes?|Male|Female)\s+", re.IGNORECASE)


def extract_p11d1(pdf_path, csv_stem=None):
    """
    Extract disability table (p11d1) which has 3 sex sub-rows per district.
    """
    lines = get_text_lines(pdf_path)

    rows = []
    current_district = None

    for ln in lines:
        # Attempt AREA_PAT match first
        m = AREA_PAT.match(ln)
        if m:
            label = m.group(0).strip()
            label = re.sub(
                r"\s*\(\d+\s*districts?\)", "", label, flags=re.IGNORECASE
            ).strip()
            # Check whether any real data values follow the district name
            rest = ln[m.end() :]
            nums = re.findall(r"-?[\d,]+\.?\d*", rest)
            if not nums:
                # Standalone district heading — next lines are sex sub-rows
                current_district = label
            continue  # always skip AREA_PAT lines (data comes from sub-rows)

        # Check for sex sub-row
        sm = SEX_SUBROW_PAT.match(ln)
        if sm and current_district:
            sex = sm.group(1).lower().replace(" ", "_")
            rest = ln[sm.end() :]
            nums = re.findall(r"-?[\d,]+\.?\d*", rest)
            values = [n.replace(",", "") for n in nums]
            rows.append([current_district, sex] + values)

    if not rows:
        return None

    max_len = max(len(r) for r in rows)
    rows = [r + [None] * (max_len - len(r)) for r in rows]

    n_val_cols = max_len - 2  # subtract district and sex columns

    if csv_stem and csv_stem in COLUMN_OVERRIDES:
        override = COLUMN_OVERRIDES[csv_stem]
        val_cols = (
            override + [f"col_{i+1}" for i in range(len(override), n_val_cols)]
        )[:n_val_cols]
    else:
        col_names = get_col_names_from_pdf(pdf_path, 0, lines)
        if len(col_names) >= n_val_cols:
            val_cols = col_names[:n_val_cols]
        else:
            val_cols = col_names + [
                f"col_{i+1}" for i in range(len(col_names), n_val_cols)
            ]

    cols = ["district", "sex"] + val_cols
    df = pd.DataFrame(rows, columns=cols)
    df = df.replace("-", pd.NA)
    return df


# ── p9p4 special extractor ────────────────────────────────────────────────────
# Structure: three sections (BOTH SEXES / MALE / FEMALE), each with district rows.
# Each district row has total_population + counts by age group.
# District name can span two lines split awkwardly.

AGE_GROUPS = [
    "0-4",
    "5-9",
    "10-14",
    "15-19",
    "20-24",
    "25-29",
    "30-34",
    "35-39",
    "40-44",
    "45-49",
    "50-54",
    "55-59",
    "60-64",
    "65-69",
    "70-74",
    "75 and over",
]

SEX_SECTION_PAT = re.compile(r"^(BOTH SEXES|MALE|FEMALE)\s*$", re.IGNORECASE)


def extract_p9p4(pdf_path, csv_stem=None):
    """
    Extract population by district, 5-year age group, and sex.
    Returns a wide DataFrame (one row per district × sex, columns = age groups).
    """
    lines = get_text_lines(pdf_path)

    rows = []
    current_sex = None
    pending_label = (
        None  # for split district names like "Total - 18\nDistricts"
    )

    for ln in lines:
        # Section header
        if SEX_SECTION_PAT.match(ln):
            current_sex = ln.strip().lower().replace(" ", "_")
            pending_label = None
            continue

        if current_sex is None:
            continue

        # Check for district name alone (split across lines in this PDF)
        m = AREA_PAT.match(ln)
        if m:
            # Could be district + numbers on same line, or district alone
            rest = ln[m.end() :].strip()
            label = m.group(0).strip()
            label = re.sub(
                r"\s*\(\d+\s*districts?\)", "", label, flags=re.IGNORECASE
            ).strip()
            nums = re.findall(r"-?[\d,]+\.?\d*", rest)
            if nums:
                values = [n.replace(",", "") for n in nums]
                rows.append([label, current_sex] + values)
                pending_label = None
            else:
                # District name alone — next numeric line is the data
                pending_label = label
            continue

        # Continuation / data line for a split district
        if pending_label:
            nums = re.findall(r"-?[\d,]+\.?\d*", ln)
            if nums:
                values = [n.replace(",", "") for n in nums]
                rows.append([pending_label, current_sex] + values)
                pending_label = None

    if not rows:
        return None

    max_len = max(len(r) for r in rows)
    rows = [r + [None] * (max_len - len(r)) for r in rows]

    n_val_cols = max_len - 2
    # First value col is total population, rest are age groups
    age_cols = AGE_GROUPS[: n_val_cols - 1] if n_val_cols > 1 else []
    val_cols = ["total_population"] + age_cols
    # Pad/trim
    if len(val_cols) < n_val_cols:
        val_cols += [f"age_col_{i}" for i in range(len(val_cols), n_val_cols)]
    else:
        val_cols = val_cols[:n_val_cols]

    cols = ["district", "sex"] + val_cols
    df = pd.DataFrame(rows, columns=cols)
    df = df.replace("-", pd.NA)
    return df


# ── PDF → CSV mapping ────────────────────────────────────────────────────────


def find_pdf(pattern):
    """
    Find a PDF in ORIG_DIR matching a glob pattern.
    When multiple files match (e.g. p9p2*.pdf matches p9p2Popul... and p9p20...),
    prefer the file whose suffix after the literal prefix does NOT start with a
    digit, so p9p2Population... wins over p9p20Percentage...
    """
    matches = sorted(ORIG_DIR.glob(pattern), key=lambda p: p.name)
    if not matches:
        return None
    prefix = pattern.split("*")[0]  # literal part before the wildcard
    for m in matches:
        suffix = m.stem[len(prefix) :]
        if not suffix or not suffix[0].isdigit():
            return m
    return matches[0]


# ── manual column-name overrides (keyed by csv_stem) ─────────────────────────
# Values are the numeric column names only (district column is always first).
# For p11d1, district & sex come first; the list covers the value columns.

COLUMN_OVERRIDES = {
    "population_growth_by_district": [
        "population_1981",
        "population_2001",
        "intercensal_increase_no",
        "intercensal_increase_pct",
        "avg_annual_growth_rate_pct",
    ],
    "population_sex_ratio_density_by_district": [
        "total_population",
        "male",
        "female",
        "sex_ratio_males_per_100_females",
        "pop_density_per_sqkm",
    ],
    "population_by_sector_by_district": [
        "total_population",
        "urban_no",
        "urban_pct",
        "rural_no",
        "rural_pct",
        "estate_no",
        "estate_pct",
    ],
    "dependency_ratio_by_district": [
        "total_population",
        "age_0_14",
        "age_15_59",
        "age_60_plus",
        "total_dep_ratio",
        "young_dep_ratio_0_14",
        "old_dep_ratio_60_plus",
    ],
    "marital_status_by_district": [
        "total_population",
        "never_married_no",
        "never_married_pct",
        "total_married_no",
        "total_married_pct",
        "legally_married_no",
        "legally_married_pct",
        "customary_married_no",
        "customary_married_pct",
        "widowed_no",
        "widowed_pct",
        "divorced_no",
        "divorced_pct",
        "legally_separated_no",
        "legally_separated_pct",
        "not_stated_no",
        "not_stated_pct",
    ],
    "ethnicity_by_district": [
        "total_population",
        "total_pct",
        "sinhalese_no",
        "sinhalese_pct",
        "sl_tamil_no",
        "sl_tamil_pct",
        "indian_tamil_no",
        "indian_tamil_pct",
        "sl_moor_no",
        "sl_moor_pct",
        "burgher_no",
        "burgher_pct",
        "malay_no",
        "malay_pct",
        "other_no",
        "other_pct",
    ],
    "religion_by_district": [
        "total_population",
        "total_pct",
        "buddhist_no",
        "buddhist_pct",
        "hindu_no",
        "hindu_pct",
        "islam_no",
        "islam_pct",
        "roman_catholic_no",
        "roman_catholic_pct",
        "other_christian_no",
        "other_christian_pct",
        "other_religion_no",
        "other_religion_pct",
    ],
    "literacy_rates_by_district": [
        "total_literacy_rate_pct",
        "male_literacy_rate_pct",
        "female_literacy_rate_pct",
        "urban_literacy_rate_pct",
        "rural_literacy_rate_pct",
        "estate_literacy_rate_pct",
    ],
    "not_attending_school_by_district": [
        "total_not_attending_pct",
        "urban_not_attending_pct",
        "rural_not_attending_pct",
        "estate_not_attending_pct",
    ],
    "labour_force_participation_by_district": [
        "total_employed_pop_age_10plus",
        "total_lfpr_pct",
        "male_lfpr_pct",
        "female_lfpr_pct",
    ],
    "unemployment_rates_by_district": [
        "total_unemployment_rate_pct",
        "male_unemployment_rate_pct",
        "female_unemployment_rate_pct",
        "grade_0_4_pct",
        "grade_5_9_pct",
        "gce_ol_pct",
        "gce_al_pct",
        "above_al_pct",
    ],
    "not_economically_active_by_district": [
        "total_nea_pop",
        "attending_school_pct",
        "homemakers_pct",
        "pensioners_ill_pct",
        "unable_to_work_pct",
        "other_nea_pct",
    ],
    "employment_status_by_district": [
        "total_employed_pop",
        "govt_employees_pct",
        "semi_govt_pct",
        "private_employees_pct",
        "own_account_workers_pct",
        "unpaid_family_workers_pct",
    ],
    "agricultural_fishery_workers_by_district": [
        "total_employed_pop",
        "agricultural_fishery_no",
        "agricultural_fishery_pct",
        "non_agricultural_no",
        "non_agricultural_pct",
    ],
    "children_born_by_district": [
        "avg_children_born_total",
        "avg_children_born_urban",
        "avg_children_born_rural",
        "avg_children_born_estate",
    ],
    # Housing
    "housing_occupied_units_by_district": [
        "total_occupied_units",
        "urban",
        "rural",
        "estate",
    ],
    "housing_type_by_district": [
        "total_occupied_units",
        "permanent_no",
        "permanent_pct",
        "semi_permanent_no",
        "semi_permanent_pct",
        "improvised_no",
        "improvised_pct",
    ],
    "housing_construction_materials_by_district": [
        "total_occupied_units",
        "blocks_stones_no",
        "blocks_stones_pct",
        "granite_concrete_no",
        "granite_concrete_pct",
        "metal_sheets_no",
        "metal_sheets_pct",
    ],
    "housing_huts_shanties_by_district": [
        "total_occupied_units",
        "huts_shanties_no",
        "huts_shanties_pct",
    ],
    "housing_rooms_per_unit_by_district": [
        "avg_rooms_total",
        "avg_rooms_permanent",
        "avg_rooms_semi_permanent",
        "avg_rooms_improvised",
    ],
    "housing_household_size_by_district": [
        "total_households",
        "urban_households",
        "rural_households",
        "estate_households",
        "avg_household_size",
        "female_headed_hh_no",
        "female_headed_hh_pct",
    ],
    "housing_toilet_facilities_by_district": [
        "total_households",
        "using_toilet_no",
        "using_toilet_pct",
        "using_hygienic_toilet_no",
        "using_hygienic_toilet_pct",
        "not_using_toilet_no",
        "not_using_toilet_pct",
    ],
    "housing_drinking_water_by_district": [
        "total_households",
        "using_pipe_water_no",
        "using_pipe_water_pct",
        "using_safe_water_no",
        "using_safe_water_pct",
    ],
    "housing_lighting_by_district": [
        "total_households",
        "using_electricity_no",
        "using_electricity_pct",
        "urban_electricity_no",
        "urban_electricity_pct",
        "rural_electricity_no",
        "rural_electricity_pct",
        "estate_electricity_no",
        "estate_electricity_pct",
    ],
    "housing_cooking_fuel_by_district": [
        "total_households",
        "firewood_no",
        "firewood_pct",
        "lpgas_no",
        "lpgas_pct",
        "kerosene_no",
        "kerosene_pct",
    ],
    "housing_tenure_by_district": [
        "total_households",
        "owner_occupied_no",
        "owner_occupied_pct",
        "rent_free_no",
        "rent_free_pct",
        "rent_lease_no",
        "rent_lease_pct",
        "encroached_no",
        "encroached_pct",
    ],
    # Disability: first two cols are already district + sex
    "disability_by_sex_and_district": [
        "total_disabled_no",
        "total_disabled_rate",
        "seeing_disability_no",
        "seeing_disability_rate",
        "hearing_speaking_no",
        "hearing_speaking_rate",
        "hands_disability_no",
        "hands_disability_rate",
        "legs_disability_no",
        "legs_disability_rate",
        "mental_disability_no",
        "mental_disability_rate",
        "other_disability_no",
        "other_disability_rate",
    ],
    # Tables where PDF has rotated text headers or the first "total" column
    # was miscounted by coordinate detection — all corrected manually.
    "educational_attainment_by_district": [
        "total_population_age_5plus",
        "grade_1_5_pct",
        "grade_6_8_pct",
        "grade_9_11_gce_ol_pct",
        "gce_al_and_above_pct",
    ],
    "school_attendance_5_34_by_district": [
        "total_population_aged_5_34",
        "attending_school_pct",
        "attending_university_pct",
        "attending_technical_institution_pct",
    ],
    "school_attendance_6_19_by_district": [
        "age_6_9_attendance_rate_pct",
        "age_10_14_attendance_rate_pct",
        "age_15_19_not_attending_pct",
        "age_6_14_attendance_rate_pct",
        "age_15_19_attendance_rate_pct",
    ],
    "language_speaking_by_district": [
        "tamil_speaking_english_pct",
        "tamil_speaking_sinhala_pct",
        "sinhala_speaking_tamil_pct",
        "sinhala_speaking_english_pct",
        "sl_moor_speaking_sinhala_pct",
        "sl_moor_speaking_tamil_pct",
        "other_speaking_sinhala_pct",
        "other_speaking_tamil_pct",
    ],
    "migration_by_district": [
        "total_population",
        "resident_since_birth",
        "total_migrants",
        "migrated_less_than_1_year",
        "migrated_1_4_years",
        "migrated_5_9_years",
        "migrated_10_years_and_more",
        "migration_duration_not_stated",
    ],
    "occupation_by_district": [
        "total_employed_pop",
        "legislators_officials_managers_pct",
        "professionals_pct",
        "technicians_associate_pct",
        "clerks_pct",
        "service_sales_workers_pct",
        "agricultural_fishery_workers_pct",
        "craft_related_workers_pct",
        "plant_machine_operators_pct",
        "private_business_owners_pct",
        "elementary_occupations_pct",
        "unidentifiable_pct",
    ],
    "industry_by_district": [
        "total_employed_pop",
        "agriculture_hunting_forestry_pct",
        "fishing_pct",
        "mining_quarrying_pct",
        "manufacturing_pct",
        "electricity_gas_water_pct",
        "construction_pct",
        "wholesale_retail_pct",
        "hotels_restaurants_pct",
        "transport_storage_communication_pct",
        "financial_pct",
        "real_estate_renting_business_pct",
        "public_admin_defence_pct",
        "education_pct",
        "health_social_work_pct",
        "other_community_services_pct",
        "private_households_pct",
        "extra_territorial_pct",
        "not_identifiable_pct",
        "armed_forces_pct",
    ],
    "non_agricultural_workers_by_district": [
        "total_employed_pop",
        "legislators_professionals_technicians_clerks_pct",
        "service_private_business_owners_pct",
        "related_workers_pct",
        "not_identifiable_pct",
    ],
    "agricultural_subgroup_by_district": [
        "total_agricultural_fishery_workers",
        "crop_growers_pct",
        "animal_producers_pct",
        "market_gardeners_pct",
        "related_agricultural_workers_pct",
        "hunters_trappers_pct",
        "fishery_workers_pct",
        "related_fishery_workers_pct",
        "not_elsewhere_classifiable_pct",
    ],
}


PDF_MAP = {
    # filename_glob: output_csv_stem
    "p9p1Growth.pdf": "population_growth_by_district",
    "p9p2*.pdf": "population_sex_ratio_density_by_district",
    "p9p4*.pdf": "population_by_district_age_sex",  # special
    "p9p5*.pdf": "population_by_sector_by_district",
    "p9p6*.pdf": "dependency_ratio_by_district",
    "p9p7*.pdf": "marital_status_by_district",
    "p9p8*.pdf": "ethnicity_by_district",
    "p9p9*.pdf": "religion_by_district",
    "p9p10*.pdf": "literacy_rates_by_district",
    "p9p11*.pdf": "language_speaking_by_district",
    "p9p12*.pdf": "school_attendance_5_34_by_district",
    "p9p13*.pdf": "school_attendance_6_19_by_district",
    "p9p14*.pdf": "not_attending_school_by_district",
    "p9p15*.pdf": "educational_attainment_by_district",
    "p9p16*.pdf": "labour_force_participation_by_district",
    "p9p17*.pdf": "unemployment_rates_by_district",
    "p9p18*.pdf": "not_economically_active_by_district",
    "p9p19*.pdf": "employment_status_by_district",
    "p9p20*.pdf": "occupation_by_district",
    "p9p21*.pdf": "industry_by_district",
    "p9p22*.pdf": "agricultural_fishery_workers_by_district",
    "p9p23*.pdf": "agricultural_subgroup_by_district",
    "p9p24*.pdf": "non_agricultural_workers_by_district",
    "p9p25*.pdf": "migration_by_district",
    "p9p26*.pdf": "children_born_by_district",
    "p10h1*.pdf": "housing_occupied_units_by_district",
    "p10h2*.pdf": "housing_type_by_district",
    "p10h3*.pdf": "housing_construction_materials_by_district",
    "p10h4*.pdf": "housing_huts_shanties_by_district",
    "p10h5*.pdf": "housing_rooms_per_unit_by_district",
    "p10h6*.pdf": "housing_household_size_by_district",
    "p10h7*.pdf": "housing_toilet_facilities_by_district",
    "p10h8*.pdf": "housing_drinking_water_by_district",
    "p10h9*.pdf": "housing_lighting_by_district",
    "p10h10*.pdf": "housing_cooking_fuel_by_district",
    "p10h11*.pdf": "housing_tenure_by_district",
    "p11d1*.pdf": "disability_by_sex_and_district",  # special
}

SPECIAL_HANDLERS = {
    "p9p4": extract_p9p4,
    "p11d1": extract_p11d1,
}


# ── main ─────────────────────────────────────────────────────────────────────


def main():
    DATA_DIR.mkdir(exist_ok=True)
    results = []

    for glob_pat, csv_stem in PDF_MAP.items():
        pdf_path = find_pdf(glob_pat)
        if pdf_path is None:
            print(f"[SKIP] No file found for pattern: {glob_pat}")
            continue

        output_path = DATA_DIR / f"{csv_stem}.csv"
        print(f"[→] {pdf_path.name}")

        # Determine handler
        handler = extract_simple
        for key, fn in SPECIAL_HANDLERS.items():
            if pdf_path.name.lower().startswith(key.lower()):
                handler = fn
                break

        try:
            df = handler(pdf_path, csv_stem=csv_stem)
        except Exception as e:
            print(f"    ERROR: {e}")
            results.append((csv_stem, pdf_path.name, "ERROR", str(e)))
            continue

        if df is None or df.empty:
            print(f"    WARNING: No data extracted")
            results.append((csv_stem, pdf_path.name, "EMPTY", ""))
            continue

        df.to_csv(output_path, index=False)
        print(
            f"    ✓  {len(df)} rows, {len(df.columns)} cols → {output_path.name}"
        )
        results.append((csv_stem, pdf_path.name, "OK", f"{len(df)} rows"))

    print("\n" + "=" * 60)
    print("SUMMARY")
    for csv_stem, pdf_name, status, note in results:
        print(f"  [{status:5s}] {csv_stem}.csv  ← {pdf_name}  {note}")


if __name__ == "__main__":
    os.chdir(str(WORK_DIR))
    main()
