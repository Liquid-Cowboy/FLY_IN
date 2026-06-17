#! /usr/bin/env python3

import pygame
from pygame import Font, Surface, Rect
# eventually add safeguard for missing imports


class Window():
    def __init__(self, width: int, height: int) -> None:
        """
        Initiates the pygame module and a working screen
        """

        pygame.init()

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Fly-In')

    def draw_text(self, surface: Surface, text: str, font: Font,
                  color: tuple[int, int, int],
                  x: int, y: int):
        """
        Utility function to draw centered text.

            Atributes:

            surface: Surface - surface in which to display the
                text on
            text: str - string of text to be displayed
            font: Font - font obj describing font type and size
            color: tuple[int, int, int] - RGB value of the chosen color
            x: int - cordinate of middle
            y: int - coordinate of center
        """

        img: Surface = font.render(text, True, color)
        img_rect: Rect = img.get_rect()
        img_rect.center = (x, y)
        surface.blit(img, img_rect)


if __name__ == '__main__':
    renderer = Window(1000, 800)
