from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Drone import Drone

from constants import Colors, ZoneTypes


@dataclass
class Hub():
    """
    Unit of a zone in Fly-In.

        Attributes:

        name: str - name of the zone.
        x: int - integer mapping the x coordinate of the zone
        y: int - integer mapping the y coordinate of the zone
        zone: ZoneTypes - one of four types of zones ("normal",
            "restricted", "priority", "blocked")
        color: Colors - one of the valid Colors accepted by the
            program
        max_drones: int - max drone capacity for this zone
        cur_drones: int - how many drones are currently in this
            zone
        connections: list[Hub] - list of zones in near proximity
    """
    name: str = ''
    x: int = 0
    y: int = 0
    zone: ZoneTypes = ZoneTypes.NORMAL
    color: Colors = Colors.WHITE
    max_drones: int = 1

    curr_drones: list[Drone] = field(default_factory=list)

    neighbours: list[Hub] = field(default_factory=list)

    turns: dict[int, int] = field(default_factory=dict)

    h: int | None = None

    def get_connection(self, connections: list[Connection],
                       zone: Hub) -> Connection | None:
        for c in connections:
            if (c.zone1 == self and c.zone2 == zone or
               c.zone2 == self and c.zone1 == zone):
                return c
        return None
    
    def __hash__(self):
        return hash(self.name)


class Connection():
    """
    Keeps track of connections between zones and their
        capacity.

        Attributes:

        start: Hub - the starting Hub
        end: Hub - the destination Hub
        max_link_capacity: int - how many drones can
            simultaneously pass through this connection
        cur_drones: int - how many drones are currently
            passing through this location
    """
    def __init__(self, zone1: Hub, zone2: Hub, max_link_capacity: int = 1):
        self.zone1: Hub = zone1
        self.zone2: Hub = zone2

        self.turns: dict[int, int] = {}

        self.max_link_capacity: int = max_link_capacity
        self.cur_drones: int = 0

    @property
    def name(self) -> str:
        """Get connection name"""
        return self.zone1.name + '-' + self.zone2.name
