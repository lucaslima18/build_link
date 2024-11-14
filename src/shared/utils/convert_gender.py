from src.shared.ext import InvalidGenderException
from src.shared.utils.log_handler import LogHandler

logger = LogHandler()


def convert_gender(gender: str) -> str | None:
    try:
        gender = gender.lower()

        if gender == "female":
            return "f"

        elif gender == "male":
            return "m"

        else:
            raise InvalidGenderException

    except Exception as err:
        logger.error(err)
