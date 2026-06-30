
from setup import Hub, Connection
from collections import deque
from pygame import Rect, Surface
from rendering import Assets


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

    def init_graphics(self, assets: Assets) -> None:
        self.img: Surface = assets.drone.copy()

        self.rect: Rect = self.img.get_rect()

    @property
    def id(self) -> str:
        """Get drone id as a str."""
        return f'D{self._id}'


if __name__ == '__main__':

    drones: list[Drone] = []
