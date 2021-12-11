import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

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
        self.setup_player(import_csv_layout(self.level_data['player']))

        # Terrain setup
        self.shadow_tile = self.create_tile_group(
            import_csv_layout(self.level_data['shadow']), 'shadow')
        self.wall_tiles = self.create_tile_group(
            import_csv_layout(self.level_data['wall']), 'wall')
        ground_layout = import_csv_layout(self.level_data['ground'])
        self.ground_tile = self.create_tile_group(ground_layout, 'ground')

        # Camera
        total_level_width = len(ground_layout[0]) * TILE_SIZE
        total_level_height = len(ground_layout) * TILE_SIZE
        self.camera = Camera(total_level_width, total_level_height)

        # Light effect
        self.black_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.black_surface.fill("black")

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if type == 'wall':
                        wall_tiles_list = import_cut_graphics(
                            'graphics/terrain/wall.png')
                        tile_surface = wall_tiles_list[int(val)]
                        sprite = StaticTile(TILE_SIZE, x, y, tile_surface)
                    elif type == 'ground':
                        ground_tile_list = import_cut_graphics(
                            'graphics/terrain/ground.png')
                        tile_surface = ground_tile_list[int(val)]
                        sprite = StaticTile(TILE_SIZE, x, y, tile_surface)
                    elif type == 'shadow':
                        shadow_tile_list = import_cut_graphics(
                            'graphics/terrain/shadow.png')
                        tile_surface = shadow_tile_list[int(val)]
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

    def player_collision(self, tiles):
        player = self.player.sprite
        player.rect.centerx += player.direction.x * player.speed
        player.rect.centery += player.direction.y * player.speed

        for tile in tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = tile.rect.bottom
                    player.direction.y = 0

                if player.direction.x < 0:
                    player.rect.left = tile.rect.right
                    player.direction.x = 0
                elif player.direction.x > 0:
                    player.rect.right = tile.rect.left
                    player.direction.x = 0

                if player.direction.x < 0 and player.direction.y > 0 or player.direction.x > 0 and player.direction.y < 0 or player.direction.x > 0 and player.direction.y > 0 or player.direction.x < 0 and player.direction.y < 0:
                    player.direction.y = 0
                    player.direction.x = 0

    def render_light(self):
        light_mask = self.player.sprite.light_mask
        light_rect = self.player.sprite.light_rect

        self.black_surface.fill('black')
        light_rect.center = self.camera.apply(self.player.sprite).center

        self.black_surface.blit(light_mask, light_rect)
        self.display_surface.blit(
            self.black_surface, (0, 0), special_flags=pygame.BLEND_MULT)

    def run(self):
        self.camera.update(self.player.sprite)

        # Terrain
        for tile in self.ground_tile:
            self.display_surface.blit(tile.image, self.camera.apply(tile))
        self.ground_tile.update()
        for tile in self.wall_tiles:
            self.display_surface.blit(tile.image, self.camera.apply(tile))

        # Player
        self.player.update()
        self.player_collision(self.wall_tiles)
        for sprite in self.player:
            self.display_surface.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.nucleus:
            self.display_surface.blit(sprite.image, self.camera.apply(sprite))

        self.render_light()

        # Shadow
        # for tile in self.shadow_tile:
        #     self.display_surface.blit(tile.image, self.camera.apply(tile))
