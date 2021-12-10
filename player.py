import pygame
from supports import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, surface, pos):
        super().__init__()
        self.import_cell_assets()
        self.display_surface = surface
        self.pos = pos

        self.frame_index = 0
        self.animation_speed = 0.05
        self.status = 'idle'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 6

    def import_cell_assets(self):
        cell_path = 'graphics/cell/'
        self.animations = {'idle': [], 'run': []}

        for animation in self.animations:
            full_path = cell_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_a]:
            self.direction.x += 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_d]:
            self.direction.x -= 1
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y -= 1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y += 1

    def get_status(self):
        if self.direction.y > 0 or self.direction.y < 0:
            self.status = 'run'
        else:
            self.status = 'idle'
        if self.direction.x > 0 or self.direction.x < 0:
            self.status = 'run'
        else:
            self.status = 'idle'

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
