from typing import List
from src.modules.eligible_users.schemas import EligibleUsersResponse
from src.libs.business_rules.schemas import UserMetadata


class EligibleUsersService:
    def __init__(self) -> None: ...

    def get_eligible_user(
        self, data: List[UserMetadata], pageNumber: int, pageSize: int
    ):
        if data != []:
            return EligibleUsersResponse(
                pageNumber=pageNumber,
                pageSize=pageSize,
                totalCount=len(data),
                users=data[pageNumber:pageSize],
            )

        raise Exception
