"""! File that contains the web API used to retrieve data from the dashboard.
All the informations are coming from the ServiceManager class.

@author WALL-O Dev Team
@version 0.0.1
@since 02 January 2023
"""

# importing elements from modules
import json
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# importing modules
import uvicorn
# importing config
from config import config

from manager.serial_manager import SerialManager

class ServerManager(FastAPI):
    """! Class that contains the API.
    It inherits from FastAPI class.

    TODO : complete documentation
    
    @author WALL-O Dev Team
    @version 0.0.1
    @since 02 January 2023
    """
    
    def __init__(self, serial_manager: SerialManager, host: str | None = None, port: int = 8080, allow_origins: list[str] = ['*'], allow_credentials: bool = True, allow_methods: list[str] = ["*"], allow_headers: list[str] = ["*"]) -> None:
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

        self.__serial_manager: SerialManager = serial_manager
        self.__command: str = ""
        self.__data: dict = {}

        # setting routes related to the API status
        self.add_api_route('/', self.__get_welcome)

        self.add_api_route('/healthcheck', self.__get_status)
        # setting routes to get data from the robot
        self.add_api_route('/status', self.__get_status)
        # setting routes to send data to the robot
        self.add_api_route('/command/start', self.__post_start, methods=["POST", "GET"])
        self.add_api_route("/command/stop", self.__post_stop, methods=["POST", "GET"])

        self.add_api_route('/latest-data', self.__latest_data, methods=["GET"])

    async def __get_welcome(self) -> str:
        """! Method that return a welcome message.
        The only purpose is to test the API.
        
        @return string a welcome message.
        """
        return f"Welcome to the {config.API_NAME} v{config.API_VERSION}"

    async def __get_status(self) -> dict:
        """! Method that return a report on the health of the API.
        The health report the status of the API and the services loading for communications with Arduino.
        
        @return dict health report.
        """
        return {
            "status": "OK",
            "wall-o connected": self.__serial_manager.is_connected(),
            "services": "SUCCESSFULLY_LOADED"
        }
    
    async def __latest_data(self) -> dict:
        return self.__data

    # routes to post commands
    async def __post_start(self) -> dict:
        self.__command = "START"
        return {"response": "OK"}

    async def __post_stop(self) -> dict:
        self.__command = "STOP"
        return {"response": "OK"}
    

    def serial_server(self) -> None:

        if (not self.__serial_manager.is_ready()):
            self.__serial_manager.init_connection()
            print("init")
        
        self.__serial_manager.send("TEST_CONNECTION")
        self.__data: str = self.__serial_manager.read()
        
        while (True):

            if (self.__command != ""):
                self.__serial_manager.send(self.__command)
                self.__command == ""
            else:
                self.__serial_manager.send("OK")

            self.__data: str = json.loads(self.__serial_manager.read())


    def run(self) -> None:
        threading.Thread(target=self.serial_server).start()
        if (self.__host):
            uvicorn.run(self, host=self.__host, port=self.__port)
        else:
            uvicorn.run(self, port=self.__port)

