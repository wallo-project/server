import serial
import serial.tools.list_ports
import os

from manager.bridge_manager import BridgeManager
from manager.data_manager import DataManager
import logging

class SerialManager:
    def __init__(self, bridge_manager: BridgeManager, data_manager: DataManager, port: str | None = None) -> None:
        self.__s: serial.Serial = None
        self.__port: str = port
        self.__bridge: BridgeManager = bridge_manager
        self.__data_manager: DataManager = data_manager
        self.__ports: list[str] = []

    def set_port(self, port: str) -> None:
        self.__port = port

    def get_port(self) -> str | None:
        return self.__port
    
    def __reset(self) -> None:
        self.__ports = []
        self.__port = None
        self.__s = None

    def __load_ports(self) -> None:
        
        ports: list = list(serial.tools.list_ports.comports())

        match os.name:
            case "nt":
                for port in ports:
                    if 'COM' in port.description:
                        self.__ports.append(port.name)

            case "posix":
                for port in ports:
                    if 'COM' in port.description:
                        self.__ports.append(port.name)

    def init_connection(self) -> bool:
        """! Method that init the connection with the Bluetooth module.
        This method has two working mode. The first one is automated, 
        it automatically select the right port to communicate on.
        You can also use the setter for the port to select it manually.

        @return a boolean that indicate if the connection is successfully initiated or not.
        """
        # checking if the serial port is already defined or not
        if (self.__port is None):
            # in case the port is not loaded, fetch all port likely to be opened
            self.__load_ports()
            for port in self.__ports:
                # for each port, try to open the serial communication
                try:
                    logging.info(f"Attempting connection on port {port}")
                    self.__s = serial.Serial(port=port, timeout=3, write_timeout=3)
                    # send a test message
                    self.__send('3')
                    # result of the read
                    res = self.__read()
                    
                    if ((res is not None) and (res != '')):
                        # if the result is not empty, it means that the connection is established
                        # set the connection status to true
                        self.__bridge.set_connected(True)
                        # set the port
                        self.__port = port
                        logging.info(f"Connected on port {port}")
                        # return true, the connection is initiated
                        return True
                
                except:
                    pass
        else:

            try:
                self.__s = serial.Serial(port=self.__port, timeout=5, write_timeout=10)
                return True
            except:
                return False
        
        return False
    
    def __send(self, data: str) -> None:
        try:
            self.__s.write(data.encode())
        except:
            logging.error("Could not send data to Arduino")

    def __read(self) -> str | None:
        try:
            return self.__s.read_until().decode()[:-1]
        except:
            logging.error("Could not read data from Arduino")
            return None

    def run(self) -> None:
        connected: bool = False
        while (not connected):
            self.__reset()
            connected = self.init_connection()
        
        while (True):
            
            if (self.__bridge.has_command()):
                self.__send(self.__bridge.get_command())
                self.__bridge.reset_command()

            data: dict = self.__data_manager.convert_data(self.__read())
            self.__bridge.set_data(data)
            self.__data_manager.store_data(data)