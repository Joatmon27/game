import pygame
import sys
from pygame.locals import *
import time

sys.path.append('class')

from player import Player
from maploader import Map

pygame.init()

class RPG():
    """
    Main game class initialization. All other class references point to this class as "game"
    """
    def __init__(self) -> None:
        super().__init__()

        self.screen_width = 800
        self.screen_height = 600

        self.displaysurface = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.vec = pygame.math.Vector2
        self.ACC = 0.5
        self.FRIC = -0.12

        self.FPS = 60

        self.FramePerSec = pygame.time.Clock()

        pygame.display.set_caption("Game")


        self.scene = 1
        self.map = Map(self)

        self.player = Player(self)

        self.ground = self.map.platforms

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.ground)
        self.all_sprites.add(self.player)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.player.move()
            self.player.update()

            self.displaysurface.blit(self.map.current_bg, (0,0))
            self.player.draw(self.displaysurface)

            pygame.display.update()
            self.FramePerSec.tick(self.FPS)

            if self.player.rect.top > self.screen_height:
                for entity in self.all_sprites:
                    entity.kill()
                    time.sleep(1)
                    self.displaysurface.fill((255,0,0))
                    pygame.display.update()
                    time.sleep(1)
                    pygame.quit()
                    sys.exit()

RPG()
