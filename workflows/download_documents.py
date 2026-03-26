"""
Download all documents from the Sri Lanka CPH 2001 census page:
https://www.statistics.gov.lk/Population/StaticalInformation/CPH2001

Uses direct PDF URLs (derived from known iframe-src patterns) to skip wrapper-page
fetches and avoid SSL-handshake hangs on slow connections.
"""

import os
import time
import urllib.error
import urllib.request

BASE_RESOURCE = "https://www.statistics.gov.lk/Resource/en/Population"
OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "original_data"
)

# Direct PDF URLs grouped by source section.
# Patterns confirmed by inspecting iframe src attributes on wrapper pages.
PDF_URLS = [
    # --- Final Results (CPH_2001/) ---
    BASE_RESOURCE
    + "/CPH_2001/BriefAnalysisPopulationHousingCharacteristics.pdf",
    BASE_RESOURCE
    + "/CPH_2001/BriefAnalysisCharacteristicsDisabledPersons.pdf",
    # --- Census Activities (CPH_2001/) ---
    BASE_RESOURCE + "/CPH_2001/OrganizationProcedures.pdf",
    BASE_RESOURCE + "/CPH_2001/ConceptsDefinitions.pdf",
    # --- Questionnaires Used (CPH_2001/) ---
    BASE_RESOURCE + "/CPH_2001/ListingBuildingUnit.pdf",
    BASE_RESOURCE + "/CPH_2001/PopulationHousingSchedule.pdf",
    BASE_RESOURCE + "/CPH_2001/DisabilitySchedule.pdf",
    # --- Data Released (CPH_2001/) ---
    BASE_RESOURCE + "/CPH_2001/ListofPrintedPublicationsandCompactDisks.pdf",
    BASE_RESOURCE + "/CPH_2001/ListofDataAvailableintheDistrictReports.pdf",
    BASE_RESOURCE + "/CPH_2001/ListofDataAvailableintheDistrictCD.pdf",
    BASE_RESOURCE
    + "/CPH_2001/ListofDataAvailableintheCombinedReportoftheCompletedDistricts.pdf",
    BASE_RESOURCE
    + "/CPH_2001/ListofDataAvailableintheCDofAllIslandGramaNiladhari-GNDivisionLevelFinalCensusData.pdf",
    # --- Summary: Population Characteristics ---
    BASE_RESOURCE + "/PopHouStat/PDF/Population/p9p1Growth.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Population/p9p2Populationbydistrictsexsexratioandpopulationdensity.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Population/p9p3PopulationbyFiveyearagegroupsandsex.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Population/p9p4Populationbydistrict5yearagegroupsandsex.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Population/p9p5Numberandpercentageofpopulationbydistrictandsector.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Population/p9p6Dependancy.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Population/p9p7Marital.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Population/p9p8Ethnicity.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Population/p9p9Religion.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Population/p9p10Literacyratesbydistrictsexandsector.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Population/p9p11Speaking.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Population/p9p12Attendance5-34.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Population/p9p13Attendance6-19.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Population/p9p14Notattending6-14.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Population/p9p15Attainment.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Population/p9p16Labourforceparticipationratesbydistrictandsex.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Population/p9p17Unemploymentratesbydistrictsexandlevelofeducation.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Population/p9p18Percentageofnoteconomicallyactivepopulationbydistrict.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Population/p9p19employmentstatus.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Population/p9p20Percentageofemployedpopulationbydistrictandmajorgroupsofoccupation.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Population/p9p21Percentageofemployedpopulationbydistrictandmajorgroupsofindustry.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Population/p9p22Numberandpercentageofagriculturalandfisheryworkersandnonagricultural.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Population/p9p23Percentageofemployedpopulationinagriculturalfisherysectorbydistrictandsubgroup.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Population/p9p24non-agriculture.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Population/p9p25Migration.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Population/p9p26Childrenborn.pdf",
    # --- Summary: Housing Characteristics ---
    BASE_RESOURCE
    + "/PopHouStat/PDF/Housing/p10h1Numberofoccupiedhousingunitsbydistrictandsector.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Housing/p10h2NumberandpercentageofoccupiedhousingunitsbydistrictandtypeofHousingUnit.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Housing/p10h3ConsMaterials.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Housing/p10h4HutsandShanties.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Housing/p10h5Averageroomsperoccupiedhousingunitbydistrict.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Housing/p10h6NoofHH.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Housing/p10h7Toilets.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Housing/p10h8drinkingwater.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Housing/p10h9lighting.pdf",
    BASE_RESOURCE + "/PopHouStat/PDF/Housing/p10h10Cooking.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Housing/p10h11Percentageofhouseholdsbydistrictandtenure.pdf",
    # --- Summary: Disability Characteristics ---
    BASE_RESOURCE
    + "/PopHouStat/PDF/Disability/p11d1DisabledpersonsbySexandDistrict.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Disability/p11d2DisabledpersonsbyAgeandSex.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Disability/p11d3PersonswithDisabilityinSeeingbyCauseofDisabilityandSex.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Disability/p11d4PersonswithDisabilityinHearingSpeakingbyCauseofDisabilityandSex.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Disability/p11d5PersonswithDisabilityinHandsbyCauseofDisabilityandSex.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Disability/p11d6PersonswithDisabilityinLegsbyCauseofDisabilityandSex.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Disability/p11d7PersonswithMentalDisabilitybyCauseofDisabilityandSex.pdf",
    BASE_RESOURCE
    + "/PopHouStat/PDF/Disability/p11d8PersonswithOtherPhysicalDisabilitybyCauseofDisabilityandSex.pdf",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def download_pdf(pdf_url: str, output_path: str) -> bool:
    req = urllib.request.Request(pdf_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        with open(output_path, "wb") as f:
            f.write(data)
        return True
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}")
        return False
    except urllib.error.URLError as e:
        print(f"ERROR: {e.reason}")
        return False


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Saving to: {OUTPUT_DIR}")
    print(f"Total PDFs to check: {len(PDF_URLS)}\n")

    success, skipped, failed = [], [], []

    for pdf_url in PDF_URLS:
        filename = pdf_url.split("/")[-1]
        out_path = os.path.join(OUTPUT_DIR, filename)

        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            print(f"  skip  {filename}")
            skipped.append(filename)
            continue

        print(f"  dl    {filename} ...", end=" ", flush=True)
        ok = download_pdf(pdf_url, out_path)
        if ok:
            size_kb = os.path.getsize(out_path) / 1024
            print(f"{size_kb:.1f} KB")
            success.append(filename)
        else:
            failed.append(filename)

        time.sleep(1)  # polite delay

    print("\n" + "=" * 60)
    print(
        f"Done. {len(success)} downloaded, {len(skipped)} skipped, {len(failed)} failed."
    )
    if failed:
        print("\nFailed:")
        for name in failed:
            print(f"  - {name}")


if __name__ == "__main__":
    main()
