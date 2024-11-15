from abc import ABC, abstractmethod
from typing import Dict, List, Union
from requests import Response

from src.libs.business_rules.schemas import UserMetadata


class UserDataExtractorInterface(ABC):
    """
    A interface of an class to extract eligible user data from an URL origin.

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
    @abstractmethod
    def extract_data(
        all_data: Union[List[UserMetadata], List[None]], response: Response
    ) -> Union[List[UserMetadata], List[None]]: ...


class UserDataTransformInterface(ABC):
    """
    A interface of an class to transform eligible user data from an URL origin

    ```py
    def transform_data(
        all_data: Union[List[UserMetadata], List[None]],
        data_dict: Union[Dict, List[Dict]]
    ): -> Union[List[UserMetadata], List[None]]
    ```
     return all data transofrmed of an url
    """

    @staticmethod
    @abstractmethod
    def transform_data(
        all_data: Union[List[UserMetadata], List[None]],
        data_dict: List[Dict],
    ) -> Union[List[UserMetadata], List[None]]: ...
