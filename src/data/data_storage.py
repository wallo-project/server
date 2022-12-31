class DataStorage:

    __speeds: list[float] = []
    __angles: list[float] = []

    def __init__(self) -> None:
        pass

    def get_speeds() -> list[float]:
        return DataStorage.__speeds

    def get_angles() -> list[float]:
        return DataStorage.__angles

