import pygame
from pygame.locals import *

import os
import random

from spritesheet import SpriteSheet

CREATURE_SPEC_LIST = {
    'cat': [(80,49)],
    'dog': [(80,56)],
    'stork':[(200,180)],
    'dad':[(100,180)],
    'mom':[(130,150)],
    'isabella':[(70,50)],
}

class Creature(pygame.sprite.Sprite):
    def __init__(self, game, creature):
        super().__init__()
        self.creature = creature
        self.direction = random.randint(0,1) 
        self.creature_state = 0.
        self.game = game
        self.creature_surf_size = CREATURE_SPEC_LIST.get(self.creature)[0]
        self.surf = pygame.Surface(self.creature_surf_size)
        self.rect = self.surf.get_rect()

        self.first_hit_y = self.game.map.start_pos[1]

        self.pos = self.game.vec(0,0)
        self.vel = self.game.vec(0,0)
        self.acc = self.game.vec(0,0)

        self.animate()
        
        self.vel.x = 1

        if self.direction == 0:
            self.pos.x = random.randint(100,600)
            self.pos.y = 510
        if self.direction == 1:
            self.pos.x = random.randint(600,900)
            self.pos.y = 510

    def move(self):
        
        self.acc = self.game.vec(0,0.5)

        # Causes the enemy to change directions upon reaching the end of screen    
        if self.pos.x >= (self.game.screen_width-20):
                self.direction = 1
        elif self.pos.x <= self.creature_surf_size[0]:
                self.direction = 0

        self.animate()

        self.creature_state += 0.15
        if self.creature_state >= self.num_anim:
            self.creature_state = 0.

        self.acc.x += self.vel.x * self.game.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        self.rect.bottomright = self.pos 

    def maskcollide(self, ground_collection):
        for ground in ground_collection:
            collision_point = pygame.sprite.collide_mask(ground, self)
            if collision_point and ground.mask.get_at(collision_point) > 0:
                self.current_ground = ground
                return collision_point

    def animate(self):
        self.num_anim = 3

        if self.direction == 0:
            self.acc.x += self.game.ACC
            image_path = os.path.join('bin','resources','creatures',f'{self.creature}_walking_right.png')
        else:         
            self.acc.x += -self.game.ACC
            image_path = os.path.join('bin','resources','creatures',f'{self.creature}_walking_left.png')

        self.player_ss = SpriteSheet(image_path)
        rect = (0,0,CREATURE_SPEC_LIST.get(self.creature)[0][0],CREATURE_SPEC_LIST.get(self.creature)[0][1])
        self.player_frames = self.player_ss.load_strip(rect, self.num_anim )
        self.image = self.player_frames[int(self.creature_state)]

    def update(self):
        hits_2 = self.maskcollide(self.game.ground)

        if self.vel.y > 0.5:
            if hits_2:
                new_ys = [y for x,y in self.current_ground.coords if x == int(self.pos.x)]
                if new_ys and min(new_ys) < self.pos.y+5:
                    self.vel.y = 0
                if self.first_hit_y >= self.pos.y-1 and self.first_hit_y <= self.pos.y:
                    self.pos.y = self.first_hit_y
                else:
                    self.first_hit_y = self.pos.y
        elif hits_2 and self.vel.y >= 0:
            new_ys = [y for x,y in self.current_ground.coords if x == int(self.pos.x)]
            if new_ys and min(new_ys) < self.pos.y+5:
                self.pos.y = min(new_ys)
                self.last_y = self.pos.y
                self.vel.y = 0
            elif new_ys is None:
                self.pos.y = self.last_y
                self.vel.y = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Stork(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.creature = 'stork'
        self.direction = random.randint(0,1) 
        self.creature_state = 0.
        self.game = game
        self.creature_surf_size = CREATURE_SPEC_LIST.get(self.creature)[0]
        self.surf = pygame.Surface(self.creature_surf_size)
        self.rect = self.surf.get_rect()
        self.num_anim = 10

        self.first_hit_y = self.game.map.start_pos[1]

        self.pos = self.game.vec(0,0)
        self.vel = self.game.vec(0,0)

        self.animate()
        
        self.vel.x = 3

        self.pos.x = 0
        self.pos.y = 150

    def move(self):
        
        self.animate()

        self.creature_state += 0.3
        if self.creature_state >= self.num_anim:
            self.creature_state = 0.

        self.pos += self.vel
        
        self.rect.bottomright = self.pos 

    def animate(self):        
        self.num_anim = 10
        image_path = os.path.join('bin','resources','creatures',f'stork_flying_right.png')
        self.player_ss = SpriteSheet(image_path)
        rect = (0,0,200,180)
        self.player_frames = self.player_ss.load_strip(rect, self.num_anim, colorkey=(255,255,255))
        self.image = self.player_frames[int(self.creature_state)]# Updates rect

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Dad(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.creature = 'dad'
        self.creature_state = 0.
        self.direction = 1
        self.game = game
        self.creature_surf_size = CREATURE_SPEC_LIST.get(self.creature)[0]
        self.surf = pygame.Surface(self.creature_surf_size)
        self.rect = self.surf.get_rect()
        self.num_anim = 12

        self.pos = self.game.vec(0,0)
        self.vel = self.game.vec(0,0)

        self.animate()
        
        self.vel.x = 2

        self.pos.x = 1024
        self.pos.y = 510

    def move(self):
        
        self.animate()

        # Causes the enemy to change directions upon reaching the end of screen    
        if self.pos.x >= (self.game.screen_width-20):
                self.direction = 1
        elif self.pos.x <= self.creature_surf_size[0]:
                self.direction = 0

        self.creature_state += 0.3
        if self.creature_state >= self.num_anim:
            self.creature_state = 0.

        if self.direction == 1:
            self.pos -= self.vel
        else:
            self.pos += self.vel
        
        self.rect.bottomright = self.pos 

    def animate(self):        
        self.num_anim = 12

        if self.direction == 0:
            image_path = os.path.join('bin','resources','creatures',f'{self.creature}_walking_right.png')
        else:         
            image_path = os.path.join('bin','resources','creatures',f'{self.creature}_walking_left.png')

        self.player_ss = SpriteSheet(image_path)
        rect = (0,0,CREATURE_SPEC_LIST.get(self.creature)[0][0],CREATURE_SPEC_LIST.get(self.creature)[0][1])
        self.player_frames = self.player_ss.load_strip(rect, self.num_anim )
        self.image = self.player_frames[int(self.creature_state)]

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Isabella(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.creature = 'isabella'
        self.direction = 1 
        self.creature_state = 0.
        self.game = game
        self.creature_surf_size = CREATURE_SPEC_LIST.get(self.creature)[0]
        self.surf = pygame.Surface(self.creature_surf_size)
        self.rect = self.surf.get_rect()

        self.first_hit_y = self.game.map.start_pos[1]

        self.pos = self.game.vec(0,0)
        self.vel = self.game.vec(0,0)
        self.acc = self.game.vec(0,0)

        self.animate()
        
        self.vel.x = 0.5

        self.pos.x = 100
        self.pos.y = 510

    def move(self):
        
        self.acc = self.game.vec(0,0.5)

        self.animate()

        self.creature_state += 0.3
        if self.creature_state >= self.num_anim:
            self.creature_state = 0.
            
        if (self.pos.x > 400) and (self.game.player.pos.x < 400):
            self.direction = 0
        else:
            if self.game.player.pos.x > self.pos.x:
                self.direction = 1
                self.pos += self.vel
            elif self.game.player.pos.x < self.pos.x and self.pos.x < 400:
                self.direction = 1
                self.pos += self.vel
            else:
                self.direction = 0
        
        self.rect.bottomright = self.pos 

    def animate(self):
        if self.direction == 1:
            self.acc.x += self.game.ACC        
            self.num_anim = 10
            image_path = os.path.join('bin','resources','creatures',f'isabella_crawling_right.png')
        else:
            image_path = os.path.join('bin','resources','creatures',f'isabella_crawling_left.png')
        self.player_ss = SpriteSheet(image_path)
        rect = (0,0,70,50)
        self.player_frames = self.player_ss.load_strip(rect, self.num_anim )
        if self.direction == 1:
            self.image = self.player_frames[int(self.creature_state)]
        else:
            self.image = self.player_frames[1]

        self.rect = self.surf.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Mom(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.creature = 'mom'
        self.direction = random.randint(0,1) 
        self.creature_state = 0.
        self.game = game
        self.creature_surf_size = CREATURE_SPEC_LIST.get(self.creature)[0]
        self.surf = pygame.Surface(self.creature_surf_size)
        self.rect = self.surf.get_rect()

        self.first_hit_y = self.game.map.start_pos[1]

        self.pos = self.game.vec(0,0)
        self.vel = self.game.vec(0,0)
        self.acc = self.game.vec(0,0)

        self.animate()
        
        self.vel.x = 1

        self.pos.x = 100
        self.pos.y = 510

    def move(self):
        
        self.acc = self.game.vec(0,0.5)

        self.animate()

        self.creature_state += 0.15
        if self.creature_state >= self.num_anim:
            self.creature_state = 0.

        self.acc.x += self.vel.x * self.game.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        self.rect.bottomright = self.pos 

    def maskcollide(self, ground_collection):
        for ground in ground_collection:
            collision_point = pygame.sprite.collide_mask(ground, self)
            if collision_point and ground.mask.get_at(collision_point) > 0:
                self.current_ground = ground
                return collision_point

    def animate(self):
        self.acc.x += self.game.ACC        
        self.num_anim = 4
        image_path = os.path.join('bin','resources','creatures',f'mom_walking_transparent.png')
        self.player_ss = SpriteSheet(image_path)
        rect = (0,0,130,150)
        self.player_frames = self.player_ss.load_strip(rect, self.num_anim )
        self.image = self.player_frames[int(self.creature_state)]
        self.rect = self.surf.get_rect()

    def update(self):
        hits_2 = self.maskcollide(self.game.ground)

        if self.vel.y > 0.5:
            if hits_2:
                new_ys = [y for x,y in self.current_ground.coords if x == int(self.pos.x)]
                if new_ys and min(new_ys) < self.pos.y+5:
                    self.vel.y = 0
                if self.first_hit_y >= self.pos.y-1 and self.first_hit_y <= self.pos.y:
                    self.pos.y = self.first_hit_y
                else:
                    self.first_hit_y = self.pos.y
        elif hits_2 and self.vel.y >= 0:
            new_ys = [y for x,y in self.current_ground.coords if x == int(self.pos.x)]
            if new_ys and min(new_ys) < self.pos.y+5:
                self.pos.y = min(new_ys)
                self.last_y = self.pos.y
                self.vel.y = 0
            elif new_ys is None:
                self.pos.y = self.last_y
                self.vel.y = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)