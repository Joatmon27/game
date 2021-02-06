import pygame
import sys
import os
from pygame.locals import *
import time
import random

sys.path.append('class')

from player import Player
from maploader import Map
from monsters import Creature, Stork, Dad, Isabella, Mom

pygame.init()

class RPG():
    """
    Main game class initialization. All other class references point to this class as "game"
    """
    def __init__(self) -> None:
        super().__init__()

        self.screen_width = 1024
        self.screen_height = 579

        self.displaysurface = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.vec = pygame.math.Vector2
        self.ACC = 0.5
        self.FRIC = -0.12

        self.FPS = 60

        self.FramePerSec = pygame.time.Clock()

        pygame.display.set_caption("Game")

        self.star_list = []
        self.text_list = []

        for i in range(100):
            x = random.randrange(0, self.screen_width)
            y = random.randrange(0, self.screen_height)
            self.star_list.append([x, y])

        self.text_list.append(['THEY TOLD ME',[self.screen_width/2, self.screen_height/2],255,4])
        self.text_list.append(["HONEY",[self.screen_width/2, self.screen_height/2],255,10])
        self.text_list.append(["YOU'RE SPECIAL",[self.screen_width/2, self.screen_height/2],255,5])
        self.text_list.append(['YOU',[self.screen_width/2-15, self.screen_height/2],255,15])
        self.text_list.append(['ARE',[self.screen_width/2+15, self.screen_height/2],255,15])
        self.text_list.append(['OUR ENTIRE WORLD',[self.screen_width/2, self.screen_height/2],255,3])
        self.text_list.append(['YOU KNOW WHAT?',[self.screen_width/2, self.screen_height/2],255,3])
        self.text_list.append(['EVEN',[self.screen_width/2-60, self.screen_height/2],255,15])
        self.text_list.append(['WITH',[self.screen_width/2-20, self.screen_height/2],255,15])
        self.text_list.append(['THINGS',[self.screen_width/2+20, self.screen_height/2],255,15])
        self.text_list.append(['CHANGING',[self.screen_width/2+60, self.screen_height/2],255,15])
        self.text_list.append(['THEY WERE RIGHT',[self.screen_width/2, self.screen_height/2],255,2])

        self.intro()

        self.fadeInSurface = pygame.Surface((self.screen_width,self.screen_height))

        self.scene = 1
        self.map = Map(self)

        self.player = Player(self)
        self.dog = Creature(self, 'dog')
        self.cat = Creature(self, 'cat')
        self.mom = Mom(self)
        self.dad = Dad(self)
        self.stork = Stork(self)
        self.isabella = Isabella(self)

        self.ground = self.map.platforms

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.ground)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.cat)
        self.all_sprites.add(self.dog)
        self.all_sprites.add(self.stork)
        self.all_sprites.add(self.dad)
        self.all_sprites.add(self.mom)
        self.all_sprites.add(self.isabella)

        self.displaysurface.set_alpha(None)

        self.game_running = True

        while self.game_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.player.move()
            self.player.gravity_check()

            self.displaysurface.blit(self.map.current_bg, (0,0))
            self.player.draw(self.displaysurface)
            
            if self.scene == 2:
                self.dog.move()
                self.dog.update()
                self.dog.draw(self.displaysurface)
            
            if self.scene == 3:
                self.cat.move()
                self.cat.update()
                self.cat.draw(self.displaysurface)
                        
            if self.scene == 5:
                self.mom.move()
                self.mom.update()
                self.mom.draw(self.displaysurface)
            
            if self.scene == 1:
                self.dad.move()
                self.dad.draw(self.displaysurface)
            
            if self.scene == 7:
                self.stork.move()
                self.stork.draw(self.displaysurface)
                self.loading()
            
            if self.scene == 8:
                self.isabella.move()
                self.isabella.draw(self.displaysurface)

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
        
        
        self.outro()
    
    def intro(self):

        pygame.font.init()
        self.intro = True
            
        font_path = os.path.join('bin','resources','assets','VictorMono','TTF','VictorMono-Medium.ttf')
        myfont = pygame.font.Font(font_path, 30)
        self.text_surfaces = []
        self.text_rects = []

        for i in range(len(self.text_list)):
            myfont.set_bold(True)
            textsurface = myfont.render(self.text_list[i][0], True, (255,255,255))
            text_rect = textsurface.get_rect()
            text_rect.midbottom = self.text_list[i][1]
            self.text_rects.append(text_rect)
            self.text_surfaces.append(textsurface)
        
        myfont.set_bold(False)

        intro_text = []

        intro_text.append(["SOMERSET WEST", [self.screen_width/2, self.screen_height/2]])
        intro_text.append(["2021", [self.screen_width/2, self.screen_height/2-30]])
        intro_text.append(["FROM THE PEOPLE THAT BROUGHT YOU PARENTHOOD", [self.screen_width/2, self.screen_height/2]])
        intro_text.append([os.path.join('bin','resources','assets',f'parenthood.png'), [self.screen_width/2, 579]])

        display_place = True
        display_intro = False
        self.text_counter = 0
        self.alpha_surf = pygame.Surface(myfont.render(self.text_list[self.text_counter][0], False, (255, 255, 255)).get_size(), pygame.SRCALPHA)
        
        self.alpha_scene_1 = 255
        self.alpha_scene_2 = 255

        while self.intro:
            self.displaysurface.fill((0,0,0))
 
            for event in pygame.event.get():   # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.intro = False   # Flag that we are done so we exit this loop

            if display_place:
                display_place, display_intro = self.scene_1(myfont, intro_text)
            
            if display_intro:
                display_intro = self.scene_2(myfont, intro_text, display_intro)
            
            if not display_intro:
                self.stars()
                self.story(myfont)

                pygame.display.flip()
                self.FramePerSec.tick(20)

    def scene_1(self, font, intro_text):
        textsurface = font.render(intro_text[0][0], False, (255, 255, 255))
        text_rect = textsurface.get_rect()
        text_rect.midbottom = (intro_text[0][1][0],intro_text[0][1][1])
        textsurface_2 = font.render(intro_text[1][0], False, (255, 255, 255))
        text2_rect = textsurface_2.get_rect()
        text2_rect.midbottom = (intro_text[1][1][0],intro_text[1][1][1])
        self.displaysurface.blit(textsurface, text_rect)
        self.displaysurface.blit(textsurface_2, text2_rect)
        pygame.display.flip()
        time.sleep(3)
        display_place = False
        display_intro = True
        return display_place, display_intro

    def scene_2(self, font, intro_text, display_intro):
        image_path = intro_text[3][0]
        logo = pygame.image.load(image_path).convert()
        logo_rect = logo.get_rect()
        logo.set_alpha(125)
        logo_rect.midbottom = (intro_text[3][1][0],intro_text[3][1][1])
        self.displaysurface.fill((0,0,0))
        self.displaysurface.blit(logo, logo_rect)
        pygame.display.flip()
        font.set_italic(True)
        font.set_bold(True)
        textsurface = font.render(intro_text[2][0], True, (255, 255, 255))
        txt_surf = textsurface.copy()
        alpha_surf = pygame.Surface(textsurface.get_size(), pygame.SRCALPHA)
        
        # Reduce alpha each frame, but make sure it doesn't get below 0.
        self.alpha_scene_2 = max(self.alpha_scene_2-2, 0)
        
        # Fill alpha_surf with this color to set its alpha value.
        alpha_surf.fill((255, 255, 255, self.alpha_scene_2))
        # To make the text surface transparent, blit the transparent
        # alpha_surf onto it with the BLEND_RGBA_MULT flag.
        txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        text3_rect = textsurface.get_rect()
        text3_rect.midbottom = (intro_text[2][1][0],intro_text[2][1][1])
        self.displaysurface.blit(txt_surf, text3_rect)
        pygame.display.flip()
        intro_text[2][1][0] += 1
        intro_text[3][1][0] -= 1
        self.FramePerSec.tick(15)
        
        if text3_rect.x >= 150:
            display_intro = False

        return display_intro

    def story(self, font):
        font.set_italic(False)
        if self.text_counter < len(self.text_list):
            txt_surf = self.text_surfaces[self.text_counter].copy()

            if self.text_list[self.text_counter][2] <= 0:
                self.text_counter += 1
                if self.text_counter <= len(self.text_list)-1:
                    self.alpha_surf = pygame.Surface(font.render(self.text_list[self.text_counter][0], False, (255, 255, 255)).get_size(), pygame.SRCALPHA)
            else:
                # Reduce alpha each frame, but make sure it doesn't get below 0.
                self.text_list[self.text_counter][2] = max(self.text_list[self.text_counter][2]-self.text_list[self.text_counter][3], 0)
                
                # Fill alpha_surf with this color to set its alpha value.
                self.alpha_surf.fill((255, 255, 255, self.text_list[self.text_counter][2]))
                # To make the text surface transparent, blit the transparent
                # alpha_surf onto it with the BLEND_RGBA_MULT flag.
                txt_surf.blit(self.alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                self.displaysurface.blit(txt_surf, self.text_rects[self.text_counter])
        else:
            self.intro = False
    
    def stars(self):
        for i in range(len(self.star_list)):
            
            image_path = os.path.join('bin','resources','assets',f'star.png')

            star = pygame.image.load(image_path)
            star_small = pygame.transform.scale(star, (10,10))
            self.displaysurface.blit(star_small, self.star_list[i])
    
            # Move the snow flake down one pixel
            self.star_list[i][1] += 1
    
            # If the snow flake has moved off the bottom of the screen
            if self.star_list[i][1] > self.screen_height:
                # Reset it just above the top
                y = random.randrange(-50, -10)
                self.star_list[i][1] = y
                # Give it a new x position
                x = random.randrange(0, self.screen_width)
                self.star_list[i][0] = x
    
    def loading(self):
        pass
    
    def outro(self):
        pass

RPG()
