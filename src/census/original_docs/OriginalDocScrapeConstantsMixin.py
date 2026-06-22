class OriginalDocScrapeConstantsMixin:
    URL_BASE = (
        "https://www.statistics.gov.lk" + "/Population/StaticalInformation/"
    )

    INITIAL_URL_INFO_QUEUE = [
        (
            "https://www.statistics.gov.lk"
            + "/Population/PopHouStat_Population",
            "cph2001_population",
        ),
        (
            "https://www.statistics.gov.lk"
            + "/Population/PopHouStat_Housing",
            "cph2001_housing",
        ),
        (
            "https://www.statistics.gov.lk"
            + "/Population/PopHouStat_Disability",
            "cph2001_disability",
        ),
    ]

    @staticmethod
    def is_valid_url(url: str) -> bool:
        for prefix in [
            "https://www.statistics.gov.lk"
            + "/Population/StaticalInformation/CPH2001/",
            "https://www.statistics.gov.lk"
            + "/Population/PopHouStat_Population",
            "https://www.statistics.gov.lk" + "/Population",
        ]:
            if url.startswith(prefix):
                return True
        return False
