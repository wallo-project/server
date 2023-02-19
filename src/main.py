from threading import Thread
from manager.api_manager import ApiManager


from manager.serial_manager import SerialManager
from manager.bridge_manager import BridgeManager



def main() -> None:

    # setup the services for both api and server
    bridge_manager: BridgeManager = BridgeManager()
    
    # setup the serial communication with the Arduino
    serial_manager: SerialManager = SerialManager(bridge_manager)
    serial_manager.init_com()

    # setup the API
    api_manager: ApiManager = ApiManager(bridge_manager)
    api_thread: Thread = Thread(target=api_manager.run)

    serial_thread: Thread = Thread(target=serial_manager.run)
    serial_thread.start()
    print("hey")
    api_thread.run()
    

if __name__ == '__main__':
    main()