from __future__ import annotations
from typing import TYPE_CHECKING
from rendering import Window, Assets, Background
from .MainMenu import MainMenu
from pygame import Clock, Font

if TYPE_CHECKING:
    from .Scene import Scene


class Engine():

    def __init__(self,
                 window_size: tuple[int, int],
                 assets_path: str,
                 font_path: str,
                 ):

        self.window: Window = Window(window_size[0], window_size[1])

        self.assets: Assets = Assets()
        self.assets.load_imgs(assets_path)

        self.font: Font = Font(font_path, 35)

        self.scene: Scene = MainMenu(self)

        self.background: Background = Background(self.window.screen)
        self.background.setup_clouds(self.assets.clouds)

        self.clock: Clock = Clock()

        self.running: bool = True

    def change_scene(self, new_scene: Scene):
        self.scene = new_scene
