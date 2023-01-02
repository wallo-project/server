from threading import Thread
from manager.api_manager import ApiManager


from manager.serial_manager import SerialManager
from manager.service_manager import ServiceManager



def main() -> None:
    
    # setup the serial communication with the Arduino
    serial_manager: SerialManager = SerialManager()
    serial_manager.connect()

    # setup the services for both api and server
    service_manager: ServiceManager = ServiceManager(serial_manager)

    # setup the API
    api: ApiManager = ApiManager(service_manager)
    api_thread: Thread = Thread(target=api.run)


    #network_server_thread: Thread = Thread()

    api_thread.run()

if __name__ == '__main__':
    main()