#! /usr/bin/env python3

from setup import Hub, Config, Connection
import heapq
from constants import ZoneTypes
from math import sqrt
import itertools


class Algorithm():
    @staticmethod
    def a_star(start: Hub, end: Hub,
               connections: list[Connection]) -> list[tuple[Hub, int]] | None:
        """
        Runs A* algorithm to find shortest path to the end hub.

        Arguments:
            start = Hub from where to start the algorithm
            end = Goal to which the path is heading towards
        """

        visited: set = set()
        queue: list = []
        if not start.h:
            start.h = Algorithm.euclidean_d(start, end)
        counter = itertools.count()
        # a counter is used as a tie breaker between
        # nodes with the same priority

        heapq.heappush(queue, (0, next(counter), start, 0))
        path: list[tuple[Hub, int]] = []
        curr: Hub | None
        turn: int
        end_node: tuple[Hub, int] | None = None
        came_from: dict = {}
        loop_ended: bool = False

        while queue:
            _, _, curr, turn = heapq.heappop(queue)

            if not curr:
                break

            curr.neighbours.sort(key=lambda z: z.zone
                                 != ZoneTypes.PRIORITY)

            for n in curr.neighbours:

                if not n.h:
                    n.h = Algorithm.euclidean_d(n, end)

                move_cost: int = 1
                if n.zone == ZoneTypes.RESTRICTED:
                    if not Algorithm.check_restricted_zone(curr, n,
                                                           turn, connections):
                        continue
                    move_cost = 2

                else:
                    move_cost = 1

                g: int = turn + move_cost

                if ((n, g) in visited or
                   n.zone == ZoneTypes.BLOCKED or
                   n.turns.get(g) == n.max_drones):
                    continue

                f: int = g + n.h
                came_from[(n, g)] = (curr, turn)

                if n == end:
                    end_node = (n, g)
                    queue.clear()
                    loop_ended = True
                    break

                heapq.heappush(queue, (f,  # priority
                                       next(counter),  # tiebreaker
                                       n,  # hub
                                       g  # next turn
                                       ))
            if loop_ended:
                break

            g = turn + 1
            f = g + curr.h if curr.h else 0
            if (curr, g) not in visited:
                came_from[(curr, g)] = (curr, turn)
                heapq.heappush(queue, (f,
                               next(counter),
                               curr,
                               g))

            visited.add((curr, turn))

        while end_node:
            path.append(end_node)
            end_node = came_from.get(end_node)

        return path[-1::-1]

    @staticmethod
    def check_restricted_zone(curr: Hub, next: Hub,
                              turn: int,
                              connections: list[Connection]):

        connection: Connection | None = next.get_connection(connections, curr)
        if not connection:
            return False

        connection_drones: int | None = connection.turns.get(
            turn + 1)

        if (connection_drones and
           connection_drones >= connection.max_link_capacity):
            return False

        return True

    @staticmethod
    def euclidean_d(cur: Hub, target: Hub) -> int:
        """
        Utility function to calculate the euclidean distance between
        two Hubs.

        Arguments:
            cur = starting Hub
            target = end goal Hub
        """
        x1: int = cur.x
        x2: int = target.x
        y1: int = cur.y
        y2: int = target.y
        return int(sqrt((x2-x1)**2 + (y2 - y1)**2))


if __name__ == '__main__':
    FILENAME = '../maps/medium/01_dead_end_trap.txt'

    astar = Algorithm()
    config = Config(FILENAME)
