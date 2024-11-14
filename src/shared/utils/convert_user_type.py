from src.shared.utils.log_handler import LogHandler

logger = LogHandler()


def convert_user_type(lat: float, lon: float) -> str:
    special_areas = [
        {
            "min_lon": -15.411580,
            "min_lat": -46.361899,
            "max_lon": -2.196998,
            "max_lat": -34.276938,
        },
        {
            "min_lon": -23.966413,
            "min_lat": -52.997614,
            "max_lon": -19.766959,
            "max_lat": -44.428305,
        },
    ]

    for area in special_areas:
        if (
            area["min_lon"] <= lon <= area["max_lon"]
            and area["min_lat"] <= lat <= area["max_lat"]
        ):
            return "special"

    standart_area = {
        "min_lon": -34.016466,
        "min_lat": -54.777426,
        "max_lon": -26.155681,
        "max_lat": -46.603598,
    }

    if (
        standart_area["min_lon"] <= lon <= standart_area["max_lon"]
        and standart_area["min_lat"] <= lat <= standart_area["max_lat"]
    ):
        return "standart"

    return "laborious"
