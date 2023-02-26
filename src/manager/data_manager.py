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
            f.write("TIME;RUNNING;DISTANCE;FRONT_DISTANCE;LEFT_DISTANCE;RIGHT_DISTANCE;LINE_DETECTION;COMMAND_RESPONSE\n")

    def convert_data(self, data: str) -> dict[str]:
        try:
            if (data != ''):
                array: list[str] = data.split(";")
                if (len(array) == 7):
                    data = f'"time":"{datetime.datetime.now()}","running":{str(array[0])},"distance":{str(array[1])},"left":{str(array[2])},"front":{str(array[3])},"right":{str(array[4])},"lineDetection":{str(array[5])},"commandResponse":{str(array[6])}'
                else:
                    data = f'"time":"{datetime.datetime.now()}","running":-1,"distance":-1,"front":-1,"left":-1,"right":-1,"lineDetection":-1,"commandResponse":-1'
                return json.loads("{"+data+"}")
        except:
            return {}
        
    def store_data(self, data: dict[str, str]) -> None:
        with open(self.__path, 'a') as f:
            f.write(str(data['time'])+';'+str(data["running"])+';'+str(data['distance'])+';'+str(data['front'])+';'+str(data['left'])+';'+str(data['right'])+';'+str(data['lineDetection'])+';'+str(data['commandResponse'])+'\n')