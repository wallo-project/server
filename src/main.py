"""! File containing the main function to run.
This function creates and start the server.

@author WALL-O Team
@version 1.1.0
@since 15 January 2023
"""

# import libs
import threading
import webbrowser

from config import config
from manager.api_manager import ApiManager
from manager.serial_manager import SerialManager
from manager.bridge_manager import BridgeManager
from manager.data_manager import DataManager

def main() -> None:
    """! Main function to execute to run the server."""
    bridge_manager: BridgeManager = BridgeManager()

    data_manager: DataManager = DataManager()

    data_manager.init_file()

    # setup the serial communication with the Arduino
    serial_manager: SerialManager = SerialManager(bridge_manager, data_manager)
    # setup the main Server
    api_manager: ApiManager = ApiManager(bridge_manager, data_manager.get_filename())

    serial_thread = threading.Thread(target=serial_manager.run)

    # run the serial manager
    serial_thread.start()
    
    # open the dashboard
    webbrowser.open(config.DASHBOARD_URL)

    # run the API
    api_manager.run()
    
if __name__ == '__main__':
    # if the file is executed, run the main function
    main()