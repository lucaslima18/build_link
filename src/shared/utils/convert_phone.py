import re
from src.shared.utils.log_handler import LogHandler
from src.shared.enum.phone_country_code import PhoneCountryCode

logger = LogHandler()


def convert_phone(phone_number: str, nationality: str) -> str | None:
    try:
        phone_digits_only = re.sub(r"\D", "", phone_number)
        converted_phone = f"{PhoneCountryCode[nationality].value}{phone_digits_only}"

        return converted_phone

    except Exception as err:
        logger.error(err)
