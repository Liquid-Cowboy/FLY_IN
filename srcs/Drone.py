from utils import Hub, Connection
from collections import deque


class Drone():

    def __init__(self, id: int, start: Hub):
        if not isinstance(id, int):
            raise TypeError('Argument "id" is not a valid integer.')
        if id < 1:
            raise ValueError('Argument "id" must be a positive integer.')
        if not isinstance(start, Hub):
            raise TypeError('Argument "start" is not a valid Hub object.')
        self._id: int = id
        self._curr_zone: Hub | Connection = start
        self.path: deque = deque()
        self.turns: dict[int, Hub | Connection] = {}

    @property
    def id(self) -> str:
        """Get drone id as a str."""
        return f'D{self._id}'


if __name__ == '__main__':

    drones: list[Drone] = []
