import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.libs.load_data.users_etl import UsersETL
from src.shared.utils.config import config
from src.shared.utils.startapp_icon import startapp_icon
from src.modules.eligible_users.controllers import EligibleUsers


def applicate_rules():
    users_metadata = UsersETL(users_origins=config.USERS_ORIGINS).data_extraction()
    return users_metadata


def create_app():
    api = FastAPI(title=config.API_TITLE)
    api.state.all_users_metadata = applicate_rules()
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    api.router.include_router(EligibleUsers.router)

    startapp_icon()
    return api


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True,
        factory=True,
    )
