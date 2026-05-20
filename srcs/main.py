#!/usr/bin/env python3

import pygame
from utils import Config
from Map import Map
from rendering import Window, Camera

WINDOW_W = 1000
WINDOW_H = 600

FILENAME = '../maps/easy/01_linear_path.txt'

config: Config = Config(FILENAME)

window = Window(WINDOW_W, WINDOW_H)


TEXT_FONT = pygame.font.SysFont("arial", 10)

flyin_map = Map(config)

cam = Camera()

running = True
while running:

    window.screen.fill((0, 0, 0))
    grid_surface = pygame.Surface((int(WINDOW_W * 0.5), int(WINDOW_H * 0.5)))
    grid_rect = grid_surface.get_rect(center=window.screen.get_rect().center)
    grid_surface.fill((255, 255, 255))
    flyin_map.draw_map(grid_surface, TEXT_FONT, cam, window)
    window.screen.blit(grid_surface, grid_rect)
    for event in pygame.event.get():
        cam.move_camera(event)
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()
