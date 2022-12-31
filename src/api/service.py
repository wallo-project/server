from data.data_storage import DataStorage

class Service:
    def __init__(self) -> None:
        self.__data = DataStorage()


    def get_data(self):
        return {"speeds": self.__data.get_speeds(), "angles": self.__data.get_angles()}