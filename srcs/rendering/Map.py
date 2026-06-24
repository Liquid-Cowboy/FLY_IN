from setup import Config
from constants import COLOR_CODE
from rendering import Camera, Window
import pygame
from pygame import Surface, Font


class Map():
    def __init__(self, config: Config):

        self._hubs = config.hubs
        self._connections = config.connections
        self._min_x: int = min(h.x for h in config.hubs)
        self._min_y: int = min(h.y for h in config.hubs)
        self._max_x: int = max(h.x for h in config.hubs)
        self._max_y: int = max(h.y for h in config.hubs)
        # if we have cells in negative positions, the comp(ensation) fields
        # will help us to draw the whole map
        self._comp_x: int = abs(self._min_x) if self._min_x < 0 else 0
        self._comp_y: int = abs(self._min_y) if self._min_y < 0 else 0

        self._base_cs: int = 5
        self._zoom: float = 25.0
        self._cs: int = round(self._base_cs * self._zoom)

        self._width: int = (self._max_x + self._comp_x + 1) * self._cs
        self._height: int = (self._max_y + self._comp_y + 1) * self._cs

    def get_cell_pos(self, x: int, y: int) -> tuple[int, int]:
        """Translates input coordinates to pixel coordinates on the screen"""
        return ((x + self._comp_x) * self._cs + self._cs // 2,
                (y + self._comp_y) * self._cs + self._cs // 2)

    def draw_map(self, surface: Surface, hub_font: Font,
                 cam: Camera, win: Window):

        cs: int = self._cs
        circle_rad: float = (cs // 2) * 0.8
        circle_rad = cam.get_trans_nb(int(circle_rad))
        line_width = cam.get_trans_nb(3)

        x1: int
        x2: int
        y1: int
        y2: int

        for c in self._connections:
            x1, y1 = cam.get_screen_coor(
                self.get_cell_pos(
                    c.zone1.x,
                    c.zone1.y
                ))

            x2, y2 = cam.get_screen_coor(
                self.get_cell_pos(
                    c.zone2.x,
                    c.zone2.y
                ))
            pygame.draw.line(surface, (0, 0, 0),
                             (x1, y1), (x2, y2), line_width)
        for hub in self._hubs:

            # transform coordinates based on camera
            x1, y1 = cam.get_screen_coor(self.get_cell_pos(hub.x, hub.y))

            pygame.draw.circle(surface,
                               COLOR_CODE[hub.color.value],
                               (x1, y1), circle_rad)
            pygame.draw.circle(surface,
                               (0, 0, 0),
                               (x1, y1), circle_rad, line_width)
            win.draw_text(surface, hub.name, hub_font, (255, 255, 255), x1, y1)
