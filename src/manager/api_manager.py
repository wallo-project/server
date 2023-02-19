"""! File that contains the web API used to retrieve data from the dashboard.
All the informations are coming from the ServiceManager class.

@author WALL-O Dev Team
@version 0.0.1
@since 02 January 2023
"""

# importing elements from modules
import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# importing modules
import uvicorn

# importing the service management
from manager.bridge_manager import BridgeManager

# importing config
from config import config

class ApiManager(FastAPI):
    """! Class that contains the API.
    It inherits from FastAPI class.

    TODO : complete documentation
    
    @author WALL-O Dev Team
    @version 0.0.1
    @since 02 January 2023
    """
    
    def __init__(self, bridge_manager: BridgeManager, host: str | None = None, port: int = 8080, allow_origins: list[str] = ['*'], allow_credentials: bool = True, allow_methods: list[str] = ["*"], allow_headers: list[str] = ["*"]) -> None:
        """! Constructor of the class.
        This class contains the API to run.

        @param service_manager the manager of services to communicate with Arduino.
        @param host the host IP address of the API (optional).
        @param port the port of the API (optional).
        @param allow_origins the allowed origins of the incoming requests. Default: all (optional).
        @param allow_credentials wether the credential system should be enabled or not by the API. Default: True (optional).
        @param allow_methods methods allowed by the API. Default: all (optional).
        @param allow_headers headers allowed by the API. Default: all (optional).
        """
        # init the super method
        super().__init__()

        # add the middleware configuration
        self.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=allow_credentials,
            allow_methods=allow_methods,
            allow_headers=allow_headers,
        )

        # setting up the informations to run the API
        self.__host: str | None = host
        self.__port: int = port

        # setting the manager to communicate with Arduino
        self.__bridge: BridgeManager = bridge_manager

        # setting routes related to the API status
        self.add_api_route('/', self.__get_welcome)

        # setting routes to get data from the robot
        self.add_api_route('/status', self.__get_status)

        # setting routes to send data to the robot
        self.add_api_route('/command/start', self.__post_start, methods=["POST", "GET"])
        self.add_api_route("/command/stop", self.__post_stop, methods=["POST", "GET"])

    def __get_welcome(self) -> str:
        """! Method that return a welcome message.
        The only purpose is to test the API.
        
        @return string a welcome message.
        """
        return f"Welcome to the {config.API_NAME} v{config.API_VERSION}"

    def __get_status(self) -> dict:
        """! Method that return a report on the health of the API.
        The health report the status of the API and the services loading for communications with Arduino.
        
        @return dict health report.
        """
        return {
            "status": "OK",
            "wall-o connected": self.__bridge.is_connected(),
            "services": "successfully loaded"
            }

    # routes to post commands
    def __post_start(self) -> str:
        self.__bridge.store_command("START")
        return {"response": "OK"}

    def __post_stop(self) -> str:
        self.__bridge.store_command("STOP")
        return {"response": "OK"}


    def run(self) -> None:
        if (self.__host):
            uvicorn.run(self, host=self.__host, port=self.__port)
        else:
            uvicorn.run(self, port=self.__port)

