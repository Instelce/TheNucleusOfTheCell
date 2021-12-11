import pygame

from settings import *


class Camera(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.state = pygame.Rect((0, 0), (width, height))

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
        self.state.topleft += (pygame.Vector2((x, y)) -
                               pygame.Vector2(self.state.topleft)) * 0.06
        # set max/min x/y so we don't see stuff outside the world
        self.state.x = max(-(self.state.width - SCREEN_WIDTH),
                           min(0, self.state.x))
        self.state.y = max(-(self.state.height - SCREEN_HEIGHT),
                           min(0, self.state.y))
        self.state = pygame.Rect(x, y, self.width, self.height)
