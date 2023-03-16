"""! File containing the class that manage all the communications with the robot through a serial communication.
The communication is made over Bluetooth port.
    
@author WALL-O Team
@version 1.0.0
@since 15 January 2023
"""

# importing libraries
import serial
import serial.tools.list_ports
import os

from manager.bridge_manager import BridgeManager
from manager.data_manager import DataManager
import logging

class SerialManager:
    """! Class that manage all the communications with the robot through a serial communication.
    The communication is made over Bluetooth port.
    
    @author WALL-O Team
    @version 1.0.0
    @since 15 January 2023
    """
    def __init__(self, bridge_manager: BridgeManager, data_manager: DataManager, port: str | None = None) -> None:
        """! Constructor of the serial manager class.
        This method is called when creating a serial manager object.
        
        @param bridge_manager
        """
        # setup attributes
        self.__s: serial.Serial = None
        self.__port: str = port
        self.__bridge: BridgeManager = bridge_manager
        self.__data_manager: DataManager = data_manager
        self.__ports: list[str] = []

    def set_port(self, port: str) -> None:
        """! Method that set the port to use.
        If this method is not used, the port is automatically defined.

        @param port the port to use.        
        """
        self.__port = port

    def get_port(self) -> str | None:
        """! Method to get the current serial port set to communicate.
        The port allow to establish a serial communication with the Arduino.

        @return the serial port.
        """
        return self.__port
    
    def __reset(self) -> None:
        """! Private method that reset the connection information.
        This include the candidate ports to open a connection.
        """
        self.__ports = []
        self.__port = None
        self.__s = None

    def __load_ports(self) -> None:
        """! Private method to load ports that may connect to the Arduino via a serial
        communication using Bluetooth.
        """

        # get the ports
        ports: list = list(serial.tools.list_ports.comports())

        # depending on the OS, check the ports to connect on
        match os.name:
            case "nt":
                # check for windows
                for port in ports:
                    if 'COM' in port.description:
                        self.__ports.append(port.name)

            case "posix":
                # check for linux
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
        # set the connection status
        self.__bridge.set_connected(False)
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
                    # except there is an exception in the creation of the serial
                    logging.error(f"Error creating a serial communication on port {port}")
        else:
            # else there is a port set for the connection
            try:
                # try to connect
                self.__s = serial.Serial(port=self.__port, timeout=5, write_timeout=10)
                return True
            except:
                logging.error(f"Error creating a serial communication on port {self.__port}")
                return False
        # return by default false, no connection have been established
        return False
    
    def __send(self, data: str) -> None:
        """! Private method to send data to the Arduino through a serial connection.
        This data is encoded in bits to be sent.
        
        @param data a string of data.
        """
        try:
            # try to write data after encoding it
            self.__s.write(data.encode())
        except:
            logging.error("Could not send data to Arduino")

    def __read(self) -> str | None:
        """! Private method to read data from the Arduino through a serial connection.
        This data is decoded. If no value is read when the timeout is read, the method returns None.
        
        @return a string of data or None if no value has been read.
        """
        try:
            # try to return a read and decoded value
            return self.__s.read_until().decode()[:-1]
        except:
            # in case of no value read, return None
            logging.error("Could not read data from Arduino")
            return None

    def run(self) -> None:
        """! Method to run to start the serial server."""

        # set default status of connection
        connected: bool = False
        
        # while not connected try to connect
        while (not connected):
            # set default data for the API
            data: dict = self.__data_manager.convert_data(None)
            self.__bridge.set_data(data)
            # reset the elements of the connection
            self.__reset()
            # init the connection
            connected = self.init_connection()
        
        while (connected):
            # while connected if a command is waiting, send it to the Arduino
            if (self.__bridge.has_command()):
                self.__send(self.__bridge.get_command())
                # then reset the command
                self.__bridge.reset_command()

            # read data from the Arduino
            retrieved_data: str = self.__read()
            # if the data is none, then try to connect again
            if (retrieved_data is None) or (retrieved_data == ''):
                connected = False
                self.run()
            else:
                # else convert and store data 
                data: dict = self.__data_manager.convert_data(retrieved_data)
                self.__bridge.set_data(data)
                self.__data_manager.store_data(data)