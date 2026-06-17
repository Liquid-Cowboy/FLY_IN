#!/usr/bin/env python3

import pygame
import sys


class Button():
    def __init__(self, text: str,
                 width: int, height: int,
                 pos: tuple[int, int], thickness: int) -> None:

        self.pressed: bool = False

        self.thickness = thickness
        self.dynamic_thickness = thickness
        self.original_height = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, thickness))
        self.bottom_color = '#354B5E'

        # text
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # thickness logic
        self.top_rect.y = self.original_height - self.dynamic_thickness
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_thickness

        pygame.draw.rect(screen, self.bottom_color,
                         self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color,
                         self.top_rect, border_radius=12)

        screen.blit(self.text_surf, self.text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_thickness = 0
                self.pressed = True
            elif self.pressed:
                print('click')
                self.dynamic_thickness = self.thickness
                self.pressed = False
        else:
            self.top_color = '#475F77'


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    gui_font = pygame.font.Font(None, 30)

    button1 = Button('Click me', 200, 40, (100, 250), 6)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('#DCDDD8')
        button1.draw()
        button1.check_click()
        pygame.display.update()
        clock.tick(60)
