import pygame

from settings import *


class UI:
    def __init__(self, surface):
        self.display_surface = surface

        # Didactitiel
        self.text_index = 0
        self.texts_list = [
            "Hey, so you're the cell in our body that no longer has a nucleus.",
            "I can't help you now",
            "But try to find your nucleus quickly so that our body can come back to life.",
            "Good luck..."
        ]
        self.is_pressed = False

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.text_index < len(self.texts_list) and not self.is_pressed:
                self.text_index += 1
                self.is_pressed = True
        elif keys[pygame.K_p]:
            pass

    def show_paragraphs(self, texts_list):
        keys = pygame.key.get_pressed()
        font = get_font(30)

        text_pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)

        text_surf = font.render(texts_list[self.text_index], False, "#FFFFFF")
        text_rect = text_surf.get_rect(center=text_pos)
        self.display_surface.blit(text_surf, text_rect)

    def show(self):
        self.input()
        self.show_paragraphs(self.texts_list)
