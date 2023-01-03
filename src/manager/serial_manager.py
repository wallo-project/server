import serial
import serial.tools.list_ports


class SerialManager:
    def __init__(self) -> None:
        self.__serial: serial.Serial = None

    def connect(self, baud: int = 9600, port: str = None) -> None:
        # Get a list of all available serial ports
        ports = serial.tools.list_ports.comports()

        # Iterate over the available ports
        for port, desc, hwid in ports:
            print(desc)
            # Check if the port is an Arduino
            if 'Arduino' in desc or 'USB Serial Port' in desc:
                self.__serial = serial.Serial(port, baud)
    
    def disconnect(self) -> None:
        self.__serial.close()

    def write(self, data: str) -> None:
        self.__serial.write(f"{data}\n".encode('utf8'))

    def read(self) -> str:
        data: bytes = self.__serial.readline()
        decoded_data: str = data.decode('utf8')
        
        if decoded_data.endswith('\n'):
            decoded_data = decoded_data[:-2]
        
        return decoded_data