class BridgeManager:
    def __init__(self) -> None:
        self.__command: str = ""
        self.__data: str = ""
        self.__is_connected: bool = False

    def get_command(self) -> str:
        return self.__command
    
    def is_connected(self) -> bool:
        return self.__is_connected
    
    def set_connection(self, is_connected: bool) -> None:
        self.__is_connected = is_connected
    
    def get_data(self) -> str:
        return self.__data
    
    def store_data(self, command: str) -> None:
        self.__command = command

    def store_command(self, data: str) -> None:
        self.__data = data