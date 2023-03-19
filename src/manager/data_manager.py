"""! File containing the data managing system, its goal is to convert and format data.
This manager is called in the serial server.

@author WALL-O Team
@version 1.0.0
@since 15 January 2023
"""
# import libs
import datetime
import json
import os

class DataManager:
    """! Class that manage all the data. It format the data received from the Arduino.
    It also save the data in a report file.
    
    @author WALL-O Team
    @version 1.0.0
    @since 15 January 2023
    """
    def __init__(self) -> None:
        """! Constructor of the data manager."""
        # create the datetime to be used in the file
        dt: datetime.datetime = datetime.datetime.now()
        # create the name of the file
        self.__filename: str = f"report{dt.year}-{dt.month}-{dt.day}-{dt.hour}-{dt.minute}-{dt.second}.csv"
        # create the path of the file
        self.__path: str = f"./reports/{self.__filename}"
    
    def get_filename(self) -> str:
        """! Method to get the name of the latest file.
        The name of the file does not contain the path.
        
        @return a string containing the file name.
        """
        return self.__filename
    
    def init_file(self) -> None:
        """! Method that init the file to store data.
        The method also creates the path to contain all the reports if its does not exist.
        """
        # check if path already exist or not
        path_exist = os.path.exists("reports")
        if (not path_exist):
            # Create a new directory because it does not exist
            os.makedirs("reports")
        
        with open(self.__path, 'w') as f:
            # open the file and add the corresponding titles
            f.write("TIME;RUNNING;DISTANCE;FRONT_DISTANCE;LEFT_DISTANCE;RIGHT_DISTANCE;LINE_DETECTION_ACTIVATION;LINE_DETECTED;COMMAND_RESPONSE\n")

    def convert_data(self, data: str) -> dict[str]:
        """! Method that convert data from a string to a dictionary.
        This dict is delivered to the web application via the REST API.
        
        @param data the string received from the Arduino.
        @return a dictionary of data.
        """
        try:
            # use try to prevent any errors in data split
            
            if (data != ''):
                # if the data is not empty, split it
                array: list[str] = data.split(";")

                if (len(array) == 8):
                    # check if the length of the array is correct
                    data = f'"time":"{datetime.datetime.now()}","running":{str(array[0])},"distance":{str(array[1])},"left":{str(array[2])},"front":{str(array[3])},"right":{str(array[4])},"lineDetectionSensors":{str(array[5])},"lineDetection":{str(array[6])},"commandResponse":{str(array[7])}'
                
                else:
                    # else use default data
                    data = f'"time":"{datetime.datetime.now()}","running":-1,"distance":-1,"front":-1,"left":-1,"right":-1,"lineDetectionSensors":-1,"lineDetection":-1,"commandResponse":-1'
           
            else:
                # if data is empty use default data
                data = f'"time":"{datetime.datetime.now()}","running":-1,"distance":-1,"front":-1,"left":-1,"right":-1,"lineDetectionSensors":-1,"lineDetection":-1,"commandResponse":-1'
        except:
            # in case of error, use default data
            data = f'"time":"{datetime.datetime.now()}","running":-1,"distance":-1,"front":-1,"left":-1,"right":-1,"lineDetectionSensors":-1,"lineDetection":-1,"commandResponse":-1'
        
        # return a dict
        return json.loads("{"+data+"}")
        
    def store_data(self, data: dict[str, str]) -> None:
        """! Method that store the data in the file.
        This file contains all the data retrieved from the Arduino.
        
        @param data the dictionary extracted from the string from the Arduino.
        """
        with open(self.__path, 'a') as f:
            f.write(str(data['time'])+';'+str(data["running"])+';'+str(data['distance'])+';'+str(data['front'])+';'+str(data['left'])+';'+str(data['right'])+';'+str(data['lineDetectionSensors'])+';'+str(data['lineDetection'])+';'+str(data['commandResponse'])+'\n')