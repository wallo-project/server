"""! File containing the bridge manager, its goal is to pass data from the serial server to the REST API
and vice-versa.

@author WALL-O Team
@version 1.0.0
@since 10/01/2023
"""

class BridgeManager:
    """! BridgeManager pass data from the serial server to the REST API
    and vice-versa.

    @author WALL-O Team
    @version 1.0.0
    @since 10/01/2023
    """
    def __init__(self) -> None:
        """! Constructor of the BridgeManager class.
        It inits all the attributes.
        """
        # initialling all the attributes
        self.__command_bridge: str = ""
        self.__data_bridge: dict = {}
        self.__is_connected: bool = False
        self.__command_response: int = 0

    def set_command(self, command: str) -> None:
        """! Method that set the command to send to the Arduino.
        This method is called in the API REST.

        1: start
        2: stop
        3: test connection

        @param command the command to send to the Arduino (should be 1, 2 or 3).
        """
        self.__command_bridge = command

    def set_data(self, data: dict) -> None:
        """! Method that set the data read from the Arduino and formatted.
        This method is called in the Serial server.

        @param data the data to store for the API.
        """
        # set the data
        self.__data_bridge = data
        # if the command response is not 0, store it, it will be retrieved at the next call to the API
        # this ensure that the command output will arrive at the dashboard even if another batch of data is set
        if ((data["commandResponse"] == 1) or (data["commandResponse"] == -1)):
            self.set_command_response(data["commandResponse"])

    def set_connected(self, is_connected) -> None:
        """! Method that set wether the serial server is connected to the Arduino or not.
        This method is called in the Serial server.

        @param is_connected the connection_status to store for the API.
        """
        self.__is_connected = is_connected

    def set_command_response(self, command_response: int) -> None:
        """! Method that set the command response of the Arduino.
        This method is called in the BridgeManager.

        @param command_response the command response to store for the API.
        """
        self.__command_response = command_response

    def is_connected(self) -> bool:
        """! Method that return if the serial manager is connected to the Arduino or not.
        This method is called in the REST API.

        @return a boolean whether the Arduino is connected or not.
        """
        return self.__is_connected

    def get_command(self) -> str:
        """! Method that return the command to send to the Arduino.
        This method is called in the serial server.

        @return a string representing the command.
        """
        return self.__command_bridge
    
    def reset_command(self) -> None:
        """! Method that reset the state of the command bridge.
        """
        self.__command_bridge = ""

    def has_command(self) -> bool:
        """! Method that return if a command is waiting to be sent to the Arduino or not.
        This method is called in the serial server.

        @return a boolean.
        """
        return self.__command_bridge != ""
    
    def get_data(self) -> dict:
        """! Method that return the latest data fetch from the Arduino.
        This method is called in the API Rest.

        @return a dict of all the data from the Arduino.
        """
        return self.__data_bridge
    
    def get_command_response(self) -> int:
        """! Method that returns the command response of the Arduino.
        This method is called in the API. Calling this method also reset the status of the command response.

        @return command_response the command response to store for the API.
        """
        res: int = self.__command_response
        self.__command_response = 0
        return res       
    
