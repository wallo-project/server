class Speed:
    def __init__(self) -> None:
        self.__speeds: list[float] = []

    def get_speeds(self) -> list[float]:
        return self.__speeds 

    def get_latest_speed(self) -> float:
        if (len(self.__speeds) > 0):
            return self.__speeds[len(self.__speeds)-1]
        else:
            return 0.0

    def add_speed(self, speed: float) -> None:
        self.__speeds.append(speed)