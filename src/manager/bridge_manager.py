# TODO: CREATE BRIDGE FOR COMMAND RESPONSE
class BridgeManager:
    def __init__(self) -> None:
        self.__command_bridge: str = ""
        self.__data_bridge: dict = {}
        self.__is_connected: bool = False

    def set_command(self, command: str) -> None:
        self.__command_bridge = command

    def set_data(self, data: dict) -> None:
        self.__data_bridge = data

    def set_connected(self, is_connected) -> None:
        self.__is_connected = is_connected

    def is_connected(self) -> bool:
        return self.__is_connected

    def get_command(self) -> str:
        return self.__command_bridge
    
    def reset_command(self) -> None:
        self.__command_bridge = ""

    def has_command(self) -> bool:
        return self.__command_bridge != ""
    
    def get_data(self) -> dict:
        return self.__data_bridge
    
