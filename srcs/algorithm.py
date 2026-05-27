#! /usr/bin/env python3

from utils import Hub, Config
import heapq
from constants import ZoneTypes


class AStar():
    @staticmethod
    def organize(start: Hub, end:Hub, config: Config) -> None:
        visited: list = []
        queue: list = []
        heapq.heappush(queue, (0, start))
        while (queue):
            node: tuple[int, Hub] = heapq.heappop(queue)
            for neighbour in node[1].connections:
                
            


    def change_hub_cost(cur: Hub, target: Hub) -> None:



if __name__ == '__main__':
    FILENAME = '../maps/medium/01_dead_end_trap.txt'

    astar = AStar()
    config = Config(FILENAME)
    astar.organize(config)