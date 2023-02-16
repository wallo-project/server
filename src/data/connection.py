"""! File that contains the connection class.
All the informations of a connection are contained in this class.

@author WALL-O Dev Team
@version 0.0.1
@since 22 January 2023
"""

from uuid import UUID

class ConnectionData:
    """! Class that contains all the informations about a connection.
    A connection represent a client connected to the server.
    
    @author WALL-O Dev Team
    @version 0.0.1
    @since 22 January 2023
    """
    def __init__(self, uuid: UUID) -> None:
        """! Constructor of the class.
        This class contains the data needed to store informations about the connection.

        @param uuid the unique identifier of the connection.
        @param name the name selected for the robot.
        """
        self.__uuid: UUID = uuid
        self.__latest_params: dict = {}


