from fastapi import APIRouter, Query, Request

from src.modules.eligible_users.services import EligibleUsersService
from src.shared.utils.log_handler import LogHandler
from src.shared.utils.config import config


logger = LogHandler()


class EligibleUsers:

    prefix = "api/v1"
    router = APIRouter(prefix=f"/{prefix}")

    @router.get("/users")
    def get_eligible_users(
        request: Request,
        pageNumber: int = Query(default=0, ge=0),
        pageSize: int = Query(default=100, gt=0),
    ):

        return EligibleUsersService().get_eligible_user(
            pageNumber=pageNumber,
            pageSize=pageSize,
            data=request.app.state.all_users_metadata,
        )
