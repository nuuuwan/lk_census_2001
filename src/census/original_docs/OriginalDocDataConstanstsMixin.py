class OriginalDocDataConstanstsMixin:
    # flake8: noqa: C901
    CUSTOM_HEADER_MAP = {
        "percentage-of-employed-population-by-district-and-major-groups-of-industry": [
            "district",
            "total-employed-population",
            "agriculture-and-forestry",
            "fishing",
            "mining-and-quarrying",
            "manufacturing",
            "electricity-gas-and-water-supply",
            "construction",
            "wholesale-and-retail-trade",
            "hotels-and-restaurants",
            "transport-storage-and-communication",
            "financial-intermediation",
            "real-estate-renting-and-business-activities",
            "public-administration-and-defence-compulsory-social-security",
            "education",
            "health-and-social-work",
            "other-community-social-and-personal-service-activities",
            "private-households-with-employed-persons",
        ]
    }

    def get_custom_headers(self):
        return self.CUSTOM_HEADER_MAP.get(self.doc_id, None)
