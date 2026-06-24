#! /usr/bin/env python3

import pygame
from pygame import Font, Surface, Rect
# eventually add safeguard for missing imports


class Window():
    def __init__(self, width: int, height: int) -> None:
        """
        Initiates the pygame module and a working screen
        """
        self.width: int = width
        self.height: int = height
        pygame.init()

        self.screen = pygame.display.set_mode((width, height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption('Fly-In')

    @staticmethod
    def draw_text(surface: Surface, text: str, font: Font,
                  color: tuple[int, int, int],
                  center: tuple[int, int]) -> Surface:
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
        img_rect.center = center
        surface.blit(img, img_rect)

        return img


if __name__ == '__main__':
    renderer = Window(1000, 800)
