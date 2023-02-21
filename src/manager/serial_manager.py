import serial
import serial.tools.list_ports
import os

from manager.bridge_manager import BridgeManager
from manager.data_manager import DataManager


class SerialManager:
    def __init__(self, bridge_manager: BridgeManager, data_manager: DataManager, port: str | None = None) -> None:
        self.__s: serial.Serial = None
        self.__port: str = port
        self.__bridge: BridgeManager = bridge_manager
        self.__data_manager: DataManager = data_manager

    def set_port(self, port: str) -> None:
        self.__port = port

    def get_port(self) -> str | None:
        return self.__port
    
    def is_ready(self) -> bool:
        return self.__s != None

    def init_connection(self, port: str | None = None) -> None:
        if (port is not None):
            self.set_port(port)
        
        elif (self.__port is None):
            self.__auto_detect_port()
        
        if (self.__port is not None):
            try:
                self.__s = serial.Serial(self.__port)
                self.__bridge.set_connected(True)
            except:
                pass

    def __auto_detect_port(self) -> bool:
        ports: list = list(serial.tools.list_ports.comports())

        match os.name:
            case "nt":
                for port in ports:
                    if 'COM' in port.description:
                        self.__port = port.name

            case "posix":
                for port in ports:
                    if 'COM' in port.description:
                        self.__port = port.name 
    
    def __send(self, data: str) -> None:
        try:
            self.__s.write(data.encode())
        except:
            pass
            # faire log

    def __read(self) -> str:
        try:
            return self.__s.read_until().decode()[:-1]
        except:
            pass

    def run(self) -> None:
        if (not self.is_ready()):
            self.init_connection()
        
        self.__send("TEST_CONNECTION")
        data: dict = self.__data_manager.convert_data(self.__read())

        self.__bridge.set_data(data)
        
        while (True):

            if (self.__bridge.has_command()):
                self.__send(self.__bridge.get_command())
                self.__bridge.reset_command()
            
            else:
                self.__send("OK")

            data: dict = self.__data_manager.convert_data(self.__read())

            self.__bridge.set_data(data)