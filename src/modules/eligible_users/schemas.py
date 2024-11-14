from typing import List
from pydantic import BaseModel

from src.libs.business_rules.schemas import UserMetadata


class EligibleUsersResponse(BaseModel):
    pageNumber: int
    pageSize: int
    totalCount: int
    users: List[UserMetadata]
