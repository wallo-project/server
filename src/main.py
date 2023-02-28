import threading
from manager.api_manager import ApiManager
from manager.serial_manager import SerialManager
from manager.bridge_manager import BridgeManager
from manager.data_manager import DataManager



def main() -> None:
    bridge_manager: BridgeManager = BridgeManager()

    data_manager: DataManager = DataManager()

    data_manager.init_file()

    # setup the serial communication with the Arduino
    serial_manager: SerialManager = SerialManager(bridge_manager, data_manager)
    # setup the main Server
    api_manager: ApiManager = ApiManager(bridge_manager, data_manager.get_filename())

    serial_thread = threading.Thread(target=serial_manager.run)

    serial_thread.start()

    api_manager.run()
    
if __name__ == '__main__':
    main()