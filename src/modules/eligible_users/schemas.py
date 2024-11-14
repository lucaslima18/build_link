from typing import List
from pydantic import BaseModel

from src.libs.business_rules.schemas import UserMetadata


class EligibleUsersResponse(BaseModel):
    """
    Default response from eligible users endpoints
    """

    pageNumber: int
    pageSize: int
    totalCount: int
    users: List[UserMetadata]
