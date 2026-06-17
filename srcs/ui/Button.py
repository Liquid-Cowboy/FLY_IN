#!/usr/bin/env python3

import pygame
from pygame import Surface, Rect, Event
from typing import Callable, Any
import sys


class Button():
    def __init__(self,
                 base_img: Surface,
                 highlight: Surface,
                 bottom_img: Surface,
                 pos: tuple[int, int],
                 thickness: int) -> None:

        self.pressed: bool = False

        self.thickness: int = thickness
        self.dynamic_thickness: int = thickness

        self.top_rect: Rect = base_img.get_rect()
        self.top_rect.topleft = pos

        self.pos: tuple[int, int] = pos
        self.size: tuple[int, int] = base_img.get_size()

        self.base_img: Surface = base_img
        self.highlight: Surface = highlight
        self.bottom_img: Surface = bottom_img

        self.top_img: Surface = base_img

    def draw(self, screen: Surface):
        screen.blit(self.bottom_img,
                    (self.pos[0],
                     self.pos[1]))
        screen.blit(self.top_img,
                    (self.pos[0],
                     self.pos[1] - self.dynamic_thickness))

    def hover(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_img = self.highlight
        else:
            self.top_img = self.base_img

    def check_click(self, event: Event) -> bool:

        if event.type not in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            return False
        if self.top_rect.collidepoint(event.pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.dynamic_thickness = 0
                self.pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dynamic_thickness = self.thickness
                return True
        return False

# if __name__ == '__main__':
#     pygame.init()
#     screen = pygame.display.set_mode((500, 500))
#     clock = pygame.time.Clock()
#     gui_font = pygame.font.Font(None, 30)

#     button1 = Button('Click me', 200, 40, (100, 250), 6)

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#         screen.fill('#DCDDD8')
#         button1.draw()
#         button1.check_click()
#         pygame.display.update()
#         clock.tick(60)
