import os
import sys

from spritesheet import SpriteSheet
import pygame
from pygame.locals import *
import operator

class Player(pygame.sprite.Sprite):
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game
        self.surf = pygame.Surface((60,80))
        self.player_state = 0.
        self.num_anim = 4
        self.can_move = 1
        self.player_act = 'standing_right'
        self.direction = self.player_act.split('_')[1]
        ss_path = os.path.join('bin','resources','player',f'elizabeth_{self.player_act}.png')
        self.player_ss = SpriteSheet(ss_path)
        rect = (0,0,60,80)
        self.player_frames = self.player_ss.load_strip(rect, self.num_anim)
        self.image = self.player_frames[int(self.player_state)]
        self.rect = self.surf.get_rect()

        self.pos = self.game.vec((self.game.map.start_pos[0],self.game.map.start_pos[1]))
        self.vel = self.game.vec(0,0)
        self.acc = self.game.vec(0,0)

    def jump(self):
        self.rect.x += 1
    
        # Check to see if payer is in contact with the ground
        hits = pygame.sprite.spritecollide(self, self.game.ground, False)
        
        self.rect.x -= 1
    
        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12

    def gravity_check(self):
        hits = pygame.sprite.spritecollide(self ,self.game.ground, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        self.acc = self.game.vec(0,0.5)
            
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.acc.x += -self.game.ACC
            self.num_anim = 6
            self.player_act = 'running_left'
            image_path = os.path.join('bin','resources','player',f'elizabeth_{self.player_act}.png')
            self.player_ss = SpriteSheet(image_path)
            rect = (0,0,60,80)
            self.player_frames = self.player_ss.load_strip(rect, self.num_anim )
            self.image = self.player_frames[int(self.player_state)]

        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.acc.x += self.game.ACC            
            self.num_anim = 6
            self.player_act = 'running_right'
            image_path = os.path.join('bin','resources','player',f'elizabeth_{self.player_act}.png')
            self.player_ss = SpriteSheet(image_path)
            rect = (0,0,60,80)
            self.player_frames = self.player_ss.load_strip(rect, self.num_anim )
            self.image = self.player_frames[int(self.player_state)]

        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.num_anim = 6
            self.jump()
            if self.player_state >= self.num_anim:
                self.player_state = 0.  
            self.direction = self.player_act.split('_')[1]
            self.player_act = f'jumping_{self.direction}'
            image_path = os.path.join('bin','resources','player',f'elizabeth_{self.player_act}.png')
            self.player_ss = SpriteSheet(image_path)
            rect = (0,0,60,80)
            self.player_frames = self.player_ss.load_strip(rect, self.num_anim )
            self.image = self.player_frames[int(self.player_state)]

        if (not pressed_keys[K_w] and not pressed_keys[K_a] and not pressed_keys[K_s] and not pressed_keys[K_d] 
            and not pressed_keys[K_UP] and not pressed_keys[K_DOWN] and not pressed_keys[K_LEFT] and not pressed_keys[K_RIGHT] ):
            self.num_anim = 4
            self.direction = self.player_act.split('_')[1]
            self.player_act = f'standing_{self.direction}'
            ss_path = os.path.join('bin','resources','player',f'elizabeth_{self.player_act}.png')
            self.player_ss = SpriteSheet(ss_path)
            rect = (0,0,60,80)
            self.player_frames = self.player_ss.load_strip(rect, self.num_anim)
            if self.player_state >= self.num_anim:
                self.player_state = 0.  
            self.image = self.player_frames[int(self.player_state)]

        if self.pos.x >= self.game.screen_width and self.game.scene != 8:
            self.pos.x = 2
            self.game.scene += 1
            self.game.map.change_scene()
        elif self.pos.x >= self.game.screen_width:
            self.pos.x = self.game.screen_width

        if self.pos.x <= 0 and self.game.scene != 1:
            self.pos.x = self.game.screen_width - 20
            self.game.scene -= 1
            self.game.map.change_scene()
        elif self.pos.x <= 0:
            self.pos.x = 1

        self.player_state += 0.2
        if self.player_state >= self.num_anim:
            self.player_state = 0.

        self.acc.x += self.vel.x * self.game.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)