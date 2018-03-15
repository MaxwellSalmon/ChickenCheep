import random
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHTGREY = (200, 200, 200)
DARKGREEN = (0, 200, 0)

pygame.init()

class MiniGame:
    def __init__(self, width, height, x, y, foodbar):
        self.width = width
        self.height = height
        self.foodbar = int(foodbar*0.5)
        if self.foodbar < 4:
            self.foodbar = 5

        self.egg_sound = pygame.mixer.Sound('sounds//plop.ogg')
        self.egg_crack = pygame.mixer.Sound('sounds//crack.ogg')
        self.egg_error = pygame.mixer.Sound('sounds//error.ogg')
            
        self.area = pygame.Surface((self.width, self.height)).convert()
        self.rect = self.area.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.hit = pygame.Surface((random.randint(4, self.foodbar), self.height)).convert()
        self.hit_rect = self.hit.get_rect()
        self.hit_rect.x = random.randint(self.rect.left, (self.rect.right - self.hit_rect.width))
        self.hit_rect.y = y
        
        self.avoid1 = pygame.Surface((random.randint(4, self.foodbar), self.height)).convert()
        self.avoid1_rect = self.avoid1.get_rect()
        self.avoid1_rect.x = random.randint(self.rect.left, (self.rect.right - self.avoid1_rect.width))
        self.avoid1_rect.y = y

        self.avoid2 = pygame.Surface((random.randint(4, self.foodbar), self.height)).convert()
        self.avoid2_rect = self.avoid1.get_rect()
        self.avoid2_rect.x = random.randint(self.rect.left, (self.rect.right - self.avoid2_rect.width))
        self.avoid2_rect.y = y

        self.pind = pygame.Surface((2, self.height + 10)).convert()
        self.pind_rect = self.pind.get_rect()
        self.pind_rect.x = x + 1
        self.pind_rect.y = y - 5
        #Ekstra:
        self.pind_right = True
        self.pind_stop = False

        #sprites
        self.add_egg_sprite = pygame.image.load('graphics//add_egg.png').convert_alpha()
        self.sub_egg_sprite = pygame.image.load('graphics//sub_egg.png').convert_alpha()
        self.cross_sprite = pygame.image.load('graphics//cross.png').convert_alpha()

    def add_egg(self, player, canvas):
        if self.pind_rect.colliderect(self.hit_rect):
            self.egg_sound.play()
            player.egg += 1
            canvas.blit(self.add_egg_sprite, (380, 400))
        elif self.pind_rect.colliderect(self.avoid1_rect) or self.pind_rect.colliderect(self.avoid2_rect):
            if player.egg > 0:
                self.egg_crack.play()
                player.egg -= 1
                canvas.blit(self.sub_egg_sprite, (380, 400))
            else:
                self.egg_error.play()
                canvas.blit(self.cross_sprite, (380, 400))
        else:
            self.egg_error.play()
            canvas.blit(self.cross_sprite, (380, 400))
        pygame.display.update()
        pygame.time.wait(1000)

    def draw(self, canvas):
        if self.hit_rect.colliderect(self.avoid1_rect) or self.hit_rect.colliderect(self.avoid2_rect) or self.avoid1_rect.colliderect(self.avoid2_rect):
            self.hit_rect.x = random.randint(self.rect.left, (self.rect.right - self.hit_rect.width))
            self.avoid1_rect.x = random.randint(self.rect.left, (self.rect.right - self.avoid1_rect.width))
            self.avoid2_rect.x = random.randint(self.rect.left, (self.rect.right - self.avoid2_rect.width))
        
        self.area.fill(LIGHTGREY)
        canvas.blit(self.area, self.rect)
        
        self.hit.fill(DARKGREEN)
        canvas.blit(self.hit, self.hit_rect)

        self.avoid1.fill(RED)
        canvas.blit(self.avoid1, self.avoid1_rect)

        if self.foodbar < 40:
            self.avoid2.fill(RED)
            canvas.blit(self.avoid2, self.avoid2_rect)
        else:
            self.avoid2_rect.x = 9999

        self.pind.fill(BLUE)
        canvas.blit(self.pind, self.pind_rect)

    def move(self):
        if self.pind_stop == False:
            if self.pind_right == True:
                if self.pind_rect.right > self.rect.right:
                    self.pind_right = False
            elif self.pind_right == False:
                if self.pind_rect.left < self.rect.left:
                    self.pind_right = True

            if self.pind_right == True:
                self.pind_rect.x += 3
            else:
                self.pind_rect.x -= 3
        stopkey = pygame.key.get_pressed()
        if stopkey[pygame.K_RCTRL]:
            self.pind_stop = True
        
    
        

        
        
        
        
