import multiprocessing
from manager.api_manager import ApiManager

from manager.serial_manager import SerialManager
from manager.bridge_manager import BridgeManager



def main() -> None:

    # setup the services for both api and server
    shared_bridge = multiprocessing.Value('i', BridgeManager()) 

    
    # setup the serial communication with the Arduino
    serial_manager: SerialManager = SerialManager(shared_bridge)

    # setup the API
    api_manager: ApiManager = ApiManager(shared_bridge)

    p1 = multiprocessing.Process(target=serial_manager.run)
    p2 = multiprocessing.Process(target=api_manager.run)

    

if __name__ == '__main__':
    main()