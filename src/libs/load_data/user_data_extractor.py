from typing import List, Union
from requests import Response
from src.libs.business_rules.schemas import UserMetadata
from src.libs.load_data.user_data_transformer import UserDataTransformJSON
from src.libs.load_data.interfaces import UserDataExtractor
from src.shared.utils.log_handler import LogHandler

logger = LogHandler()


class UserDataExtractorJSON(UserDataExtractor):

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
