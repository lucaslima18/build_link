import requests
from typing import List, Union

from src.libs.load_data.user_data_extractor import (
    UserDataExtractorCSV,
    UserDataExtractorJSON,
)
from src.libs.business_rules.schemas import UserMetadata
from src.libs.load_data.ext import UnsupportedContent
from src.shared.utils.log_handler import LogHandler

logger = LogHandler()


class UsersETL:
    """
    A class for performing the ETL (Extract, Transform, Load) process on eligible user data from various URL sources.

    Attributes
    ---
    ```
    - users_origins (List[str]): List of URLs to extract user data from.
    - all_data (List[UserMetadata]): List to store all transformed user data.
    ```
    Methods
    ---
    ```py
    def data_extraction() -> Union[List[UserMetadata], None]
    ```
    Executes the ETL process by consuming each URL in `users_origins`, determining its content type, and using the appropriate extractor to process
    data. Unsupported content types raise an exception. Returns a list of transformed user data or `None` if an error occurs.
    """

    def __init__(self, users_origins: List[str] = []) -> None:
        self.users_origins = users_origins
        self.all_data = []

    def data_extraction(self) -> Union[List[UserMetadata], None]:
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
                    transformed_rows = UserDataExtractorCSV().extract_data(
                        all_data=self.all_data, response=response
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
