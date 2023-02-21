import datetime
import json

class DataManager:
    def __init__(self, path: str | None = None) -> None:
        
        self.__path: str = path

        if (path is None):
            dt: datetime.datetime = datetime.datetime.now()
            self.__path: str = f"./reports/report{dt.year}-{dt.month}-{dt.day}-{dt.hour}-{dt.minute}-{dt.second}.csv"
    
    
    def init_file(self):
        with open(self.__path, 'w') as f:
            f.write("RUNNING,SPEED,ANGLE")

    def convert_data(self, data: str) -> dict:
        try:
            return json.loads(data)
        except:
            return {}
        
    def store_data(self, data: dict) -> None:
        with open(self.__path, 'a') as f:
            f.write(str(data))