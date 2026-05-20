from Drone import Drone
from utils import Config, Hub
from constants import ZoneTypes

class DroneManager():
    _drones: list[Drone] = []

    def __init__(self, config: Config):
        if not isinstance(config, Config):
            raise TypeError('Argument "config" is not a valid Config obj.')

        self._config: Config = config
        for i in range(1, config.nb_drones + 1):
            self._drones.append(Drone(i, config.start_hub))

    def validate_map(self):
        hubs:list[Hub] = self._config.hubs
        cur: Hub = self._config.start_hub
        end_hub: Hub = self._config.end_hub
        cur.cost = 0
        while not end_hub.visited:
            cur.visited = True
            self.astar_helper(cur, end_hub)


    @staticmethod
    def astar_helper(start: Hub, end: Hub):

        x2: int = end.x
        y2: int = end.y

        s_cost: int = start.cost if start.cost else 0

        for hub in start.connections:
            if hub.zone == ZoneTypes.BLOCKED:
                continue
            x1: int = hub.x
            y1: int = hub.y
            cost: int = s_cost + abs(x2 - x1) + abs(y2 - y1)
            if hub.zone == ZoneTypes.RESTRICTED:
                cost += 1
            elif hub.zone == ZoneTypes.PRIORITY:
                cost -= 1
            if not hub.cost or hub.cost > cost:
                hub.cost = cost




if __name__ == '__main__':
    from parser import parser

    config: Config = parser('../maps/easy/01_linear_path.txt')
    manager: DroneManager = DroneManager(config)
    for drone in manager._drones:
        print(drone.id)
