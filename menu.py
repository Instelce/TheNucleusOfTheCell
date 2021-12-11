import pygame
import sys

from settings import *

pygame.font.init()


class Menu:
    def __init__(self, surface, title, buttons_list, background_image=None):
        """
        Constructor

        Args:
            surface (pygame.Surface)
            title (str)
            buttons_list (list): All buttons
            background_image (str): Path of the background image

        """
        self.title = title
        self.display_surface = surface

        # Buttons
        self.button_gap = 60
        self.buttons_list = buttons_list
        print(self.buttons_list)

        # Background
        if background_image != None:
            self.background = pygame.image.load(background_image)
        else:
            self.background = None

    def draw_title(self):
        title_font = get_font(80)
        title_surf = title_font.render(self.title, True, "#FFFFFF")
        title_rect = title_surf.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))
        self.display_surface.blit(title_surf, title_rect)

    def position_buttons(self):
        is_repositioned = False
        if not is_repositioned:
            temp_pos = self.buttons_list[0].pos
            for i in range(len(self.buttons_list)):
                button = self.buttons_list[i]
                button_pos = list(button.pos)
                button_pos[1] = temp_pos[1] + self.button_gap * i
                button.pos = tuple(button_pos)
                is_repositioned = True

    def draw_buttons(self):
        for button in self.buttons_list:
            button.draw(button.pos)

    def run(self):
        if self.background != None:
            self.display_surface.blit(self.background, (0, 0))

        self.draw_buttons()
        self.position_buttons()
        self.draw_title()


class Button:
    def __init__(self, surface, callback, text, width, height, default_image='graphics/button/default.png', hover_image='graphics/button/hover.png', pos=None):
        super().__init__()
        self.width = width
        self.height = height
        self.display_surface = surface
        self.text = text
        self.callback = callback
        self.default_image = default_image
        self.hover_image = hover_image

        # If the button is on a menu or not
        if pos != None:
            self.pos = pos
        else:
            self.pos = ((SCREEN_WIDTH / 2) - int(width /
                                                 2), (SCREEN_HEIGHT / 2) - int(height / 2))

        # Font and colors
        self.font = get_font(30)
        self.image = pygame.image.load(self.default_image).convert_alpha()

        # Rect
        self.rect = self.image.get_rect(topleft=self.pos)

        # Text
        self.text_surf = self.font.render(text, True, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            # Change color of button on hover
            self.image = pygame.image.load(self.hover_image).convert_alpha()
            self.display_surface.blit(self.image, self.rect)
            self.display_surface.blit(self.text_surf, self.text_rect)

            if pygame.mouse.get_pressed()[0]:
                print('CLICK')
                print(self.text)
                self.callback()
        else:
            self.image = pygame.image.load(self.default_image).convert_alpha()
            self.display_surface.blit(self.image, self.rect)
            self.display_surface.blit(self.text_surf, self.text_rect)

    def draw(self, pos):
        # Update rect end text
        self.rect = self.image.get_rect(topleft=self.pos)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        # Draw rext and text
        self.display_surface.blit(self.image, self.rect)
        self.display_surface.blit(self.text_surf, self.text_rect)

        self.check_click()
