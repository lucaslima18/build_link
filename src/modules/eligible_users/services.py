from typing import List, Union

from src.shared.enum.user_type_enum import UserTypeEnum
from src.modules.eligible_users.ext import (
    EligibleUserTypeInvalid,
    EligibleUsersNotFind,
    LocationInvalid,
)
from src.modules.eligible_users.schemas import EligibleUsersResponse
from src.libs.business_rules.schemas import UserMetadata
from src.shared.utils.convert_user_type import convert_user_type


class EligibleUsersService:
    """
    A service class for retrieving eligible user data based on different filters such as user type and location.

    Methods
    ---
    ```py
    def get_eligible_user(data: List[UserMetadata], pageNumber: int, pageSize: int) -> EligibleUsersResponse
    ```
    Returns a paginated list of eligible users from the provided `data`. If no users are found, raises an `EligibleUsersNotFind` exception.

    ```py
    def get_eligible_user_by_type(userType: str, data: List[UserMetadata], pageNumber: int, pageSize: int) -> EligibleUsersResponse
    ```
    Filters eligible users by the given `userType`. Returns a paginated list of users. If no matching users are found, raises an `EligibleUsersNotFind`
    exception. If the `userType` is invalid, raises an `EligibleUserTypeInvalid` exception.

    ```py
    def get_eligible_user_by_location(
        lat: float, lon: float, data: List[UserMetadata], pageNumber: int, pageSize: int
    ) -> EligibleUsersResponse
    ```
    Filters eligible users based on the `lat` and `lon` location coordinates. Determines the user type based on the location and then calls
    `get_eligible_user_by_type` to retrieve the filtered data. If the coordinates are invalid, raises a `LocationInvalid` exception.
    """

    @staticmethod
    def get_eligible_user(data: List[UserMetadata], pageNumber: int, pageSize: int):
        if data != []:
            return EligibleUsersResponse(
                pageNumber=pageNumber,
                pageSize=pageSize,
                totalCount=len(data),
                users=data[pageNumber:pageSize],
            )

        raise EligibleUsersNotFind("No eligible user are found!")

    @staticmethod
    def get_eligible_user_by_type(
        userType: str, data: List[UserMetadata], pageNumber: int, pageSize: int
    ):
        print("HERE")
        if userType in UserTypeEnum:
            filter_data = [user for user in data if user.user_type == userType][
                pageNumber:pageSize
            ]
            if filter_data:
                return EligibleUsersResponse(
                    pageNumber=pageNumber,
                    pageSize=pageSize,
                    totalCount=len(filter_data),
                    users=filter_data,
                )

            raise EligibleUsersNotFind("No eligible user are found!")

        raise EligibleUserTypeInvalid(
            f"The userType {userType} is not valid! try one of this types: standart, special, laborious"
        )

    @staticmethod
    def get_eligible_user_by_location(
        lat: Union[float, None],
        lon: Union[float, None],
        data: List[UserMetadata],
        pageNumber: int,
        pageSize: int,
    ):
        if lat and lon:
            user_type = convert_user_type(lat=lat, lon=lon)

            return EligibleUsersService.get_eligible_user_by_type(
                userType=user_type, data=data, pageNumber=pageNumber, pageSize=pageSize
            )

        raise LocationInvalid("the query params lat and lon must be valid float values")
