#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join
from pygame import Surface
import pygame


class Assets():
    def __init__(self):
        self.clouds = {}
        self.buttons = {}
        self.logo: Surface
        self.drone: Surface

    def load_imgs(self, img_dir: str):
        files: list[str] = [f for f in listdir(img_dir)
                            if isfile(join(img_dir, f))]
        for filename in files:
            f_path: str = join(img_dir, filename)
            if "cloud" in filename:
                self.clouds[filename] = self.get_image(f_path, 5)

            if "button" in filename or "text_box" in filename:
                self.buttons[filename] = self.get_image(f_path, 5)

            if "logo" in filename:
                self.logo = self.get_image(f_path)

            if "drone" in filename:
                self.drone = self.get_image(f_path, 5)

    def get_image(self, img_path: str,
                  scale_by: int | None = None) -> Surface:
        img: Surface = pygame.image.load(img_path).convert_alpha()
        if scale_by is None:
            return img
        else:
            return pygame.transform.scale_by(img, scale_by)


if __name__ == '__main__':
    assets = Assets()
    assets.load_imgs('assets/imgs')
