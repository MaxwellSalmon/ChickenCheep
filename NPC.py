import pygame
import random

pygame.init()

class AI(pygame.sprite.Sprite):
    def __init__(self, spriteList, speed, canvas, canvas_rect):
        self.got = False
        self.sound = pygame.mixer.Sound('sounds//bok.ogg')
        
        self.flipped = False
        self.hak_sprite = False
        self.hak_timer = 0
        self.hak_timer_max = 20
        self.stationary = False
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.distance = random.randint(5, 80)
        self.distance_timer = 0
        
        self.speed = speed
        self.spriteList = spriteList
        self.canvas = canvas
        self.canvas_rect = canvas_rect
        
        self.sprites = len(self.spriteList)
        self.current_frame = 0
        self.timer = 0
        self.frame_duration = 150
        self.hak = pygame.image.load('graphics//NPCchicken_hak.png').convert_alpha()
        self.sprite = pygame.image.load(self.spriteList[self.current_frame]).convert_alpha()
        self.rect = self.sprite.get_rect(center = self.canvas_rect.center)
        
    def draw(self, dt, goal, goal_pos, goal_rect):
        self.sprite = pygame.image.load(self.spriteList[self.current_frame]).convert_alpha()
        self.timer += dt
        self.rect.clamp_ip(self.canvas_rect)
        if self.hak_sprite == False:
            if self.up == True or self.down == True or self.right == True or self.left == True:
                if self.timer >= self.frame_duration:
                    self.current_frame = (self.current_frame +1) % self.sprites
                    self.timer = 0
        else:
            self.sprite = self.hak
            self.stationary = True
            self.hak_timer += 1
            if self.hak_timer == self.hak_timer_max:
                self.hak_sprite = False
                self.hak_timer = 0
        if goal == False:
            if self.up == False and self.down == False and self.right == False and self.left == False and self.stationary == False:
                self.valg = random.randrange(6)
                if self.valg == 0:
                    self.up = True
                elif self.valg == 1:
                    self.down = True
                elif self.valg == 2:
                    self.right = True
                elif self.valg == 3:
                    self.left = True
                else:
                    self.stationary = True
            elif self.up == True:
                self.rect.y -= self.speed
                self.distance_timer += 1
            elif self.down == True:
                self.rect.y += self.speed
                self.distance_timer += 1
            elif self.right == True:
                self.flipped = True
                self.rect.x += self.speed
                self.distance_timer += 1
            elif self.left == True:
                self.flipped = False
                self.rect.x -= self.speed
                self.distance_timer += 1
            elif self.stationary == True:
                self.distance_timer += 1
            if self.distance_timer == self.distance:
                self.distance_timer = 0
                self.distance = random.randint(5, 80)
                self.down, self.up, self.right, self.left, self.stationary = False, False, False, False, False
                
        else:
            if goal_pos[0] <= self.rect.right and goal_pos[0] >= self.rect.left:
                if goal_pos[1] > self.rect.center[1]:
                    self.rect.y += self.speed
                    self.down = True
                elif goal_pos[1] < self.rect.center[1]:
                    self.rect.y -= self.speed
                    self.up = True
            elif goal_pos[0] > self.rect.right:
                self.rect.x += self.speed
                self.right = True
                self.flipped = True
            elif goal_pos[0] < self.rect.left:
                self.rect.x -= self.speed
                self.left = True
                
            if goal_pos[1] <= self.rect.bottom and goal_pos[1] >= self.rect.top:
                if goal_pos[0] > self.rect.center[0]:
                    if self.right == False:
                        self.rect.x += self.speed
                        self.right = True
                        self.flipped = True
                elif goal_pos[0] < self.rect.center[0]:
                    if self.left == False:
                        self.rect.x -= self.speed
                        self.left = True
            elif goal_pos[1] > self.rect.bottom:
                if self.down == False:
                    self.rect.y += self.speed
                    self.down = True
            elif goal_pos[1] < self.rect.top:
                if self.up == False:
                    self.rect.y -= self.speed
                    self.up = True
                    
            if self.left == True:
                self.flipped = False                
            else:
                self.up, self.down, self.right, self.left = False, False, False, False

        if self.rect.colliderect(goal_rect):
            self.sound.play()
            self.sprite = self.hak
            self.hak_sprite = True
            self.stationary = True
            self.got = True
            
        if self.flipped == True:
            self.sprite = pygame.transform.flip(self.sprite, True, False)
        self.canvas.blit(self.sprite, self.rect)
