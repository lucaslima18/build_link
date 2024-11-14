from abc import ABC, abstractmethod
from typing import List, Union
from requests import Response

from src.libs.business_rules.schemas import UserMetadata


class UserDataExtractor(ABC):
    """
    A interface of an class to extract data from an URL origin.

    Methods
    ---
    `def extract_data(all_data: Union[List[UserMetadata], List[None]], response: Response) -> Union[List[UserMetadata], List[None]]`
        return all data extracted of an url
    """

    @staticmethod
    @abstractmethod
    def extract_data(
        all_data: Union[List[UserMetadata], List[None]], response: Response
    ) -> Union[List[UserMetadata], List[None]]: ...
