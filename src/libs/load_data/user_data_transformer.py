from typing import Dict, List, Union

from src.libs.business_rules.schemas import UserMetadata
from src.shared.validators.register_exist_validator import register_exist_validator
from src.libs.business_rules.business_rules_json import BusinessRulesJSON
from src.shared.utils.log_handler import LogHandler

logger = LogHandler()


class UserDataTransformJSON:

    @staticmethod
    def transform_data(
        all_data: Union[List[UserMetadata], List[None]], data_dict: Dict
    ):
        transformed_data_dict = []

        logger.info("Start data transformation of founded json content...")

        if data_dict:
            for data in data_dict:
                transformed_data = BusinessRulesJSON(data=data).run()

                if register_exist_validator(all_data=all_data, data=transformed_data):
                    logger.warning(f"UserMetadata with email {transformed_data.email}")

                else:
                    transformed_data_dict.append(transformed_data)

            logger.info(
                f"{len(transformed_data_dict)} data are transformed into UserMetadata object..."
            )

            return transformed_data_dict
