#!/usr/bin/env python3

import pygame
from setup import Config
from rendering.Map import Map
from rendering import Window, Camera, Background, Assets
from ui import Button, MainMenu
from setup.DroneManager import DroneManager

WINDOW_W = 1366
WINDOW_H = 768

EASY = 'maps/easy/01_linear_path.txt'
MEDIUM = 'maps/medium/01_dead_end_trap.txt'
HARD = 'maps/hard/02_capacity_hell.txt'
CHALLENGER = 'maps/challenger/01_the_impossible_dream.txt'

FILENAME = HARD

config: Config = Config(FILENAME)

window = Window(WINDOW_W, WINDOW_H)
background = Background(window.screen)
assets = Assets()
assets.load_imgs('assets/imgs')
background.setup_clouds(assets.clouds)
TEXT_FONT = pygame.font.SysFont("arial", 10)

flyin_map = Map(config)

cam = Camera()

running = True

clock = pygame.time.Clock()

# manager = DroneManager(config)
# manager.schedule_drones()
# turn_gen = manager.execute_turn()
# for res in turn_gen:
#     print(res['log'])

button_font = pygame.Font('assets/fonts/Jersey10-Regular.ttf', 35)

main_menu = MainMenu(window, assets, button_font)

if __name__ == '__main__':
    main_menu.main_menu(background, clock)
