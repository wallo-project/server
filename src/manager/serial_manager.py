import multiprocessing
import serial
import serial.tools.list_ports
import os
import json


class SerialManager:
    def __init__(self, shared_command_queue: multiprocessing.Queue, shared_data_queue: multiprocessing.Queue, port: str | None = None) -> None:
        self.__s: serial.Serial = None
        self.__port: str = port
        self.__connected: bool = True
        self.__shared_command_queue: multiprocessing.Queue = shared_command_queue
        self.__shared_data_queue: multiprocessing.Queue = shared_data_queue

    def set_port(self, port: str) -> None:
        self.__port = port

    def get_port(self) -> str | None:
        return self.__port

    def init_com(self, port: str | None = None) -> None:
        if (port is not None):
            self.set_port(port)
        
        elif (self.__port is None):
            self.__auto_detect_port()
        
        if (self.__port is not None):
            try:
                self.__s = serial.Serial(self.__port)
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
            self.__s.write(data.encode("utf-8"))
        except:
            pass
            # faire log

    def __read(self) -> str:
        try:
            return self.__s.read_until().decode()[:-1]
        except:
            pass

    def run(self):

        if (not self.__s):
            self.init_com()
        
        self.__send("TEST_CONNECTION")
        data: str = self.__read()
        
        while(self.__connected):

            try:
                command: str = self.__shared_command_queue.get_nowait()
                self.__send(command)
            except:
                self.__send("OK")

            data: str = self.__read()
            
            self.__shared_data_queue.put(data)