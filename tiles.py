import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y, color="purple"):
        """ 
        Constructor. 

        Args:
            size (int): Size of the tile
            x (int): x position
            y (int): y position

        """
        super().__init__()
        self.size = size
        self.pos = (x, y)
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass


class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface
