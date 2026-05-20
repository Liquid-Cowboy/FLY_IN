from config import Hub, Connection, Config

class Drone():
    _ended: bool = False

    def __init__(self, id: int, start: Hub):
        if not isinstance(id, int):
            raise TypeError('Argument "id" is not a valid integer.')
        if id < 1:
            raise ValueError('Argument "id" must be a positive integer.')
        if not isinstance(start, Hub):
            raise TypeError('Argument "start" is not a valid Hub object.')
        self._id: int = id
        self._cur_zone = start

    @property
    def id(self) -> str:
        """Get drone id as a str."""
        return f'D{self._id}'

    @property
    def current_zone(self) -> str:
        """Get name from zone where the drone is currently at."""
        return self._cur_zone.name

    def get_routes(self, config: Config):
        links: list[Connection] = config.connections
        end: Hub = config.end_hub
        cur: Hub = self._cur_zone
        paths: list[Hub]
        path_way: list[Hub]
        tmp: Hub = cur
        while(1):
            paths = [x.end for x in links if x.start == cur]
            # get possible next nodes


if __name__ == '__main__':

    drones: list[Drone] = []
