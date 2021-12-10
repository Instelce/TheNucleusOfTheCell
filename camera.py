import pygame

from settings import *


class Camera(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        x = -target.rect.center[0] + SCREEN_WIDTH / 2
        y = -target.rect.center[1] + SCREEN_HEIGHT / 2

        # Limit scrolling to map size
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = max(-(self.height - SCREEN_HEIGHT), y)
        self.state = pygame.Rect(x, y, self.width, self.height)
