import pygame
from pygame import Surface, Rect
import random
from typing import Any

IMGS_FOLDER = 'imgs/flats/'

IMGS = {
    'big_cloud_1': pygame.image.load(IMGS_FOLDER + '42_cloud.png'),
    'big_cloud_2': pygame.image.load(IMGS_FOLDER + 'big_cloud_1.png'),
    'big_cloud_3': pygame.image.load(IMGS_FOLDER + 'big_cloud_2.png'),
    'medium_cloud_1': pygame.image.load(IMGS_FOLDER + 'medium_cloud_1.png'),
    'medium_cloud_2': pygame.image.load(IMGS_FOLDER + 'medium_cloud_2.png'),
    'medium_cloud_3': pygame.image.load(IMGS_FOLDER + 'medium_cloud_3.png'),
    'medium_cloud_4': pygame.image.load(IMGS_FOLDER + 'medium_cloud_4.png'),
    'medium_cloud_5': pygame.image.load(IMGS_FOLDER + 'medium_cloud_5.png'),
    'medium_cloud_6': pygame.image.load(IMGS_FOLDER + 'medium_cloud_6.png')
}


class Background():
    """
    Object directed towards making background cloud animation.
    """
    def __init__(self, screen: Surface):
        """
        Initiates basic background info.

        Args:
            screen = Surface object on which to blit clouds.
        """
        self.screen: Surface = screen
        self.screen_rect: Rect = screen.get_rect()
        self.pos: tuple[int, int] = screen.get_offset()
        self.size: tuple[int, int] = screen.get_size()
        self.clouds: list[dict[str, Any]] = []

    def setup_clouds(self, imgs: dict[str, Surface]) -> None:
        """
         Initializes cloud assets, organizing useful information in a
         concise way.

         Args:
            imgs = Dictionary in which the key is the name of the image
            and the value is the Surface object of the loaded image itself
        """
        for k, v in imgs.items():
            surf = pygame.transform.scale_by(v.convert_alpha(), 5)
            size: tuple[int, int] = surf.get_size()
            x: int = random.randint(-int(size[0] * 0.8),
                                    self.pos[0] + self.size[0] - 10)
            y: int = random.randint(-int(size[1] * 0.8),
                                    self.pos[1] + self.size[1] - 10)
            cloud = {
                'name': k,
                'surf': surf,
                'pos': (x, y),
                'size': size,
                'direction': self.chose_direction(),
            }
            self.clouds.append(cloud)

    def run_clouds(self, dt: float) -> None:
        """
        Runs the cloud animation by updating their position
        """
        for c in self.clouds:
            direction: str | None = c.get('direction')
            pos: tuple[int, int] | None = c.get('pos')
            size: tuple[int, int] | None = c.get('size')
            surf: Surface | None = c.get('surf')

            if (direction is None or
               pos is None or
               size is None or
               surf is None):
                return
            if not self.check_bounds(direction, pos[0], pos[0] + size[0]):
                c['direction'] = self.chose_direction()
                y: int = random.randint(-int(size[1] * 0.8),
                                        self.pos[1] + self.size[1] - 10)
                if c['direction'] == 'left':
                    x: int = self.pos[0] + self.size[0]
                else:
                    x: int = self.pos[0] - size[0]
                c['pos'] = (x, y)
            self.screen.blit(surf, pos)
        self.move_clouds(dt)

    def move_clouds(self, dt: float) -> None:
        """
        Increments or decrements the cloud position,
        given the assigned direction.

        Args:
            dt = Delta time - converted time so FPS can be
        """
        for c in self.clouds:
            name: str | None = c.get('name')
            speed: float
            if not name:
                return
            if name.startswith('small'):
                speed = 5 * dt
            elif name.startswith('medium'):
                speed = 10 * dt
            else:
                speed = 15 * dt
            pos: tuple[int, int] | None = c.get('pos')
            if pos is None:
                return

            x: int
            y: int

            x, y = pos
            if c.get('direction') == 'left':
                c['pos'] = (x - speed, y)
            else:
                c['pos'] = (x + speed, y)

    def check_bounds(self, direction: str, left: int, right: int) -> bool:
        """
        Checks if the given coordinates are out of bounds, given the
        direction the object is moving towards.

        Args:
            direction = "left" or "right"
            left = further left bound of object
            right = further right bound of object
        """
        l: int
        r: int
        l, _ = self.pos
        r = l + self.size[0]
        if direction == 'left':
            return False if right < l else True
        else:
            return False if left > r else True

    @staticmethod
    def chose_direction() -> str:
        """
        Randomly choses a direction - either left or right.
        """
        if random.randint(1, 2) == 1:
            return "left"
        else:
            return "right"
