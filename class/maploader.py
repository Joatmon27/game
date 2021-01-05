import os
import pygame
from pygame.locals import *

PLATFORM_SPEC_LIST = {
    1: [[(176,50),(88,405)],[(192,40),(411,380)],[(176,50),(712,405)]]
}

MAP_START_POS = {
    1: [0,380]
}

class Map():
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game
        self.pf_list = PLATFORM_SPEC_LIST.get(self.game.scene)
        self.start_pos = MAP_START_POS.get(self.game.scene)
        bg_path = os.path.join('bin','resources','map',f'{self.game.scene}.gif')
        self.current_bg = pygame.image.load(bg_path)
        self.platforms = self.load_platforms()

    def load_platforms(self):
        platforms = pygame.sprite.Group()
        for pf_spec in self.pf_list:
            platforms.add(platform(pf_spec))
        return platforms

class platform(pygame.sprite.Sprite):
    def __init__(self, pf_spec) -> None:
        super().__init__()
        self.surf = pygame.Surface(pf_spec[0])
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = pf_spec[1])