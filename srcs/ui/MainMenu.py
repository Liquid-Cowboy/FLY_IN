import pygame
from pygame import Surface, Rect, Font, Clock
from rendering import Window, Assets, Background
from ui import Button, TextBox
from setup import Config


class MainMenu():
    def __init__(self, window: Window, assets: Assets,
                 button_font: Font) -> None:

        self.window = window
        self.button_font = button_font

        buttons: dict[str, Surface] = assets.buttons

        v_gap: int = 30

        self.logo = assets.logo
        self.logo_rect = self.logo.get_rect()
        logo_w = self.logo.get_size()[0]
        self.logo_rect.topleft = (window.width // 2 - logo_w // 2, 120)

        text_box_imgs = self.get_button_imgs('text_box', buttons)
        play_imgs = self.get_button_imgs('play_button', buttons)
        custom_imgs = self.get_button_imgs('large_button', buttons)
        options_imgs = self.get_button_imgs('medium_button', buttons)
        quit_imgs = self.get_button_imgs('medium_button', buttons)

        text_rect: Rect = text_box_imgs['base'].get_rect()
        play_rect: Rect = play_imgs['base'].get_rect()
        custom_rect: Rect = custom_imgs['base'].get_rect()
        options_rect: Rect = options_imgs['base'].get_rect()
        quit_rect: Rect = options_imgs['base'].get_rect()

        text_rect.topleft = (
            self.logo_rect.left,
            self.logo_rect.bottom + v_gap)

        play_rect.topright = (
            self.logo_rect.right,
            self.logo_rect.bottom + v_gap)

        custom_rect.topleft = (
            text_rect.left,
            text_rect.bottom + v_gap)

        options_rect.topleft = (
            custom_rect.left,
            custom_rect.bottom + v_gap)

        quit_rect.topright = (
            custom_rect.right,
            custom_rect.bottom + v_gap)

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

    @staticmethod
    def get_button_imgs(button_type: str, button_dict: dict):
        base = button_dict.get(button_type +
                               '_base.png', Surface((243, 60))).copy()
        highlight = button_dict.get(button_type +
                                    '_highlight.png',
                                    Surface((243, 60))).copy()
        bottom = button_dict.get(button_type +
                                 '_bottom.png', Surface((243, 60))).copy()

        return {
            'base': base,
            'highlight': highlight,
            'bottom': bottom,
        }

    def main_menu(self, background: Background, clock: Clock) -> None:
        # get button imgs
        # setup button rects at the right place on the grid
        buttons = [self.text_box, self.play,
                   self.custom, self.options, self.quit]
        running: bool = True

        while running:
            self.window.screen.fill('#59e5ff')

            for event in pygame.event.get():
                if self.text_box.check_click(event):
                    pass

                if self.play.check_click(event):
                    self.run_filename(self.text_box.input_text)

                if self.options.check_click(event):
                    pass

                if self.custom.check_click(event):
                    pass

                if self.quit.check_click(event):
                    running = False

                if event.type == pygame.QUIT:
                    running = False

                self.text_box.check_click(event)
                self.text_box.write_text(event)

            dt: float = clock.tick(60) / 1000
           
            background.run_clouds(dt)
            self.window.screen.blit(self.logo, self.logo_rect)

            for button in buttons:
                button.hover()
                button.draw(self.window.screen)

            pygame.display.update()

    def display_error_msg(self, error: str) -> None:
        error_img = self.button_font.render(error, True, (255, 0, 0))
        error_rect = error_img.get_rect()
        error_rect.bottomright = (self.window.screen_rect.right - 20,
                                  self.window.screen_rect.bottom - 20)
        print('Fuck!')
        self.window.screen.blit(error_img, error_rect)


    def run_filename(self, filename: str) -> None:
        try:
            config = Config(filename)
        except Exception as e:
            self.display_error_msg(str(e))
