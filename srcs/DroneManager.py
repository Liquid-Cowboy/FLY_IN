from Drone import Drone
from utils import Config, Hub, Connection
from constants import ZoneTypes
from Algorithm import Algorithm
from typing import Callable, Generator, Any


class DroneManager():
    _drones: list[Drone] = []

    def __init__(self, config: Config) -> None:
        if not isinstance(config, Config):
            raise TypeError('Argument "config" is not a valid Config obj.')

        self._config: Config = config
        for i in range(1, config.nb_drones + 1):
            self._drones.append(Drone(i, config.start_hub))

    def schedule_drones(self) -> None:
        algo: Callable = Algorithm.a_star

        for d in self._drones:
            path: list[tuple[Hub, int]] | None = algo(
                self._config.start_hub,
                self._config.end_hub,
                self._config.connections)
            if not path:
                continue
            # print(d.id, path[0][0].name)
            for i, item in enumerate(path):
                hub: Hub
                turn: int

                hub, turn = item

                if hub.zone == ZoneTypes.RESTRICTED and i > 0:
                    connection: Connection | None = hub.get_connection(
                        self._config.connections, path[i - 1][0])
                    if not connection:
                        raise Exception
                    if connection.turns.get(turn - 1):
                        connection.turns[turn - 1] += 1
                    else:
                        connection.turns[turn - 1] = 1

                    d.turns[turn - 1] = connection
                if hub.turns.get(turn):
                    hub.turns[turn] += 1
                else:
                    hub.turns[turn] = 1
                d.turns[turn] = hub

    def execute_turn(self) -> Generator:
        i: int = 1
        finished: bool = False
        while not finished:
            finished = True
            moved_drones: list[Drone] = []
            log: str = ''
            for d in self._drones:
                zone: Hub | Connection | None = d.turns.get(i)
                if zone:
                    finished = False
                    if zone != d.turns.get(i - 1):
                        log += d.id + '-' + zone.name + ' '
                        moved_drones.append(d)
            i += 1
            res: dict[str, Any] = {
                'log': log,
                'moved_drones': moved_drones,
                'turn': i,
            }
            yield res
