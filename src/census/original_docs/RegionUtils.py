from utils_future import Log

log = Log("RegionUtils")


class RegionUtils:
    REGION_NAME_TO_ID = {
        "Sri Lanka": "LK",
        #
        "Colombo": "LK-11",
        "Gampaha": "LK-12",
        "Kalutara": "LK-13",
        #
        "Kandy": "LK-21",
        "Matale": "LK-22",
        "Nuwara Eliya": "LK-23",
        #
        "Galle": "LK-31",
        "Matara": "LK-32",
        "Hambantota": "LK-33",
        #
        "Jaffna": "LK-41",
        "Kilinochchi": "LK-42",
        "Mannar": "LK-43",
        "Vavuniya": "LK-44",
        "Mullaitivu": "LK-45",
        #
        "Batticaloa": "LK-51",
        "Ampara": "LK-52",
        "Trincomalee": "LK-53",
        #
        "Kurunegala": "LK-61",
        "Puttalam": "LK-62",
        #
        "Anuradhapura": "LK-71",
        "Polonnaruwa": "LK-72",
        #
        "Badulla": "LK-81",
        "Moneragala": "LK-82",
        #
        "Ratnapura": "LK-91",
        "Kegalle": "LK-92",
    }

    @staticmethod
    def parse(region_str):
        if "Total" in region_str:
            return "total", "District-Total"

        for (
            district_name,
            district_id,
        ) in RegionUtils.REGION_NAME_TO_ID.items():
            if district_name in region_str:
                return district_id, district_name

        log.warning(f"Could not parse region from {region_str}")
        return None, None
