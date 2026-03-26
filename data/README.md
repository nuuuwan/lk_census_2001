# Data Directory — Sri Lanka Census of Population and Housing 2001

Extracted from statistical tables in the [original PDFs](../original_data/README.md).

All district-level tables are extracted as CSVs. Each row represents one
administrative area (district, or an aggregate "Total" row). Numbers with commas
have been stripped of commas; dash values (`-`) are stored as empty/NaN.

**Coverage notes**
- Most tables cover **18 districts** (the districts for which census data was
  collected; conflict-affected areas Jaffna, Mannar, Vavuniya, Mullaitivu,
  Kilinochchi, Batticaloa, Trincomalee were partially or fully excluded from
  some tables).
- Population and growth tables additionally include a **Sri Lanka** aggregate and
  a **Total – 18 Districts** sub-total.
- The `disability_by_sex_and_district.csv` and
  `population_by_district_age_sex.csv` tables are in **long format** with a
  `sex` column.

---

## 1. Population — Overview

### `population_growth_by_district.csv`
**Source:** `p9p1Growth.pdf`  
Population size and intercensal change between the 1981 and 2001 censuses.

| Column | Description |
|---|---|
| `district` | District / area name |
| `population_1981` | Census population, 1981 |
| `population_2001` | Census population, 2001 |
| `intercensal_increase_no` | Absolute population change 1981–2001 (can be negative) |
| `intercensal_increase_pct` | Percentage population change 1981–2001 |
| `avg_annual_growth_rate_pct` | Average annual growth rate (%) |

---

### `population_sex_ratio_density_by_district.csv`
**Source:** `p9p2Populationbydistrictsexsexratioandpopulationdensity.pdf`  
Total population, sex breakdown, sex ratio, and population density.

| Column | Description |
|---|---|
| `district` | District / area name |
| `total_population` | Total census population, 2001 |
| `male` | Male population |
| `female` | Female population |
| `sex_ratio_males_per_100_females` | Males per 100 females |
| `pop_density_per_sqkm` | Population per square kilometre |

---

### `population_by_district_age_sex.csv`
**Source:** `p9p4Populationbydistrict5yearagegroupsandsex.pdf`  
Long-format table: one row per (district × sex) combination. Age groups are
5-year bands.

| Column | Description |
|---|---|
| `district` | District / area name |
| `sex` | `both_sexes`, `male`, or `female` |
| `total_population` | Total population for that sex group |
| `0-4` … `75 and over` | Count in each 5-year age group |

---

### `population_by_sector_by_district.csv`
**Source:** `p9p5Numberandpercentageofpopulationbydistrictandsector.pdf`  
Population split by sector (Urban / Rural / Estate).

| Column | Description |
|---|---|
| `district` | District / area name |
| `total_population` | Total population |
| `urban_no` | Urban sector population |
| `urban_pct` | Urban population as % of total |
| `rural_no` | Rural sector population |
| `rural_pct` | Rural population as % of total |
| `estate_no` | Estate sector population |
| `estate_pct` | Estate population as % of total |

---

### `dependency_ratio_by_district.csv`
**Source:** `p9p6Dependancy.pdf`  
Age-structure indicators.

| Column | Description |
|---|---|
| `district` | District / area name |
| `total_population` | Total population |
| `age_0_14` | Population aged 0–14 |
| `age_15_59` | Population aged 15–59 |
| `age_60_plus` | Population aged 60 and over |
| `total_dep_ratio` | Total dependency ratio |
| `young_dep_ratio_0_14` | Young-age dependency ratio (0–14) |
| `old_dep_ratio_60_plus` | Old-age dependency ratio (60+) |

---

## 2. Population — Social Characteristics

### `marital_status_by_district.csv`
**Source:** `p9p7Marital.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_population` | Total population aged 15+ |
| `never_married_no` / `_pct` | Never married — count and % |
| `total_married_no` / `_pct` | Total married (legal + customary) — count and % |
| `legally_married_no` / `_pct` | Legally (registered) married |
| `customary_married_no` / `_pct` | Customarily married |
| `widowed_no` / `_pct` | Widowed |
| `divorced_no` / `_pct` | Divorced |
| `legally_separated_no` / `_pct` | Legally separated |
| `not_stated_no` / `_pct` | Marital status not stated |

---

### `ethnicity_by_district.csv`
**Source:** `p9p8Ethnicity.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_population` | Total population |
| `total_pct` | Always 100 (reference) |
| `sinhalese_no` / `_pct` | Sinhalese ethnic group |
| `sl_tamil_no` / `_pct` | Sri Lanka Tamil |
| `indian_tamil_no` / `_pct` | Indian Tamil |
| `sl_moor_no` / `_pct` | Sri Lanka Moor |
| `burgher_no` / `_pct` | Burgher |
| `malay_no` / `_pct` | Malay |
| `other_no` / `_pct` | Other ethnicities |

---

### `religion_by_district.csv`
**Source:** `p9p9Religion.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_population` | Total population |
| `total_pct` | Always 100 (reference) |
| `buddhist_no` / `_pct` | Buddhist |
| `hindu_no` / `_pct` | Hindu |
| `islam_no` / `_pct` | Islam |
| `roman_catholic_no` / `_pct` | Roman Catholic |
| `other_christian_no` / `_pct` | Other Christian |
| `other_religion_no` / `_pct` | Other religions |

---

### `language_speaking_by_district.csv`
**Source:** `p9p11Speaking.pdf`  
Percentage of the population who speak a second language, broken down by
mother-tongue group.

| Column | Description |
|---|---|
| `district` | District |
| `tamil_speaking_english_pct` | % of Tamil speakers who speak English |
| `tamil_speaking_sinhala_pct` | % of Tamil speakers who speak Sinhala |
| `sinhala_speaking_tamil_pct` | % of Sinhala speakers who speak Tamil |
| `sinhala_speaking_english_pct` | % of Sinhala speakers who speak English |
| `sl_moor_speaking_sinhala_pct` | % of Sri Lanka Moor who speak Sinhala |
| `sl_moor_speaking_tamil_pct` | % of Sri Lanka Moor who speak Tamil |
| `other_speaking_sinhala_pct` | % of other groups who speak Sinhala |
| `other_speaking_tamil_pct` | % of other groups who speak Tamil |

---

## 3. Population — Education

### `literacy_rates_by_district.csv`
**Source:** `p9p10Literacyratesbydistrictsexandsector.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_literacy_rate_pct` | Overall literacy rate (%) |
| `male_literacy_rate_pct` | Male literacy rate |
| `female_literacy_rate_pct` | Female literacy rate |
| `urban_literacy_rate_pct` | Urban sector literacy rate |
| `rural_literacy_rate_pct` | Rural sector literacy rate |
| `estate_literacy_rate_pct` | Estate sector literacy rate |

---

### `school_attendance_5_34_by_district.csv`
**Source:** `p9p12Attendance5-34.pdf`  
School / institution attendance among population aged 5–34.

| Column | Description |
|---|---|
| `district` | District |
| `total_population_aged_5_34` | Population aged 5–34 |
| `attending_school_pct` | % attending school |
| `attending_university_pct` | % attending university |
| `attending_technical_institution_pct` | % attending technical/other institutions |

---

### `school_attendance_6_19_by_district.csv`
**Source:** `p9p13Attendance6-19.pdf`  
Attendance rates by narrower age groups within the 6–19 age range.

| Column | Description |
|---|---|
| `district` | District |
| `age_6_9_attendance_rate_pct` | Attendance rate, ages 6–9 |
| `age_10_14_attendance_rate_pct` | Attendance rate, ages 10–14 |
| `age_15_19_not_attending_pct` | Not attending school rate, ages 15–19 |
| `age_6_14_attendance_rate_pct` | Attendance rate, combined 6–14 |
| `age_15_19_attendance_rate_pct` | Attendance rate, ages 15–19 |

---

### `not_attending_school_by_district.csv`
**Source:** `p9p14Notattending6-14.pdf`  
Percentage of children aged 6–14 not attending any educational institution.

| Column | Description |
|---|---|
| `district` | District |
| `total_not_attending_pct` | % not attending school, ages 6–14 (total) |
| `urban_not_attending_pct` | Urban sector |
| `rural_not_attending_pct` | Rural sector |
| `estate_not_attending_pct` | Estate sector |

---

### `educational_attainment_by_district.csv`
**Source:** `p9p15Attainment.pdf`  
Highest educational attainment of the population aged 5+.

| Column | Description |
|---|---|
| `district` | District |
| `total_population_age_5plus` | Population aged 5 and over |
| `grade_1_5_pct` | % whose highest attainment is Grade 1–5 |
| `grade_6_8_pct` | % whose highest attainment is Grade 6–8 |
| `grade_9_11_gce_ol_pct` | % with Grade 9–11 / GCE O-Level |
| `gce_al_and_above_pct` | % with GCE A-Level and above |

---

## 4. Population — Labour Force

### `labour_force_participation_by_district.csv`
**Source:** `p9p16Labourforceparticipationratesbydistrictandsex.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_employed_pop_age_10plus` | Total employed population aged 10+ |
| `total_lfpr_pct` | Labour force participation rate — total (%) |
| `male_lfpr_pct` | Male labour force participation rate |
| `female_lfpr_pct` | Female labour force participation rate |

---

### `unemployment_rates_by_district.csv`
**Source:** `p9p17Unemploymentratesbydistrictsexandlevelofeducation.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_unemployment_rate_pct` | Overall unemployment rate (%) |
| `male_unemployment_rate_pct` | Male unemployment rate |
| `female_unemployment_rate_pct` | Female unemployment rate |
| `grade_0_4_pct` | Unemployment rate, no schooling / Grade 0–4 education |
| `grade_5_9_pct` | Unemployment rate, Grade 5–9 education |
| `gce_ol_pct` | Unemployment rate, GCE O-Level |
| `gce_al_pct` | Unemployment rate, GCE A-Level |
| `above_al_pct` | Unemployment rate, above A-Level |

---

### `not_economically_active_by_district.csv`
**Source:** `p9p18Percentageofnoteconomicallyactivepopulationbydistrict.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_nea_pop` | Not economically active population (count) |
| `attending_school_pct` | % attending school / full-time students |
| `homemakers_pct` | % homemakers |
| `pensioners_ill_pct` | % pensioners / ill / retired |
| `unable_to_work_pct` | % unable to work |
| `other_nea_pct` | % other not economically active |

---

### `employment_status_by_district.csv`
**Source:** `p9p19employmentstatus.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_employed_pop` | Total employed population aged 10+ |
| `govt_employees_pct` | % government employees |
| `semi_govt_pct` | % semi-government employees |
| `private_employees_pct` | % private-sector employees |
| `own_account_workers_pct` | % own-account (self-employed) workers |
| `unpaid_family_workers_pct` | % unpaid family workers |

---

### `occupation_by_district.csv`
**Source:** `p9p20Percentageofemployedpopulationbydistrictandmajorgroupsofoccupation.pdf`  
ISCO-88 major occupation groups.

| Column | Description |
|---|---|
| `district` | District |
| `total_employed_pop` | Total employed population aged 10+ |
| `legislators_officials_managers_pct` | % Legislators, Senior Officials, Managers |
| `professionals_pct` | % Professionals |
| `technicians_associate_pct` | % Technicians and Associate Professionals |
| `clerks_pct` | % Clerks |
| `service_sales_workers_pct` | % Service Workers and Shop/Market Sales Workers |
| `agricultural_fishery_workers_pct` | % Skilled Agricultural and Fishery Workers |
| `craft_related_workers_pct` | % Craft and Related Trade Workers |
| `plant_machine_operators_pct` | % Plant and Machine Operators and Assemblers |
| `private_business_owners_pct` | % Private Business Owners |
| `elementary_occupations_pct` | % Elementary Occupations |
| `unidentifiable_pct` | % Unidentifiable / Inadequate occupations |

---

### `industry_by_district.csv`
**Source:** `p9p21Percentageofemployedpopulationbydistrictandmajorgroupsofindustry.pdf`  
ISIC major industry groups.

| Column | Description |
|---|---|
| `district` | District |
| `total_employed_pop` | Total employed population aged 10+ |
| `agriculture_hunting_forestry_pct` | % Agriculture, Hunting, Forestry |
| `fishing_pct` | % Fishing |
| `mining_quarrying_pct` | % Mining and Quarrying |
| `manufacturing_pct` | % Manufacturing |
| `electricity_gas_water_pct` | % Electricity, Gas and Water Supply |
| `construction_pct` | % Construction |
| `wholesale_retail_pct` | % Wholesale and Retail Trade |
| `hotels_restaurants_pct` | % Hotels and Restaurants |
| `transport_storage_communication_pct` | % Transport, Storage and Communications |
| `financial_pct` | % Financial Intermediation |
| `real_estate_renting_business_pct` | % Real Estate, Renting and Business Activities |
| `public_admin_defence_pct` | % Public Administration and Defence |
| `education_pct` | % Education |
| `health_social_work_pct` | % Health and Social Work |
| `other_community_services_pct` | % Other Community and Personal Services |
| `private_households_pct` | % Private Households with Employed Persons |
| `extra_territorial_pct` | % Extra-Territorial Organisations |
| `not_identifiable_pct` | % Not identifiable / Inadequate |
| `armed_forces_pct` | % Armed Forces / Not elsewhere classified |

---

### `agricultural_fishery_workers_by_district.csv`
**Source:** `p9p22Numberandpercentageofagriculturalandfisheryworkersandnonagricultural.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_employed_pop` | Total employed population |
| `agricultural_fishery_no` | Agricultural and fishery workers (count) |
| `agricultural_fishery_pct` | Agricultural and fishery workers (%) |
| `non_agricultural_no` | Non-agricultural workers (count) |
| `non_agricultural_pct` | Non-agricultural workers (%) |

---

### `agricultural_subgroup_by_district.csv`
**Source:** `p9p23Percentageofemployedpopulationinagriculturalfisherysectorbydistrictandsubgroup.pdf`  
Sub-groups within the agricultural and fishery sector.

| Column | Description |
|---|---|
| `district` | District |
| `total_agricultural_fishery_workers` | Total agricultural and fishery workers |
| `crop_growers_pct` | % Crop and plant growers |
| `animal_producers_pct` | % Animal producers |
| `market_gardeners_pct` | % Market gardeners |
| `related_agricultural_workers_pct` | % Related agricultural workers |
| `hunters_trappers_pct` | % Hunters and trappers |
| `fishery_workers_pct` | % Fishery workers |
| `related_fishery_workers_pct` | % Related fishery workers |
| `not_elsewhere_classifiable_pct` | % Not elsewhere classifiable |

---

### `non_agricultural_workers_by_district.csv`
**Source:** `p9p24non-agriculture.pdf`  
Non-agricultural and fishery workers by broad occupation sector.

| Column | Description |
|---|---|
| `district` | District |
| `total_employed_pop` | Total employed population |
| `legislators_professionals_technicians_clerks_pct` | % Legislators, Professionals, Technicians, Clerks |
| `service_private_business_owners_pct` | % Service Workers and Private Business Owners |
| `related_workers_pct` | % Craft, Plant/Machine, Elementary Workers |
| `not_identifiable_pct` | % Not identifiable or Inadequate |

---

## 5. Population — Migration and Fertility

### `migration_by_district.csv`
**Source:** `p9p25Migration.pdf`  
Population by usual district of residence, resident status, and duration of
migration. Rows include 25 districts and Sri Lanka total (26 rows).

| Column | Description |
|---|---|
| `district` | District of usual residence |
| `total_population` | Total population |
| `resident_since_birth` | Population resident in current district since birth |
| `total_migrants` | Total migrant population |
| `migrated_less_than_1_year` | Migrants who moved less than 1 year ago |
| `migrated_1_4_years` | Migrants who moved 1–4 years ago |
| `migrated_5_9_years` | Migrants who moved 5–9 years ago |
| `migrated_10_years_and_more` | Migrants who moved 10+ years ago |
| `migration_duration_not_stated` | Duration of migration not stated |

---

### `children_born_by_district.csv`
**Source:** `p9p26Childrenborn.pdf`  
Average number of live children ever born per woman, by sector.

| Column | Description |
|---|---|
| `district` | District |
| `avg_children_born_total` | Average children born (all sectors) |
| `avg_children_born_urban` | Urban sector |
| `avg_children_born_rural` | Rural sector |
| `avg_children_born_estate` | Estate sector |

---

## 6. Housing

### `housing_occupied_units_by_district.csv`
**Source:** `p10h1Numberofoccupiedhousingunitsbydistrictandsector.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_occupied_units` | Total occupied housing units |
| `urban` | Urban sector occupied units |
| `rural` | Rural sector occupied units |
| `estate` | Estate sector occupied units |

---

### `housing_type_by_district.csv`
**Source:** `p10h2NumberandpercentageofoccupiedhousingunitsbydistrictandtypeofHousingUnit.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_occupied_units` | Total occupied housing units |
| `permanent_no` / `_pct` | Permanent housing units |
| `semi_permanent_no` / `_pct` | Semi-permanent housing units |
| `improvised_no` / `_pct` | Improvised housing units |

---

### `housing_construction_materials_by_district.csv`
**Source:** `p10h3ConsMaterials.pdf`  
Housing units by main construction material used for walls/roof.

| Column | Description |
|---|---|
| `district` | District |
| `total_occupied_units` | Total occupied housing units |
| `blocks_stones_no` / `_pct` | Units with blocks / stones |
| `granite_concrete_no` / `_pct` | Units with granite / concrete |
| `metal_sheets_no` / `_pct` | Units with metal sheets |

---

### `housing_huts_shanties_by_district.csv`
**Source:** `p10h4HutsandShanties.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_occupied_units` | Total occupied housing units |
| `huts_shanties_no` | Number of huts and shanties |
| `huts_shanties_pct` | Huts and shanties as % of total units |

---

### `housing_rooms_per_unit_by_district.csv`
**Source:** `p10h5Averageroomsperoccupiedhousingunitbydistrict.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `avg_rooms_total` | Average rooms per unit (all types) |
| `avg_rooms_permanent` | Average rooms — permanent units |
| `avg_rooms_semi_permanent` | Average rooms — semi-permanent units |
| `avg_rooms_improvised` | Average rooms — improvised units |

---

### `housing_household_size_by_district.csv`
**Source:** `p10h6NoofHH.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_households` | Total households in occupied housing units |
| `urban_households` | Urban sector households |
| `rural_households` | Rural sector households |
| `estate_households` | Estate sector households |
| `avg_household_size` | Average household size (persons per household) |
| `female_headed_hh_no` | Female-headed households (count) |
| `female_headed_hh_pct` | Female-headed households (%) |

---

### `housing_toilet_facilities_by_district.csv`
**Source:** `p10h7Toilets.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_households` | Total households |
| `using_toilet_no` / `_pct` | Households using any toilet facility |
| `using_hygienic_toilet_no` / `_pct` | Households using hygienic toilets |
| `not_using_toilet_no` / `_pct` | Households not using any toilet |

---

### `housing_drinking_water_by_district.csv`
**Source:** `p10h8drinkingwater.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_households` | Total households |
| `using_pipe_water_no` / `_pct` | Households using pipe-borne water |
| `using_safe_water_no` / `_pct` | Households using safe drinking water |

---

### `housing_lighting_by_district.csv`
**Source:** `p10h9lighting.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_households` | Total households |
| `using_electricity_no` / `_pct` | Households using electricity (all sectors) |
| `urban_electricity_no` / `_pct` | Urban sector electricity households |
| `rural_electricity_no` / `_pct` | Rural sector electricity households |
| `estate_electricity_no` / `_pct` | Estate sector electricity households |

---

### `housing_cooking_fuel_by_district.csv`
**Source:** `p10h10Cooking.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_households` | Total households |
| `firewood_no` / `_pct` | Households using firewood as cooking fuel |
| `lpgas_no` / `_pct` | Households using LP gas |
| `kerosene_no` / `_pct` | Households using kerosene |

---

### `housing_tenure_by_district.csv`
**Source:** `p10h11Percentageofhouseholdsbydistrictandtenure.pdf`

| Column | Description |
|---|---|
| `district` | District |
| `total_households` | Total households |
| `owner_occupied_no` / `_pct` | Owner-occupied households |
| `rent_free_no` / `_pct` | Rent-free households |
| `rent_lease_no` / `_pct` | Rented or leased households |
| `encroached_no` / `_pct` | Encroached / squatter households |

---

## 7. Disability

### `disability_by_sex_and_district.csv`
**Source:** `p11d1DisabledpersonsbySexandDistrict.pdf`  
Long-format table: one row per (district × sex). Rates are per 10,000 population.

| Column | Description |
|---|---|
| `district` | District |
| `sex` | `both_sexes`, `male`, or `female` |
| `total_disabled_no` | Total disabled persons (count) |
| `total_disabled_rate` | Total disabled rate per 10,000 |
| `seeing_disability_no` / `_rate` | Disability in seeing |
| `hearing_speaking_no` / `_rate` | Disability in hearing/speaking |
| `hands_disability_no` / `_rate` | Disability in hands |
| `legs_disability_no` / `_rate` | Disability in legs |
| `mental_disability_no` / `_rate` | Mental disability |
| `other_disability_no` / `_rate` | Other physical disability |

---

## File Summary

| File | Rows | Cols | Level |
|---|---|---|---|
| `population_growth_by_district.csv` | 27 | 6 | district |
| `population_sex_ratio_density_by_district.csv` | 27 | 6 | district |
| `population_by_district_age_sex.csv` | 59 | 19 | district × sex (long) |
| `population_by_sector_by_district.csv` | 19 | 8 | district |
| `dependency_ratio_by_district.csv` | 20 | 8 | district |
| `marital_status_by_district.csv` | 19 | 18 | district |
| `ethnicity_by_district.csv` | 19 | 17 | district |
| `religion_by_district.csv` | 19 | 15 | district |
| `language_speaking_by_district.csv` | 19 | 9 | district |
| `literacy_rates_by_district.csv` | 19 | 7 | district |
| `school_attendance_5_34_by_district.csv` | 19 | 5 | district |
| `school_attendance_6_19_by_district.csv` | 19 | 6 | district |
| `not_attending_school_by_district.csv` | 19 | 5 | district |
| `educational_attainment_by_district.csv` | 19 | 6 | district |
| `labour_force_participation_by_district.csv` | 19 | 5 | district |
| `unemployment_rates_by_district.csv` | 19 | 9 | district |
| `not_economically_active_by_district.csv` | 19 | 7 | district |
| `employment_status_by_district.csv` | 19 | 7 | district |
| `occupation_by_district.csv` | 19 | 13 | district |
| `industry_by_district.csv` | 19 | 21 | district |
| `agricultural_fishery_workers_by_district.csv` | 19 | 6 | district |
| `agricultural_subgroup_by_district.csv` | 19 | 10 | district |
| `non_agricultural_workers_by_district.csv` | 19 | 6 | district |
| `migration_by_district.csv` | 26 | 9 | district |
| `children_born_by_district.csv` | 19 | 5 | district |
| `housing_occupied_units_by_district.csv` | 19 | 5 | district |
| `housing_type_by_district.csv` | 19 | 8 | district |
| `housing_construction_materials_by_district.csv` | 19 | 8 | district |
| `housing_huts_shanties_by_district.csv` | 19 | 4 | district |
| `housing_rooms_per_unit_by_district.csv` | 19 | 5 | district |
| `housing_household_size_by_district.csv` | 19 | 8 | district |
| `housing_toilet_facilities_by_district.csv` | 19 | 8 | district |
| `housing_drinking_water_by_district.csv` | 19 | 6 | district |
| `housing_lighting_by_district.csv` | 19 | 10 | district |
| `housing_cooking_fuel_by_district.csv` | 19 | 8 | district |
| `housing_tenure_by_district.csv` | 19 | 10 | district |
| `disability_by_sex_and_district.csv` | 57 | 16 | district × sex (long) |
