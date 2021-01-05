import os
import sys

from spritesheet import SpriteSheet
import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game
        self.surf = pygame.Surface((16,16))
        self.player_state = 0.
        self.num_anim = 2
        self.can_move = 1
        self.player_act = 'standing_right'
        ss_path = os.path.join('bin','resources','player',f'player_{self.player_act}.png')
        self.player_ss = SpriteSheet(ss_path)
        rect = (0,0,32,32)
        self.player_frames = self.player_ss.load_strip(rect, self.num_anim)
        self.image = self.player_frames[int(self.player_state)]
        self.rect = self.surf.get_rect()

        self.pos = self.game.vec((self.game.map.start_pos[0],self.game.map.start_pos[1]-10))
        self.vel = self.game.vec(0,0)
        self.acc = self.game.vec(0,0)

    def update(self):
        hits = pygame.sprite.spritecollide(self, self.game.ground, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0

    def jump(self):
        hits = pygame.sprite.spritecollide(self, self.game.ground, False)
        if hits:
            self.vel.y = -5

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        self.acc = self.game.vec(0,0.5)
            
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.acc.x += -self.game.ACC
            self.num_anim = 5
            self.player_act = 'running_left'
            image_path = os.path.join('bin','resources','player',f'player_{self.player_act}.png')
            self.player_ss = SpriteSheet(image_path)
            rect = (0,0,32,32)
            self.player_frames = self.player_ss.load_strip(rect, self.num_anim )
            self.image = self.player_frames[int(self.player_state)]

        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.acc.x += self.game.ACC
            self.num_anim = 5
            self.player_act = 'running_right'
            image_path = os.path.join('bin','resources','player',f'player_{self.player_act}.png')
            self.player_ss = SpriteSheet(image_path)
            rect = (0,0,32,32)
            self.player_frames = self.player_ss.load_strip(rect, self.num_anim )
            self.image = self.player_frames[int(self.player_state)]

        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.num_anim = 4
            self.jump()
            if self.player_state >= self.num_anim:
                self.player_state = 0.  
            self.direction = self.player_act.split('_')[1]
            self.player_act = f'jumping_{self.direction}'
            image_path = os.path.join('bin','resources','player',f'player_{self.player_act}.png')
            self.player_ss = SpriteSheet(image_path)
            rect = (0,0,32,32)
            self.player_frames = self.player_ss.load_strip(rect, self.num_anim )
            self.image = self.player_frames[int(self.player_state)]

        if self.pos.x > self.game.screen_width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.game.screen_width

        self.player_state += 0.15
        if self.player_state >= self.num_anim:
            self.player_state = 0.

        self.acc.x += self.vel.x * self.game.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)