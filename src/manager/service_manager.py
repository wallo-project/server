from data.connection import ConnectionData
from manager.serial_manager import SerialManager
from uuid import uuid1, UUID

class ServiceManager:
    def __init__(self, serial) -> None:
        self.__connections: list[ConnectionData] = []
        self.__serial: SerialManager = serial

    
    def add_conection(self) -> UUID:
        self.__connections.append(ConnectionData(uuid1()))


    def remove_connection(self, uuid: UUID) -> bool:
        for c in self.__connections:
            if (c.get_uuid() == uuid):
                self.__connections.remove(c)

    def send_start(self):
        self.__serial.send("ON")
        return "ok"


    def send_stop(self):
        self.__serial.send("OFF")
        return "ok"