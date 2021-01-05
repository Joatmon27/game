import pygame
from pygame.locals import *

import os
import random

# class Enemy(pygame.sprite.Sprite):
#     def __init__(self, game) -> None:
#         super().__init__()
#         image_path = os.path.join('bin','resources','enemy_2.png')
#         self.game = game
#         self.image = pygame.image.load(image_path)
#         self.surf = pygame.Surface((49,80))
#         self.rect = self.surf.get_rect(center = (random.randint(40,self.game.screen_width - 40),0))

#     def move(self):
#         self.rect.move_ip(0,10)
#         if (self.rect.bottom > self.game.screen_height):
#             self.rect.top = 0
#             self.rect.center = (random.randint(30,370),0)

#     def draw(self, surface):
#         surface.blit(self.image, self.rect)