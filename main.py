import pygame
import sys

from settings import *
from level import Level
from menu import *


# Game class
class Game:
    def __init__(self):
        self.status = 'level'
        self.level = Level(screen)

        # self.menu = Menu(screen, "Game Name",
        #                  [
        #                      Button(screen, self.create_level,
        #                             "Start", 200, 50),
        #                      Button(screen, self.create_level,
        #                             "Settings", 200, 50),
        #                      Button(screen, self.create_level,
        #                             "Credits", 200, 50),
        #                      Button(screen, self.create_level,
        #                             "Quit", 200, 50),
        #                  ])

    def create_menu(self):
        self.status = 'menu'
        self.menu = Menu(screen, "Game Name",
                         [
                             Button(screen, self.create_level,
                                    "Start", 200, 50),
                             Button(screen, self.create_level,
                                    "Settings", 200, 50),
                             Button(screen, self.create_level,
                                    "Credits", 200, 50),
                             Button(screen, self.create_level,
                                    "Quit", 200, 50),
                         ])

    def create_level(self):
        self.status = 'level'
        self.level = Level(screen)

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        if self.status == 'menu':
            self.menu.run()
        else:
            self.level.run()


        # Setup
pygame.init()

pygame.display.set_caption("The nucleus of the cell")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game = Game()
clock = pygame.time.Clock()


# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    game.run()

    pygame.display.update()
    clock.tick(60)
