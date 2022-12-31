from fastapi_utils import inferring_router
from fastapi_utils import cbv

from api.service import Service
"""
router = inferring_router()

@cbv(router)
class Router:
    def __init__(self) -> None:
        self.__services = Service()

    @router.get("/get-data")
    def __get_data(self):
        return self.__services.get_data()

    @router.get("/get-latest-data")
    def __get_latest_data(self):
        pass

"""