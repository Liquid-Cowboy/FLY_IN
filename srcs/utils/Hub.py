from dataclasses import dataclass, field
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
    cur_drones: int = 0
    connections: list["Hub"] = field(default_factory=list)
    visited: bool = False
    cost: int = 0
    eur: int = 0


@dataclass
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
    start: Hub
    end: Hub
    max_link_capacity: int = 1
    cur_drones: int = 0
