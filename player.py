import pygame

from settings import *
from supports import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, surface, pos):
        super().__init__()
        self.import_cell_assets()
        self.import_light_assets()
        self.display_surface = surface

        self.frame_index = 0
        self.light_frame_index = 0
        self.animation_speed = 0.05
        self.status = 'idle'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.pos = self.rect.center

        # Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 6

        # Light
        self.light_radius = (500, 500)
        self.light_mask = self.light_animations['idle'][self.light_frame_index]
        self.light_mask = pygame.transform.scale(
            self.light_mask, self.light_radius)
        self.light_rect = self.light_mask.get_rect(center=pos)

    def import_cell_assets(self):
        cell_path = 'graphics/cell/'
        self.animations = {'idle': [], 'run': []}

        for animation in self.animations:
            full_path = cell_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_light_assets(self):
        light_path = 'graphics/light/'
        self.light_animations = {'idle': []}

        for animation in self.light_animations:
            print(import_folder(light_path))
            self.animations[animation] = import_folder(light_path)

    def animate(self):
        animation = self.animations[self.status]
        light_animation = self.light_animations['idle']

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.light_frame_index += self.animation_speed
        if self.light_frame_index >= len(light_animation):
            self.light_frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(topleft=self.pos)
        self.light_mask = light_animation[self.light_frame_index]
        self.light_rect = self.light_mask.get_rect(center=self.pos)

    def get_status(self):
        self.status = 'idle'
        # if self.direction.x == 0:
        #     self.status = 'idle'
        # elif self.direction.y == 0:
        #     self.status = 'idle'
        # elif self.direction.x > 0:
        #     self.status = 'run'
        # elif self.direction.y > 0:
        #     self.status = 'run'

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def get_direction(self, start_vec, end_vec):
        start = pygame.math.Vector2(start_vec)
        end = pygame.math.Vector2(end_vec)

        if not start == [0, 0] or not end == [0, 0]:
            return (end - start).normalize()

    def update(self):
        self.pos += self.direction * self.speed
        self.rect.center = self.pos

        self.get_input()
        self.get_status()
        self.animate()
