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
from manager.service_manager import ServiceManager

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
    
    def __init__(self, service_manager: ServiceManager, host: str | None = None, port: int = 8080, allow_origins: list[str] = ['*'], allow_credentials: bool = True, allow_methods: list[str] = ["*"], allow_headers: list[str] = ["*"]) -> None:
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
        self.__manager: ServiceManager = service_manager

        # setting routes related to the API status
        self.add_api_route('/', self.__get_welcome)
        self.add_api_route('/healthcheck', self.__get_healthcheck)

        # setting routes to get data from the robot
        self.add_websocket_route('/status', self.__get_status)
        self.add_websocket_route('/data/download', self.__get_data_file)
        self.add_websocket_route('/data/latest', self.__get_latest_data)
        self.add_websocket_route('/data/speeds', self.__get_speeds)
        self.add_websocket_route('/data/angles', self.__get_angles)

        # setting routes to send data to the robot
        self.add_api_route('/command/{command}', self.__post_command, methods=["GET", "POST"])
        self.add_api_route("/command/stop", self.__post_stop, methods=["GET", "POST"])

    def __get_welcome(self) -> str:
        """! Method that return a welcome message.
        The only purpose is to test the API.
        
        @return string a welcome message.
        """
        return f"Welcome to the {config.API_NAME} v{config.API_VERSION}"

    def __get_healthcheck(self) -> dict:
        """! Method that return a report on the health of the API.
        The health report the status of the API and the services loading for communications with Arduino.
        
        @return dict health report.
        """
        return {
            "status": "OK", 
            "services": "successfully loaded"
            }

    def __get_status(self) -> dict:
        """! Method that return the status of the connection with the Robot.
        The health report the status of the API and the services loading for communications with Arduino.
        
        @return dict health report.
        """
        return {"connection": self.__manager.is_connected()}

    # routes for data access
    def __get_speeds(self) -> dict[str, list[float]]:
        return {"speeds": []}
    
    def __get_angles(self) -> dict[str, list[float]]:
        return {"angles": []}

    def __get_latest_data(self) -> dict:
        return {"speed": 0.0, "angle": 0.0, "timestamp": datetime.datetime.now()}

    def __get_data_file(self) -> None:
        return None

    # routes to post commands
    def __post_command(self, command: str) -> str:
        if (command.upper() == "START"):
            self.__manager.send_start()
        else:
            self.__manager.send_stop()
        return "OK"

    def __post_stop(self) -> str:
        return "OK"


    def run(self) -> None:
        if (self.__host):
            uvicorn.run(self, host=self.__host, port=self.__port)
        else:
            uvicorn.run(self, port=self.__port)

