import pygame

TILE_SIZE = 64
WIDTH_TILE_NUMBER = 16
HEIGHT_TILE_NUMBER = 10
SCREEN_WIDTH = WIDTH_TILE_NUMBER * TILE_SIZE
SCREEN_HEIGHT = HEIGHT_TILE_NUMBER * TILE_SIZE


def get_font(size):
    return pygame.font.Font("graphics/Gamer.ttf", size)
