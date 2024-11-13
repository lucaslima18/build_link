import uvicorn
from src.libs.load_data.users_etl import UsersETL
from src.shared.utils.config import get_config
from src.libs.api.api_handler import APIHandler
from src.shared.utils.startapp_icon import startapp_icon

config = get_config()


def applicate_rules():
    users = UsersETL(users_origins=config.USERS_ORIGINS)
    users.data_extraction()


def create_app():
    api = APIHandler(
        port=config.API_PORT, host=config.API_HOST, api_title=config.API_TITLE
    )
    startapp_icon()
    return api.get_app()


if __name__ == "__main__":
    applicate_rules()
    uvicorn.run("main:create_app", host="0.0.0.0", port=3000, reload=True, factory=True)
