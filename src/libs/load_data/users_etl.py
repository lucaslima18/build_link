import io, csv
from typing import Dict, List
import requests

from src.libs.load_data.user_data_extractor import UserDataExtractorJSON
from src.libs.business_rules.business_rules_csv import BusinessRulesCSV
from src.libs.business_rules.business_rules_json import BusinessRulesJSON
from src.libs.business_rules.schemas import UserMetadata

from src.libs.load_data.ext import TransformationDataIsNull, UnsupportedContent
from src.shared.utils.log_handler import LogHandler

logger = LogHandler()


class UsersETL:
    def __init__(self, users_origins: List[str] = []) -> None:
        self.users_origins = users_origins
        self.all_data = []

    def run(self):
        self.data_extraction()

    def data_extraction(self) -> List[UserMetadata] | None:
        logger.info("Start ETL proccess of Users informations...")
        logger.info(f"searching for {self.users_origins} urls...")
        for url in self.users_origins:
            try:
                logger.info(f"Start consume {url} route...")
                response = requests.get(url)
                content_type = response.headers.get("content-type", "")

                if "application/json" in content_type:
                    transformed_json_data = UserDataExtractorJSON().extract_data(
                        all_data=self.all_data, response=response
                    )

                    self.all_data.extend(transformed_json_data)

                    logger.info(
                        f"{len(transformed_json_data)} New json content added to cache..."
                    )

                elif "text/csv" in content_type or url.endswith(".csv"):
                    logger.info("New csv content founded! start extraction...")

                    csv_data = response.content.decode("utf-8-sig")
                    csv_reader = csv.DictReader(io.StringIO(csv_data))
                    rows = [row for row in csv_reader]
                    transformed_rows = self.data_transform_csv(
                        data_dict=rows, url=url, content_type=content_type
                    )
                    self.all_data.extend(transformed_rows)

                    logger.info(
                        f"{len(transformed_rows)} New csv content added to cache..."
                    )

                else:
                    raise UnsupportedContent(f"not supported content to url: {url}")

            except Exception as err:
                logger.error(err)

        logger.info(f"{len(self.all_data)} UserMetadata in cache...")
        return self.all_data

    def data_transform_json(
        self, data_dict: List[Dict], url: str, content_type: str
    ) -> List[UserMetadata]:
        transformed_data_dict = []

        logger.info("Start data transformation of founded json content...")

        if data_dict:
            for data in data_dict:
                transformed_data = BusinessRulesJSON(data=data).run()

                if self.register_exist(data=transformed_data):
                    logger.warning(f"UserMetadata with email {transformed_data.email}")

                else:
                    transformed_data_dict.append(transformed_data)

            logger.info(
                f"{len(transformed_data_dict)} data are transformed into UserMetadata object..."
            )

            return transformed_data_dict

        raise TransformationDataIsNull(f"Have no data to transform for {url}")

    def data_transform_csv(
        self, data_dict: List[Dict], url: str, content_type: str
    ) -> List[UserMetadata]:
        transformed_data_dict = []

        logger.info("Start data transformation of founded csv content...")

        if data_dict:
            for data in data_dict:
                transformed_data = BusinessRulesCSV(data=data).run()

                if self.register_exist(data=transformed_data):
                    logger.warning(f"UserMetadata with email {transformed_data.email}")

                else:
                    transformed_data_dict.append(transformed_data)

            logger.info(
                f"{len(transformed_data_dict)} data are tranformed into UserMetadata object..."
            )

            return transformed_data_dict

        raise TransformationDataIsNull(f"Have no data to transform for {url}")

    def register_exist(self, data: UserMetadata | None) -> bool:
        return True if data in self.all_data else False
