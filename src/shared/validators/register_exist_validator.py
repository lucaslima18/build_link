from typing import List, Union
from src.libs.business_rules.schemas import UserMetadata


def register_exist_validator(
    all_data: Union[List[UserMetadata], List[None]], data: UserMetadata | None
) -> bool:
    return True if data in all_data else False
