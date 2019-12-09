import pygame
from pygame.locals import *


class Goose(pygame.sprite.Sprite):
    start_positions = [0, 0]
    x, y = 0, 0

    def __init__(self, color, start_positions, width=22, height=22):
        super().__init__()

        self.start_positions = start_positions

        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def init_sprite_positions(self):
        self.x = self.start_positions[0]
        self.y = self.start_positions[1]

    def move(self, next_position):
        self.x = next_position[0]
        self.y = next_position[1]

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
