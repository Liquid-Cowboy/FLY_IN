#!/usr/bin/env python3

import pygame
from setup import Config
from rendering.Map import Map
from rendering import Camera
from ui import Engine
# from setup.DroneManager import DroneManager

WINDOW_W = 1366
WINDOW_H = 768

EASY = 'maps/easy/01_linear_path.txt'
MEDIUM = 'maps/medium/01_dead_end_trap.txt'
HARD = 'maps/hard/02_capacity_hell.txt'
CHALLENGER = 'maps/challenger/01_the_impossible_dream.txt'

FILENAME = HARD

FPS = 60


# manager = DroneManager(config)
# manager.schedule_drones()
# turn_gen = manager.execute_turn()
# for res in turn_gen:
#     print(res['log'])

IMGS_PATH: str = 'assets/imgs/'
FONT_PATH: str = 'assets/fonts/Jersey10-Regular.ttf'


if __name__ == '__main__':

    e = Engine((WINDOW_W, WINDOW_H),
               IMGS_PATH,
               FONT_PATH)

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
