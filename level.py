import pygame

from settings import *
from supports import *
from tiles import *
from player import Player
from camera import Camera
from game_data import levels


class Level:
    def __init__(self, surface):
        self.display_surface = surface

        self.level_data = levels[0]

        # Player setup
        self.player = pygame.sprite.GroupSingle()
        self.nucleus = pygame.sprite.GroupSingle()

        # Terrain setup
        # self.shadow_tile = self.create_tile_group(
        #     import_csv_layout(self.level_data['shadow']), 'shadow')
        self.wall_tile = self.create_tile_group(
            import_csv_layout(self.level_data['wall']), 'wall')
        ground_layout = import_csv_layout(self.level_data['ground'])
        self.ground_tile = self.create_tile_group(ground_layout, 'ground')

        # Camera
        total_level_width = len(ground_layout[0]) * TILE_SIZE
        total_level_height = len(ground_layout) * TILE_SIZE
        self.camera = Camera(total_level_width, total_level_height)

        self.setup_player(import_csv_layout(self.level_data['player']))

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if type == 'wall':
                        wall_tile_list = import_cut_graphics(
                            'graphics/terrain/wall.png')
                        tile_surface = wall_tile_list[int(val)]
                        sprite = StaticTile(TILE_SIZE, x, y, tile_surface)
                    elif type == 'ground':
                        ground_tile_list = import_cut_graphics(
                            'graphics/terrain/ground.png')
                        tile_surface = ground_tile_list[int(val)]
                        sprite = StaticTile(TILE_SIZE, x, y, tile_surface)

                    sprite_group.add(sprite)

        return sprite_group

    def setup_player(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val == '0':
                    sprite = Player(self.display_surface, (x, y))
                    self.player.add(sprite)
                if val == '1':
                    sprite = Tile(TILE_SIZE, x, y, 'yellow')
                    self.nucleus.add(sprite)

    def apply_horizontal_movement(self):
        player = self.player.sprite
        player.rect.x = player.direction.x * player.speed

    def apply_vertical_movement(self):
        player = self.player.sprite
        player.rect.y = player.direction.y * player.speed

    def run(self):
        self.camera.update(self.player.sprite)

        # Terrain
        for tile in self.ground_tile:
            self.display_surface.blit(tile.image, self.camera.apply(tile))
        for tile in self.wall_tile:
            self.display_surface.blit(tile.image, self.camera.apply(tile))

        # Player
        self.player.update()
        self.apply_horizontal_movement()
        self.apply_vertical_movement()
        for sprite in self.player:
            self.display_surface.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.nucleus:
            self.display_surface.blit(sprite.image, self.camera.apply(sprite))
