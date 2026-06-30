#!/usr/bin/env python3

from __future__ import annotations
from typing import TYPE_CHECKING
from setup import Config, DroneManager, Hub, Connection
from pygame import Surface, Event
from .Scene import Scene
from rendering import Camera, Map
import pygame

if TYPE_CHECKING:
    from .Engine import Engine


class Simulation(Scene):
    def __init__(self,
                 engine: Engine,
                 config: Config) -> None:

        super().__init__(engine)

        self.config: Config = config
        self.cam = Camera()
        self.map = Map(config, engine.window)
        self.manager = DroneManager(config)
        self.manager.schedule_drones()
        self.manager.init_graphics(self.map, self.engine.assets)
        self.logs = []
        turn_gen = self.manager.execute_turn()
        for res in turn_gen:
            self.logs.append(res['log'])
        self.logs = self.logs[:-1]

        self.turn = 0

    def handle_event(self, event: Event):
        self.cam.move_camera(event)
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RIGHT and
               self.turn < self.manager.max_turn):
                print(self.logs[self.turn])
                self.turn += 1

            elif event.key == pygame.K_LEFT and self.turn > 0:
                self.turn -= 1

    def update(self, dt: float):
        return super().update(dt)

    def update_drone_pos(self):
        for d in self.manager.drones:
            if not d.turns.get(self.turn):
                continue
            hub: Hub | Connection = d.turns[self.turn]

            if isinstance(hub, Hub):
                d.rect.center = hub.rect.center

            else:
                if self.turn < 1:
                    d.rect.center = self.manager.config.start_hub.rect.center
                else:
                    prev_hub: tuple[int, int]
                    next_hub: tuple[int, int]

                    if hub.zone1 == d.turns[self.turn - 1]:
                        prev_hub = hub.zone1.rect.center
                        next_hub = hub.zone2.rect.center
                    else:
                        prev_hub = hub.zone2.rect.center
                        next_hub = hub.zone1.rect.center

                    middle_x: int = ((next_hub[0] - prev_hub[0]) // 2 +
                                     prev_hub[0])

                    middle_y: int = ((next_hub[1] - prev_hub[1]) // 2 +
                                     prev_hub[1])

                    d.rect.center = (middle_x, middle_y)

    def draw(self, screen: Surface):
        self.update_drone_pos()
        self.draw_connections(screen)

        for hub in self.manager.config.hubs:
            img: Surface = hub.img
            img = pygame.transform.scale_by(img, self.cam._zoom)
            topleft = self.cam.get_screen_coor(hub.rect.topleft)
            screen.blit(img, topleft)

        for d in self.manager.drones:
            img: Surface = d.img
            img = pygame.transform.scale_by(img, self.cam._zoom)
            topleft = self.cam.get_screen_coor(d.rect.topleft)
            screen.blit(img, topleft)

        # self.draw_grid(screen)

    def draw_connections(self, screen: Surface) -> None:
        connections = self.config.connections
        thickness = self.cam.get_trans_nb(10)

        for c in connections:
            zone1_pos = c.zone1.rect.center
            zone2_pos = c.zone2.rect.center

            zone1_pos = self.cam.get_screen_coor(zone1_pos)
            zone2_pos = self.cam.get_screen_coor(zone2_pos)

            pygame.draw.line(screen, (0, 0, 0), zone1_pos,
                             zone2_pos, thickness)

    def draw_grid(self, screen):
        map_width = self.map.max_x + self.map.comp_x
        map_height = self.map.max_y + self.map.comp_y
        real_width = self.cam.get_trans_nb(self.map.width)
        real_height = self.cam.get_trans_nb(self.map.height)

        for x in range(map_width + 2):
            x, y = self.map.get_cell_pos(x, 0)
            x, y = self.cam.get_screen_coor((x, y))
            pygame.draw.line(screen,
                             (0, 255, 0),
                             (x, y),
                             (x, y + real_height), 10)

        for y in range(map_height + 2):
            x, y = self.map.get_cell_pos(0, y)
            x, y = self.cam.get_screen_coor((x, y))
            pygame.draw.line(screen,
                             (0, 255, 0),
                             (x, y),
                             (x + real_width, y), 10)


if __name__ == '__main__':
    from .Engine import Engine

    WINDOW_W = 1366
    WINDOW_H = 768
    IMGS_PATH: str = 'assets/imgs/'
    FONT_PATH: str = 'assets/fonts/Jersey10-Regular.ttf'
    FILEPATH = 'maps/challenger/01_the_impossible_dream.txt'
    FPS = 60

    e = Engine((WINDOW_W, WINDOW_H),
               IMGS_PATH,
               FONT_PATH)
    config = Config(FILEPATH)
    e.scene = Simulation(e, config)
    while e.running:

        dt: float = e.clock.tick(FPS) / 1000
        e.window.screen.fill('#59e5ff')
        e.background.run_clouds(dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                e.running = False

            e.scene.handle_event(event)
        e.scene.update(dt)
        e.scene.draw(e.window.screen)

        pygame.display.update()
