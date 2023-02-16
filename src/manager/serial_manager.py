import serial
import serial.tools.list_ports
import os
import time


class SerialManager:
    def __init__(self, port: str | None = None) -> None:
        self.__s: serial.Serial = None
        self.__port: str = port

    def set_port(self, port: str) -> None:
        self.__port = port

    def get_port(self) -> str | None:
        return self.__port

    def init_com(self, port: str | None = None) -> None:
        if (port is not None):
            self.set_port(port)
        
        elif (self.__port is None):
            self.auto_detect_port()
        
        if (self.__port is not None):
            self.__s = serial.Serial(self.__port)

    def auto_detect_port(self) -> bool:
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
        print(data)
        self.__s.write(data.encode("utf-8"))

    def read(self) -> str:
        return self.__s.read_until().decode()[:-2]

    def test(self):
        while(True):
            self.send("ON")
            print(self.read())
            self.send("OFF")
            print(self.read())