from manager.server_manager import ServerManager
from manager.serial_manager import SerialManager



def main() -> None:
    # setup the serial communication with the Arduino
    serial_manager: SerialManager = SerialManager()
    # setup the main Server
    server: ServerManager = ServerManager(serial_manager)

    server.run()
    
if __name__ == '__main__':
    main()