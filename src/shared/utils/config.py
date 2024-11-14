import os
from typing import List
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel

from src.libs.business_rules.schemas import UserMetadata
from src.shared.utils.parse_list_env import parse_list_env
from src.shared.validators.check_log_level import check_log_level

load_dotenv(find_dotenv())


class GeneralConfig(BaseModel):
    API_TITLE: str = os.getenv("API_TITLE", "Build Link")
    API_PORT: int = int(os.getenv("API_PORT", default=8000))
    API_HOST: str = os.getenv("API_HOST", "localhost")
    API_LOG_LEVEL: str = check_log_level(
        act_log_level=os.getenv("API_LOG_LEVEL", default="info")
    )
    USERS_ORIGINS: List[str] = parse_list_env("USERS_ORIGINS", default=[])
    ALL_USERS_METADATA: List[UserMetadata] | None = []


config = GeneralConfig()
