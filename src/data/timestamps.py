class Timestamp:
    def __init__(self) -> None:
        self.__timestamps: list[float] = []

    def get_timestamps(self) -> list[float]:
        return self.__timestamps 

    def get_latest_speed(self) -> float:
        if (len(self.__timestamps) > 0):
            return self.__timestamps[len(self.__timestamps)-1]
        else:
            return 0.0

    def add_speed(self, speed: float) -> None:
        self.__timestamps.append(speed)