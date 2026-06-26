from __future__ import annotations
from typing import TYPE_CHECKING
from pygame import Surface, Rect
from setup import Config
from .Scene import Scene
from .TextBox import TextBox
from .Button import Button
from .Simulation import Simulation

if TYPE_CHECKING:
    from .Engine import Engine

V_GAP: int = 30
LOGO_TOP: int = 120


class MainMenu(Scene):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine)

        self.window = engine.window
        self.button_font = engine.font
        button_font = engine.font

        self.logo = engine.assets.logo
        self.logo_rect = engine.assets.logo.get_rect()
        logo_w = self.logo.get_size()[0]
        self.logo_rect.topleft = (engine.window.width // 2 -
                                  logo_w // 2, LOGO_TOP)

        text_box_imgs = engine.assets.buttons['text_box']
        play_imgs = engine.assets.buttons['play']
        custom_imgs = engine.assets.buttons['custom']
        options_imgs = engine.assets.buttons['options']
        quit_imgs = engine.assets.buttons['quit']

        text_rect: Rect = text_box_imgs['base'].get_rect()
        play_rect: Rect = play_imgs['base'].get_rect()
        custom_rect: Rect = custom_imgs['base'].get_rect()
        options_rect: Rect = options_imgs['base'].get_rect()
        quit_rect: Rect = quit_imgs['base'].get_rect()

        text_rect.topleft = (
            self.logo_rect.left,
            self.logo_rect.bottom + V_GAP)

        play_rect.topright = (
            self.logo_rect.right,
            self.logo_rect.bottom + V_GAP)

        custom_rect.topleft = (
            text_rect.left,
            text_rect.bottom + V_GAP)

        options_rect.topleft = (
            custom_rect.left,
            custom_rect.bottom + V_GAP)

        quit_rect.topright = (
            custom_rect.right,
            custom_rect.bottom + V_GAP)

        white: tuple[int, int, int] = (255, 255, 255)
        dark_gray: tuple[int, int, int] = (100, 100, 100)

        text_box_text: Surface = button_font.render('/ FILENAME',
                                                    True,
                                                    dark_gray)

        custom_text: Surface = button_font.render('CUSTOM',
                                                  True, white)

        options_text: Surface = button_font.render('OPTIONS', True, white)

        quit_text: Surface = button_font.render('QUIT', True, white)

        self.text_box = TextBox(text_box_imgs['base'],
                                text_box_imgs['highlight'],
                                text_box_imgs['bottom'],
                                text_rect,
                                text_box_text,
                                button_font)

        self.play = Button(play_imgs['base'],
                           play_imgs['highlight'],
                           play_imgs['bottom'],
                           play_rect)

        self.custom = Button(custom_imgs['base'],
                             custom_imgs['highlight'],
                             custom_imgs['bottom'],
                             custom_rect,
                             custom_text)

        self.options = Button(options_imgs['base'],
                              options_imgs['highlight'],
                              options_imgs['bottom'],
                              options_rect,
                              options_text)

        self.quit = Button(quit_imgs['base'],
                           quit_imgs['highlight'],
                           quit_imgs['bottom'],
                           quit_rect,
                           quit_text)

        self.buttons = [self.text_box, self.play,
                        self.custom, self.options, self.quit]

        self.error: Surface | None = None
        self.error_timer: float = 0
        self.error_alpha: int = 255

    def handle_event(self, event):
        self.text_box.check_click(event)
        self.text_box.write_text(event)
        self.custom.check_click(event)

        if self.play.check_click(event):
            config: Config | None = self.run_filename(self.text_box.input_text)
            if config:
                self.engine.change_scene(Simulation(self.engine, config))
        if self.options.check_click(event):
            pass

        if self.quit.check_click(event):
            self.engine.running = False

    def update(self, dt: float) -> None:

        self.error_timer += dt

        if self.error_timer > 2 and self.error is not None:
            self.error_alpha -= 5
            if self.error_alpha <= 0:
                self.error = None

    def draw(self, screen: Surface):
        self.window.screen.blit(self.logo, self.logo_rect)

        for button in self.buttons:
            button.hover()
            button.draw(self.window.screen)

        self.display_error_msg()

    def display_error_msg(self) -> None:
        if not self.error:
            return
        self.error.set_alpha(self.error_alpha)
        self.window.screen.blit(self.error, self.error_rect)

    def run_filename(self, filename: str) -> None | Config:
        config = Config(filename)
        if config.error:
            self.error = self.button_font.render(config.error.upper(),
                                                 True, (255, 0, 0))
            self.error_alpha = 255
            self.error_rect = self.error.get_rect()
            self.error_rect.bottomright = (self.window.screen_rect.right - 20,
                                           self.window.screen_rect.bottom - 20)
            self.error_timer = 0
        else:
            return config
