import io, csv
from typing import Dict, List
import requests

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

    def data_extraction(self):
        all_data = []
        logger.info("Start ETL proccess of Users informations...")
        logger.info(f"searching for {self.users_origins} urls...")
        for url in self.users_origins:
            try:
                response = requests.get(url)
                content_type = response.headers.get("content-type", "")

                if "application/json" in content_type:
                    json_data = response.json().get("results", [])
                    transformed_json_data = self.data_transform_json(
                        data_dict=json_data, url=url, content_type=content_type
                    )
                    self.all_data.extend(transformed_json_data)

                elif "text/csv" in content_type or url.endswith(".csv"):
                    csv_data = response.content.decode("utf-8-sig")
                    csv_reader = csv.DictReader(io.StringIO(csv_data))
                    rows = [row for row in csv_reader]
                    # transformed_rows = self.data_transform(
                    #     data_dict=rows, url=url, data_type=content_type
                    # )
                    all_data.extend(rows)
                else:
                    raise UnsupportedContent(f"not supported content to url: {url}")

            except Exception as err:
                logger.error(err)

    def data_transform_json(
        self, data_dict: Dict, url: str, content_type: str
    ) -> List[UserMetadata]:
        transformed_data_dict = []

        if data_dict:
            for data in data_dict:
                transformed_data_dict.append(
                    BusinessRulesJSON(data=data, content_type=content_type).run()
                )

            return transformed_data_dict

        raise TransformationDataIsNull(f"Have no data to transform for {url}")

    def data_transform_csv(
        self, data_dict: Dict, url: str, content_type: str
    ) -> UserMetadata: ...

    def test(self):
        response = requests.get(url=config.USERS_ORIGINS[1])
        print(response.json())
