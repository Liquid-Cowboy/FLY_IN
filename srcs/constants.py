from enum import Enum

COLOR_CODE = {
    'white': (255, 255, 255),
    'yellow': (255, 255, 0),
    'orange': (255, 165, 0),
    'red': (255, 0, 0),
    'crimson': (200, 20, 60),
    'darkred': (139, 0, 0),
    'violet': (127, 0, 255),
    'purple': (128, 0, 128),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'brown': (150, 75, 0),
    'maroon': (85, 0, 0),
    'gold': (255, 215, 0),
    'black': (0, 0, 0),
}


class Colors(Enum):
    WHITE = 'white'
    YELLOW = 'yellow'
    ORANGE = 'orange'
    RED = 'red'
    CRIMSON = 'crimson'
    DARKRED = 'darkred'
    VIOLET = 'violet'
    PURPLE = 'purple'
    BLUE = 'blue'
    GREEN = 'green'
    BROWN = 'brown'
    MAROON = 'maroon'
    GOLD = 'gold'
    BLACK = 'black'
    RAINBOW = 'rainbow'


class ZoneTypes(Enum):
    NORMAL = 'normal'
    BLOCKED = 'blocked'
    RESTRICTED = 'restricted'
    PRIORITY = 'priority'
