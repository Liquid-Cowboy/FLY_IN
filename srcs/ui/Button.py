#!/usr/bin/env python3

import pygame
from pygame import Surface, Rect, Event


class Button():
    def __init__(self,
                 base: Surface,
                 highlight: Surface,
                 bottom_img: Surface,
                 rect: Rect,
                 text_img: Surface | None = None) -> None:

        self.base_img: Surface = base
        self.highlight: Surface = highlight
        self.bottom_img: Surface = bottom_img
        self.rect: Rect = rect
        self.text_img: Surface | None = text_img

        self.topleft: tuple[int, int] = self.rect.topleft

        self.thickness: int = 10
        self.text_leading: int = 50
        self.dynamic_thickness: int = self.thickness

        self.size: tuple[int, int] = base.get_size()

        self.top_img: Surface = base

        self.pressed: bool = False

    def draw(self, screen: Surface) -> None:
        self.rect.topleft = (self.topleft[0],
                             self.topleft[1] - self.dynamic_thickness)

        screen.blit(self.bottom_img,
                    self.topleft)

        screen.blit(self.top_img,
                    (self.rect))

        if self.text_img:

            text_x: int = self.rect.left + self.text_leading
            text_size_y: int = self.text_img.get_size()[1]
            text_y: int = self.rect.centery - text_size_y // 2

            screen.blit(self.text_img, (text_x, text_y))

    def hover(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.top_img = self.highlight
        else:
            self.top_img = self.base_img

    def check_click(self, event: Event) -> bool:

        if event.type not in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            return False

        if event.type == pygame.MOUSEBUTTONUP:
            self.dynamic_thickness = self.thickness

        if self.rect.collidepoint(event.pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.dynamic_thickness = 0
                self.pressed = True

            if event.type == pygame.MOUSEBUTTONUP and self.pressed:
                return True
        else:
            self.pressed = False
        return False
