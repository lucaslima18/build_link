from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.shared.utils.log_handler import LogHandler


logger: LogHandler = LogHandler()


class APIHandler:
    """
    APIHandler is a wrapper class designed to provide additional control over the FastAPI framework.

    This class facilitates API creation and management by allowing custom routers to be injected and reset, and
    by configuring middleware for cross-origin resource sharing (CORS). It also provides an interface for
    starting the API with specified host and port settings.
    """

    def __init__(
        self,
        port: int = 8000,
        host: str = "localhost",
        api_title: str = "Api",
    ) -> None:
        self.port = port
        self.host = host
        doc_urls = {}
        self.app = FastAPI(**doc_urls, title=api_title)
        self.router = APIRouter()

    def inject_router(self, router: APIRouter) -> None:
        self.router.include_router(router)

    def reset_routers(self):
        for route in self.router.routes:
            logger.info(route)
            self.router.routes.remove(route)

    def get_app(self) -> FastAPI:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.app.include_router(self.router)
        return self.app
