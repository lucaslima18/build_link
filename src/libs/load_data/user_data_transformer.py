from typing import Dict, List, Union

from src.libs.business_rules.business_rules_csv import BusinessRulesCSV
from src.libs.load_data.interfaces import UserDataTransformInterface
from src.libs.business_rules.schemas import UserMetadata
from src.shared.validators.register_exist_validator import register_exist_validator
from src.libs.business_rules.business_rules_json import BusinessRulesJSON
from src.shared.utils.log_handler import LogHandler

logger = LogHandler()


class UserDataTransformJSON(UserDataTransformInterface):
    """
    A class that inherits from UserDataTransformInterface and implements a
    structure responsible for transforming data from a source URL that returned
    a JSON format

    Methods
    ---
    ```py
    def transform_data(
        all_data: Union[List[UserMetadata], List[None]],
        data_dict: Dict
    ): -> Union[List[UserMetadata], List[None]]
    ```
    return all data transofrmed of an url
    """

    @staticmethod
    def transform_data(
        all_data: Union[List[UserMetadata], List[None]],
        data_dict: List[Dict],
    ) -> Union[List[UserMetadata], List[None]]:
        transformed_data_dict = []

        logger.info("Start data transformation of founded json content...")

        if data_dict:
            for data in data_dict:
                transformed_data = BusinessRulesJSON(data=data).run()

                if register_exist_validator(all_data=all_data, data=transformed_data):
                    logger.warning(
                        f"UserMetadata with email {transformed_data.email} already exist!... Skipping register..."
                    )

                else:
                    transformed_data_dict.append(transformed_data)

            logger.info(
                f"{len(transformed_data_dict)} data are transformed into UserMetadata object..."
            )

            return transformed_data_dict

        return []


class UserDataTransformCSV(UserDataTransformInterface):
    """
    A class that inherits from UserDataTransformInterface and implements a
    structure responsible for transforming data from a source URL that returned
    a CSV format

    Methods
    ---
    ```py
    def transform_data(
        all_data: Union[List[UserMetadata], List[None]],
        data_dict: Dict
    ): -> Union[List[UserMetadata], List[None]]
    ```
    return all data transofrmed of an url
    """

    @staticmethod
    def transform_data(
        all_data: Union[List[UserMetadata], List[None]],
        data_dict: List[Dict],
    ) -> Union[List[UserMetadata], List[None]]:
        transformed_data_dict = []

        logger.info("Start data transformation of founded json content...")

        if data_dict:
            for data in data_dict:
                transformed_data = BusinessRulesCSV(data=data).run()

                if register_exist_validator(all_data=all_data, data=transformed_data):
                    logger.warning(
                        f"UserMetadata with email {transformed_data.email} already exist!... Skipping register..."
                    )

                else:
                    transformed_data_dict.append(transformed_data)

            logger.info(
                f"{len(transformed_data_dict)} data are transformed into UserMetadata object..."
            )

            return transformed_data_dict

        return []
