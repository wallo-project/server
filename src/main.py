import multiprocessing
from manager.api_manager import ApiManager
from manager.serial_manager import SerialManager



def main() -> None:

    # setup the services for both api and server
    shared_command_queue = multiprocessing.Queue()
    shared_data_queue = multiprocessing.Queue()
    
    # setup the serial communication with the Arduino
    serial_manager: SerialManager = SerialManager(shared_command_queue, shared_data_queue)
    # setup the API
    api_manager: ApiManager = ApiManager(shared_command_queue, shared_data_queue)

    p1 = multiprocessing.Process(target=serial_manager.run)
    

    p1.start()
    api_manager.run()
    

if __name__ == '__main__':
    main()