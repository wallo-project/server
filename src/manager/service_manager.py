
from manager.serial_manager import SerialManager

class ServiceManager:
    def __init__(self, serial_manager) -> None:
        self.__serial: SerialManager = serial_manager


    def is_connected(self) -> bool:
        return False

    def send_start(self) -> None:
        self.__serial.write("start")
    
    def send_stop(self) -> None:
        self.__serial.write("stop")
