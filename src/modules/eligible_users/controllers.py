from typing import Optional
from fastapi import APIRouter, Query, Request, HTTPException

from src.modules.eligible_users.schemas import EligibleUsersResponse
from src.modules.eligible_users.ext import (
    EligibleUserTypeInvalid,
    EligibleUsersNotFind,
    LocationInvalid,
)
from src.modules.eligible_users.services import EligibleUsersService
from src.shared.utils.log_handler import LogHandler

logger = LogHandler()


class EligibleUsers:
    """
    A class to define routes for retrieving eligible user data based on various filters such as user type and location.

    Attributes
    ---
    - `prefix` (str): The API version prefix for the routes.
    - `router` (APIRouter): The FastAPI router to handle requests for eligible users.

    Methods
    ---
    ```py
    def get_eligible_users(
        request: Request,
        pageNumber: int = Query(default=0, ge=0),
        pageSize: int = Query(default=100, gt=0),
        userType: Optional[str] = Query(default=None),
        lat: Optional[float] = Query(default=None),
        lon: Optional[float] = Query(default=None)
    ) -> EligibleUsersResponse
    ```
    Handles the GET request for eligible users. Filters users based on the `userType`, `lat`, and `lon` parameters.
    Returns a paginated list of eligible users. If no users are found or if invalid parameters are provided, appropriate exceptions are raised.

    Exceptions handled:
    - `EligibleUserTypeInvalid`: Raised if the provided user type is invalid.
    - `LocationInvalid`: Raised if the latitude or longitude values are invalid.
    - `EligibleUsersNotFind`: Raised if no eligible users are found based on the provided filters.
    """

    prefix = "api/v1"
    router = APIRouter(prefix=f"/{prefix}")

    @router.get("/users", response_model=EligibleUsersResponse)
    def get_eligible_users(
        request: Request,
        pageNumber: int = Query(default=0, ge=0),
        pageSize: int = Query(default=100, gt=0),
        userType: Optional[str] = Query(default=None),
        lat: Optional[float] = Query(default=None),
        lon: Optional[float] = Query(default=None),
    ):
        try:
            service = EligibleUsersService()
            data = request.app.state.all_users_metadata
            logger.info(userType)
            if userType:
                return service.get_eligible_user_by_type(
                    userType=userType,
                    pageNumber=pageNumber,
                    pageSize=pageSize,
                    data=data,
                )

            if lat or lon:
                return service.get_eligible_user_by_location(
                    lat=lat,
                    lon=lon,
                    pageNumber=pageNumber,
                    pageSize=pageSize,
                    data=data,
                )
            return service.get_eligible_user(
                pageNumber=pageNumber, pageSize=pageSize, data=data
            )

        except EligibleUserTypeInvalid as err:
            logger.error(str(err.args[0]))
            raise HTTPException(status_code=400, detail=str(err.args[0]))

        except LocationInvalid as err:
            logger.error(str(err.args[0]))
            raise HTTPException(status_code=400, detail=str(err.args[0]))

        except EligibleUsersNotFind as err:
            logger.error(str(err.args[0]))
            raise HTTPException(status_code=404, detail=str(err.args[0]))
