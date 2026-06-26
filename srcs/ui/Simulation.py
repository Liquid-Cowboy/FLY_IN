from __future__ import annotations
from typing import TYPE_CHECKING
from setup import Config, DroneManager
from pygame import Surface, Event
from .Scene import Scene
from rendering import Camera, Map

if TYPE_CHECKING:
    from .Engine import Engine


class Simulation(Scene):
    def __init__(self,
                 engine: Engine,
                 config: Config) -> None:

        super().__init__(engine)

        self.config: Config = config
        self.cam = Camera()
        self.map = Map(config)
        self.manager = DroneManager(config)
        self.manager.schedule_drones()
        self.drone_sprites = {}

        for drone in self.manager._drones:
            surface = engine.assets.drone.copy()
            rect = surface.get_rect()

            self.drone_sprites[drone.id]['surface'] = surface
            self.drone_sprites[drone.id]['rect'] = rect

    def handle_event(self, event: Event):
        return super().handle_event(event)

    def update(self, dt: float):
        return super().update(dt)

    def draw(self, screen: Surface):
        return super().draw(screen)
