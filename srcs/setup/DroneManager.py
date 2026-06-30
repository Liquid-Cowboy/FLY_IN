from setup.Drone import Drone
from setup import Config, ConfigError, Hub, Connection
from constants import ZoneTypes
from setup.Algorithm import Algorithm
from typing import Callable, Generator, Any
from rendering import Assets, Map


class DroneManager():
    drones: list[Drone] = []

    def __init__(self, config: Config) -> None:
        if not isinstance(config, Config):
            raise TypeError('Argument "config" is not a valid Config obj.')

        self.config: Config = config
        for i in range(1, config.nb_drones + 1):
            self.drones.append(Drone(i, config.start_hub))

    def schedule_drones(self) -> None:
        algo: Callable = Algorithm.a_star
        self.max_turn = 0

        for d in self.drones:
            path: list[tuple[Hub, int]] | None = algo(
                self.config.start_hub,
                self.config.end_hub,
                self.config.connections)
            if not path:
                raise ConfigError('Error: No viable path to end_hub.')

            for i, item in enumerate(path):
                hub: Hub
                turn: int

                hub, turn = item

                if hub.zone == ZoneTypes.RESTRICTED and i > 0:
                    connection: Connection | None = hub.get_connection(
                        self.config.connections, path[i - 1][0])
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

                self.max_turn = max(self.max_turn, turn)

    def execute_turn(self) -> Generator:
        i: int = 1
        finished: bool = False
        while not finished:
            finished = True
            moved_drones: list[Drone] = []
            log: str = ''
            for d in self.drones:
                zone: Hub | Connection | None = d.turns.get(i)
                if zone:
                    finished = False
                    if zone != d.turns.get(i - 1):
                        log += d.id + '-' + zone.name + ' '
                        moved_drones.append(d)
            i += 1
            res: dict[str, Any] = {
                'log': log[:-1],
                'moved_drones': moved_drones,
                'turn': i,
            }
            yield res

    def init_graphics(self, map: Map, assets: Assets) -> None:

        for hub in self.config.hubs:
            hub.init_graphics(map, assets)

        for drone in self.drones:
            drone.init_graphics(assets)
