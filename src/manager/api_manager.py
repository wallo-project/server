"""! File that contains the web API used to retrieve data from the dashboard.
All the informations are coming from the @see BridgeManager class.

@author WALL-O Team
@version 1.0.0
@since 02 January 2023
"""

# importing elements from modules
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
# importing modules
import uvicorn
# importing config
from config import config

from manager.bridge_manager import BridgeManager

class ApiManager(FastAPI):
    """! Class that contains the API.
    It inherits from FastAPI class.
    
    @author WALL-O Team
    @version 1.0.0
    @since 02 January 2023
    """
    
    def __init__(self, bridge_manager: BridgeManager, filename: str, host: str | None = None, port: int = 8080, allow_origins: list[str] | str = '*', allow_credentials: bool = True, allow_methods: list[str] = ["*"], allow_headers: list[str] = ["*"]) -> None:
        """! Constructor of the class.
        This class contains the API to run.

        @param bridge_manager the manager of services to communicate with Arduino.
        @param filename the file to serve for report.
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

        self.__filename: str = filename

        self.__bridge_manager: BridgeManager = bridge_manager

        # setting routes related to the API status
        self.add_api_route('/', self.__get_welcome)

        # status of the API
        self.add_api_route('/healthcheck', self.__get_healthcheck)
        self.add_api_route('/status', self.__get_status)
        # setting routes to send data to the Arduino
        self.add_api_route('/command/start', self.__post_start, methods=["POST", "GET"])
        self.add_api_route("/command/stop", self.__post_stop, methods=["POST", "GET"])
        self.add_api_route('/command/enable-line-track', self.__post_line_track_enable, methods=["POST", "GET"])
        self.add_api_route('/command/disable-line-track', self.__post_line_track_disable, methods=["POST", "GET"])
        # get data from the Arduino
        self.add_api_route('/latest-data', self.__latest_data, methods=["GET"])
        # serv reports
        self.mount("/reports", StaticFiles(directory="reports"), name="static")
        self.add_api_route("/report", self.__get_report, methods=["GET"])

    async def __get_welcome(self) -> str:
        """! Method that return a welcome message.
        The only purpose is to test the API.
        
        @return string a welcome message.
        """
        return f"Welcome to the {config.API_NAME} v{config.API_VERSION}"

    async def __get_healthcheck(self) -> dict:
        """! Method that return a report on the health of the API.
        
        @return dict health report.
        """
        return {"healthcheck": "OK"}

    async def __get_status(self) -> dict:
        """! Method that return a report on the status of the API.
        It reports the status of the API and the services loading for communications with Arduino.
        
        @return dict status report.
        """
        return {
            "status": "OK",
            "wallo_connection": self.__bridge_manager.is_connected(),
            "services": "SUCCESSFULLY_LOADED"
        }
    
    async def __get_report(self) -> RedirectResponse:
        """! Method that redirect to the file to download.
        This method use the filename passed at the creation of the object.
        
        @return a RedirectResponse object.
        """
        return RedirectResponse(url=f"/reports/{self.__filename}")
    
    async def __latest_data(self) -> dict:
        """! Method get latest data from the Arduino.
        This call the bridge to get the data to send.

        @return a dict of the latest data fetch from the Arduino.
        """
        data: dict = self.__bridge_manager.get_data()
        data["commandResponse"] = self.__bridge_manager.get_command_response()
        return data

    async def __post_start(self) -> dict:
        """! Method to store a start command to pass to the Arduino.
        This call the bridge to store the command to send.

        @return a dict to confirm the storage of the command.
        """
        self.__bridge_manager.set_command("1")
        return {"response": "OK"}


    async def __post_stop(self) -> dict:
        """! Method to store a stop command to pass to the Arduino.
        This call the bridge to store the command to send.

        @return a dict to confirm the storage of the command.
        """
        self.__bridge_manager.set_command("2")
        return {"response": "OK"}
    
    async def __post_line_track_enable(self) -> dict:
        """! Method to store a line track enabled command to pass to the Arduino.
        This call the bridge to store the command to send.

        @return a dict to confirm the storage of the command.
        """
        self.__bridge_manager.set_command("4")
        return {"response": "OK"}
    
    async def __post_line_track_disable(self) -> dict:
        """! Method to store a line track disable command to pass to the Arduino.
        This call the bridge to store the command to send.

        @return a dict to confirm the storage of the command.
        """
        self.__bridge_manager.set_command("5")
        return {"response": "OK"}
    

    def run(self) -> None:
        """! Method to run the API. """
        if (self.__host):
            uvicorn.run(self, host=self.__host, port=self.__port)
        else:
            uvicorn.run(self, port=self.__port)

