import serial
import serial.tools.list_ports
import os


class SerialManager:
    def __init__(self, port: str | None = None) -> None:
        self.__s: serial.Serial = None
        self.__port: str = port
        self.__is_connected: bool = True

    def set_port(self, port: str) -> None:
        self.__port = port

    def get_port(self) -> str | None:
        return self.__port
    
    def set_connected(self, is_connected: bool) -> None:
        self.__is_connected = is_connected

    def is_connected(self) -> bool:
        return self.__is_connected
    
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
                self.set_connected(True)
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
    
    def send(self, data: str) -> None:
        try:
            self.__s.write(data.encode("utf-8"))
        except:
            pass
            # faire log

    def read(self) -> str:
        try:
            return self.__s.read_until().decode()[:-1]
        except:
            pass