import io, csv
from typing import List, Union
from requests import Response
from src.libs.business_rules.schemas import UserMetadata
from src.libs.load_data.user_data_transformer import (
    UserDataTransformCSV,
    UserDataTransformJSON,
)
from src.libs.load_data.interfaces import UserDataExtractorInterface
from src.shared.utils.log_handler import LogHandler

logger = LogHandler()


class UserDataExtractorJSON(UserDataExtractorInterface):
    """
    A class that inherits from UserDataExtractorInterface and implements a
    structure responsible for extract data from a source URL that returned a
    JSON format.

    Methods
    ---
    ```py
    def extract_data(
        all_data: Union[List[UserMetadata], List[None]],
        response: Response
    ) -> Union[List[UserMetadata], List[None]]
    ```
    return all data extracted of an url
    """

    @staticmethod
    def extract_data(
        all_data: Union[List[UserMetadata], List[None]], response: Response
    ) -> Union[List[UserMetadata], List[None]]:
        logger.info("New json content founded! start extraction...")

        json_data = response.json().get("results", [])
        transformed_json_data = UserDataTransformJSON().transform_data(
            all_data=all_data, data_dict=json_data
        )
        return transformed_json_data


class UserDataExtractorCSV(UserDataExtractorInterface):
    """
    A class that inherits from UserDataExtractorInterface and implements a
    structure responsible for extract data from a source URL that returned a
    CSV format.

    Methods
    ---
    ```py
    def extract_data(
        all_data: Union[List[UserMetadata], List[None]],
        response: Response
    ) -> Union[List[UserMetadata], List[None]]
    ```
    return all data extracted of an url
    """

    @staticmethod
    def extract_data(
        all_data: Union[List[UserMetadata], List[None]], response: Response
    ) -> Union[List[UserMetadata], List[None]]:
        logger.info("New csv content founded! start extraction...")

        csv_data = response.content.decode("utf-8-sig")
        csv_reader = csv.DictReader(io.StringIO(csv_data))
        rows = [row for row in csv_reader]
        transformed_rows = UserDataTransformCSV().transform_data(
            all_data=all_data, data_dict=rows
        )

        return transformed_rows
