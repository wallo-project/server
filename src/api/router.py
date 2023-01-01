from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from config import config

router = InferringRouter()

@cbv(router)
class Router:

    @router.get("/")
    def welcome(self) -> str:
        return f"Welcome to the {config.API_NAME} v{config.API_VERSION}"

    # routes for status access
    @router.get("/healthcheck")
    def healthcheck(self) -> dict:
        return {"status": "OK"}

    @router.get("/status")
    def status(self) -> dict:
        return {"connection": True}

    # routes for data access
    @router.get("/get-speeds")
    def get_speeds(self) -> None:
        return None
    
    @router.get("/get-angles")
    def get_angles(self) -> None:
        return None

    @router.get("/get-angles")
    def get_angles(self) -> None:
        return None

    @router.get("/get-latest-data")
    def get_latest_data(self) -> None:
        return None

    @router.get("/get-data-file")
    def get_data_file(self) -> None:
        return None

    # routes to post commands
    @router.post("/command")
    def post_command(self):
        return None

    @router.post("/stop")
    def post_stop(self):
        return None