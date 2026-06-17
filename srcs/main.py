#!/usr/bin/env python3

import pygame
from utils import Config
from Map import Map
from rendering import Window, Camera, Background, clouds
from ui import Button
from DroneManager import DroneManager

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
background.setup_clouds(clouds)
TEXT_FONT = pygame.font.SysFont("arial", 10)

flyin_map = Map(config)

cam = Camera()

def create_button(size: tuple[int, int]) -> dict:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    button_base = pygame.Surface(size)
    button_base.fill(RED)
    button_highlight = pygame.Surface(size)
    button_highlight.fill(GREEN)
    button_bottom = pygame.Surface(size)
    button_bottom.fill(BLUE)

    return {
        'base': button_base,
        'highlight': button_highlight,
        'bottom': button_bottom,
        'rect': button_base.get_rect()
    }

def something() -> None:
    window_rect = window.screen.get_rect()
    large_button_w = 512
    button_height = 60
    button_gap = 75
    thickness = 20

    logo = pygame.Surface((large_button_w, 250))
    logo.fill((255, 255, 255))

    logo_rect = logo.get_rect()
    logo_rect.center = window_rect.center
    logo_rect.topleft = (logo_rect.topleft[0], 100)

    filename_button = create_button((large_button_w, button_height))
    custom_button = create_button((large_button_w, button_height))
    options_button = create_button((243, button_height))
    quit_button = create_button((243, button_height))

    filename_button['rect'].center = (window_rect.center[0], WINDOW_H // 2 + 50)

    custom_button['rect'].center = (window_rect.center[0], filename_button['rect'].bottomleft[1] + button_gap)

    options_button['rect'].midleft = (custom_button['rect'].midleft[0], custom_button['rect'].bottomleft[1] + button_gap)

    quit_button['rect'].midright = (custom_button['rect'].midright[0], custom_button['rect'].bottomleft[1] + button_gap)

    filename = Button(filename_button['base'],
                      filename_button['highlight'],
                      filename_button['bottom'],
                      filename_button['rect'].topleft,
                      thickness)

    custom = Button(custom_button['base'],
                    custom_button['highlight'],
                    custom_button['bottom'],
                    custom_button['rect'].topleft,
                    thickness)
    
    options = Button(options_button['base'],
                     options_button['highlight'],
                     options_button['bottom'],
                     options_button['rect'].topleft,
                     thickness)
    
    quit = Button(quit_button['base'],
                  quit_button['highlight'],
                  quit_button['bottom'],
                  quit_button['rect'].topleft,
                  thickness)


def main_menu(window: Window) -> None:
    # get button imgs
    # setup button rects at the right place on the grid
    running: bool = True

    while running:
        for event in pygame.event.get():
            if quit.check_click(event):
                running = False
            if event.type == pygame.QUIT:
                running = False

        dt: float = clock.tick(60) / 1000
        window.screen.fill('#59e5ff')
        background.run_clouds(dt)
        # filename.draw(window.screen)
        # filename.check_click(None)
        # custom.draw(window.screen)
        # custom.check_click(None)
        # options.draw(window.screen)
        # options.check_click(None)
        quit.hover()
        quit.draw(window.screen)

        window.screen.blit(logo, logo_rect)

        pygame.display.update()

running = True

clock = pygame.time.Clock()

manager = DroneManager(config)
manager.schedule_drones()
turn_gen = manager.execute_turn()
for res in turn_gen:
    print(res['log'])




# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#         cam.move_camera(event)

#     dt: float = clock.tick(60) / 1000
    

#     window.screen.fill('#59e5ff')

#     background.run_clouds(dt)

#     grid_surface = pygame.Surface((int(WINDOW_W * 0.5), int(WINDOW_H * 0.5)))
#     grid_rect = grid_surface.get_rect(center=window.screen.get_rect().center)
#     grid_surface.fill((255, 255, 255))
#     flyin_map.draw_map(grid_surface, TEXT_FONT, cam, window)
#     window.screen.blit(grid_surface, grid_rect)

#     pygame.display.update()
# pygame.quit()

if __name__ == '__main__':
    main_menu(window)
