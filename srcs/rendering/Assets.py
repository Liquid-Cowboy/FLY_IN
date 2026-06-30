#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join
from pygame import Surface
import pygame


class Assets():
    def __init__(self):
        self.clouds = {}
        self.buttons = {
            'text_box': {},
            'play': {},
            'custom': {},
            'options': {},
            'quit': {}
        }
        self.logo: Surface
        self.drone: Surface
        self.hubs = {}

    def load_imgs(self, img_dir: str):
        files: list[str] = [f for f in listdir(img_dir)
                            if isfile(join(img_dir, f))]

        button_map = {
            'medium_button': ['options', 'quit'],
            'large_button': ['custom'],
            'text_box': ['text_box'],
            'play_button': ['play'],
        }

        for filename in files:
            f_path: str = join(img_dir, filename)
            if "cloud" in filename:
                self.clouds[filename] = self.get_image(f_path, 5)
                continue

            for pattern, buttons in button_map.items():
                if pattern in filename:
                    type: str = filename.split('_')[-1].removesuffix('.png')
                    image: Surface = self.get_image(f_path, 5)

                    for button in buttons:
                        self.buttons[button][type] = image

            if "logo" in filename:
                self.logo = self.get_image(f_path)

            if "drone" in filename:
                self.drone = self.get_image(f_path, 5)

            if 'hub' in filename:
                color: str = filename.split('_')[-1].removesuffix('.png')
                self.hubs[color] = self.get_image(f_path, 5)

    def get_image(self, img_path: str,
                  scale_by: int | None = None) -> Surface:
        img: Surface = pygame.image.load(img_path).convert_alpha()
        if scale_by is None:
            return img
        else:
            return pygame.transform.scale_by(img, scale_by)
