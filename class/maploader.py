import os
import pygame
from pygame import color
from pygame.locals import *
from pygame.transform import threshold
from itertools import combinations 
import numpy as np

PLATFORM_SPEC_LIST = {
    1: [((-100,510),(1024,510),(1024,579),(0,579))],
    2: [((-100,460),(1024,460),(1024,579),(0,579))],
    3: [((-100,460),(1024,460),(1024,579),(0,579))],
    4: [((-100,460),(1024,460),(1024,579),(0,579))],
    5: [((-100,460),(1024,460),(1024,579),(0,579))],
    6: [((-100,460),(1024,460),(1024,579),(0,579))],
    7: [((-100,460),(1024,460),(1024,579),(0,579))],
    8: [((-100,460),(1024,460),(1024,579),(0,579))]
}

MAP_START_POS = {
    1: [4,10],
    2: [10,420]
}

class Map():
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game
        self.pf_list = PLATFORM_SPEC_LIST.get(self.game.scene)
        self.start_pos = MAP_START_POS.get(self.game.scene)
        bg_path = os.path.join('bin','resources','map',f'{self.game.scene}.png')
        self.current_bg = pygame.image.load(bg_path)
        self.platforms = self.load_platforms()

    def load_platforms(self):
        platforms = pygame.sprite.Group()
        for pf_spec in self.pf_list:
            platforms.add(platform(pf_spec, self.game))
        return platforms
    
    def change_scene(self):
        self.pf_list = PLATFORM_SPEC_LIST.get(self.game.scene)
        self.start_pos = MAP_START_POS.get(self.game.scene)
        bg_path = os.path.join('bin','resources','map',f'{self.game.scene}.png')
        self.current_bg = pygame.image.load(bg_path)
        self.platforms = self.load_platforms()


class platform(pygame.sprite.Sprite):
    def __init__(self, pf_spec, game) -> None:
        super().__init__()
        self.image = pygame.Surface(self._get_rect_size(pf_spec)).convert_alpha()
        self.image.set_colorkey((255,0,0))
        self.image.fill((255, 0, 0))
        self.rect = pygame.draw.polygon(game.displaysurface, (255,255,255), pf_spec)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask.fill()
        self.coords = self._setup_coords(pf_spec)
        
        # Leaving this here in case there is something I'm missing with the above line of code
        #self.image = pygame.Surface(pf_spec[0])
        #self.surf.fill((255,255,255))
        #self.rect = self.surf.get_rect(center = pf_spec[1])
        #self.rect.topleft = pf_spec[2]
        #self.mask = pygame.mask.from_surface(self.image)

    def _get_rect_size(self, pf_spec):
        res = np.abs([(b1 - a1, b2 - a2) for (a1, a2), (b1, b2) in combinations(pf_spec, 2)])
        
        return (max(coord[0] for coord in res), max(coord[1] for coord in res))

    def _yhat(self, m, x, b):
        return m*x+b

    def _setup_coords(self, pf_spec):
        coords = []
        
        for i in range(len(pf_spec)):
            if i == len(pf_spec)-1:
                if pf_spec[i][0]==pf_spec[0][0]:
                    miny = min(pf_spec[i][1],pf_spec[0][1])
                    maxy = max(pf_spec[i][1],pf_spec[0][1])
                    for j in range(miny, maxy+1):
                        coords.append((pf_spec[i][0], j))
                else:
                    m = (pf_spec[i][1]-pf_spec[0][1])/(pf_spec[i][0]-pf_spec[0][0])
                    b = (pf_spec[i][0]*pf_spec[0][1]-pf_spec[0][0]*pf_spec[i][1])/(pf_spec[i][0]-pf_spec[0][0])
                    minx = min(pf_spec[i][0],pf_spec[0][0])
                    maxx = max(pf_spec[i][0],pf_spec[0][0])
                    for j in range(minx, maxx+1):
                        coords.append((j,self._yhat(m,j,b)))
            else:
                if pf_spec[i][0]==pf_spec[i+1][0]:
                    miny = min(pf_spec[i][1],pf_spec[i+1][1])
                    maxy = max(pf_spec[i][1],pf_spec[i+1][1])
                    for j in range(miny, maxy+1):
                        coords.append((pf_spec[i][0], j))
                else:
                    m = (pf_spec[i][1]-pf_spec[i+1][1])/(pf_spec[i][0]-pf_spec[i+1][0])
                    b = (pf_spec[i][0]*pf_spec[i+1][1]-pf_spec[i+1][0]*pf_spec[i][1])/(pf_spec[i][0]-pf_spec[i+1][0])
                    minx = min(pf_spec[i][0],pf_spec[i+1][0])
                    maxx = max(pf_spec[i][0],pf_spec[i+1][0])
                    for j in range(minx, maxx+1):
                        coords.append((j,self._yhat(m,j,b)))
        
        return coords