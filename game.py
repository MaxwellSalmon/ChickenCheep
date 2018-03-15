import pygame, random
import minigame, text, NPC, load, menu

pygame.init()
pygame.mixer.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHTGREY = (200, 200, 200)
DARKGREEN = (0, 200, 0)

class Canvas:
    def __init__(self, width, height, file, file2):
        self.width = width
        self.height = height
        self.game = pygame.display.set_mode((self.width,self.height))
        self.rect = self.game.get_rect()
        self.file = pygame.image.load(file).convert()
        self.file2 = pygame.image.load(file2).convert_alpha()
        self.scenery = "outside"
        self.sound = pygame.mixer.Sound('sounds//bell.ogg')
        pygame.display.set_caption("Chicken Cheep")
    def draw(self):
        self.game.blit(self.file, self.rect)
    def draw2(self):
        self.game.blit(self.file2, self.rect)
    def change_background(self):
        if self.scenery == "outside":
            self.game.fill(BLACK)
            self.sound.play()
            req_egg_text.__init__(295, 100, ("Required eggs: %s" % chicken.req_egg), WHITE, "helvetica", 32)
            req_egg_text.draw(gameCanvas.game)
            nightText.draw(gameCanvas.game)
            nightGame.__init__(300, 30, 250, 450, foodBarFront.width)
            pygame.display.update()
            pygame.time.wait(2000)
            self.file = pygame.image.load('graphics//background2.png').convert()
            self.file2 = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
            timeBarFront.width += 75
            self.scenery = "inside"
        if timeBarFront.width <= 1:
            if self.scenery == "inside":
                self.game.fill(BLACK)
                self.sound.play()
                chicken.egg_highscore += chicken.egg
                if chicken.egg < chicken.req_egg:
                    if chicken.egg_highscore > load.load():
                        load.save(chicken.egg_highscore)
                    scoreText.__init__(300, 120, ("Score: %s" % chicken.egg_highscore), WHITE, "helvetica", 45)
                    scoreText.draw(gameCanvas.game)
                    highscoreText = text.Text(290, 400, ("Highscore: %s" % load.load()), WHITE, "helvetica", 45)
                    highscoreText.draw(gameCanvas.game)
                    gameOverAnim()
                else:
                    dayText.draw(gameCanvas.game)
                    chicken.egg = 0
                    chicken.req_egg += 2
                    pygame.display.update()
                    pygame.time.wait(2000)
                    self.file = pygame.image.load('graphics//background.png').convert()
                    self.file2 = pygame.image.load('graphics//hegn.png').convert_alpha()
                    timeBarFront.next_level()
                    foodBarFront.next_level()
                    timeBarFront.reset()
                    foodBarFront.reset()
                    self.scenery = "outside"
        
class Player(pygame.sprite.Sprite):
    def __init__(self, spriteList, speed):
        self.egg = 0
        self.egg_highscore = 0
        self.req_egg = 3
        self.dead = False
        self.sound = pygame.mixer.Sound('sounds//bok.ogg')
        
        self.speed = speed
        self.spriteList = spriteList
        self.flipped = False
        self.stationary = False
        self.sprites = len(self.spriteList)
        self.current_frame = 0
        self.timer = 0
        self.frame_duration = 150
        self.hak = pygame.image.load('graphics//kyl_HAK.png').convert_alpha()
        self.sprite = pygame.image.load(self.spriteList[self.current_frame]).convert_alpha()
        self.rect = self.sprite.get_rect(center = gameCanvas.rect.center)        
    def draw(self, dt):
        self.sprite = pygame.image.load(self.spriteList[self.current_frame]).convert_alpha()
        self.timer += dt
        self.rect.clamp_ip(gameCanvas.rect)
        if gameCanvas.scenery == "inside":
            self.rect.clamp_ip(redeWall.rect)
        elif gameCanvas.scenery == "outside":
            pass
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] or key[pygame.K_LEFT] or key[pygame.K_UP] or key[pygame.K_DOWN]:
            if self.timer >= self.frame_duration:
                self.current_frame = (self.current_frame + 1) % self.sprites
                self.timer = 0
        if not key[pygame.K_SPACE]:
            self.stationary = False
        if key[pygame.K_RIGHT]:
            if self.stationary == False:
                self.rect.x += self.speed
                self.flipped = True
        if key[pygame.K_LEFT]:
            if self.stationary == False:
                self.rect.x -= self.speed
                self.flipped = False
        if key[pygame.K_UP]:
            if self.stationary == False:
                self.rect.y -= self.speed
        if key[pygame.K_DOWN]:
            if self.stationary == False:
                self.rect.y += self.speed
        if key[pygame.K_SPACE]:
            self.stationary = True
            self.sprite = self.hak
            if self.rect.colliderect(korn.rect):
                self.sound.play()
                korn.spawned = False
                korn.timer = 0
                foodBarFront.update()
        if self.flipped == True:
            self.sprite = pygame.transform.flip(self.sprite, True, False)  
        gameCanvas.game.blit(self.sprite, self.rect)

class Goal(pygame.sprite.Sprite):
    def __init__(self, file):
        self.file = file
        self.sprite = pygame.image.load(self.file).convert_alpha()
        self.rect = self.sprite.get_rect(center = gameCanvas.rect.center)
        self.timer = 0
        self.spawned = False
    def spawn(self, dt):
        self.timer += dt
        if self.spawned == False and gameCanvas.scenery == "outside":
            if self.timer >= random.randint(2000, 5000):
                self.rect.x = random.randint(0, (gameCanvas.rect.width - 30))
                self.rect.y = random.randint(0, (gameCanvas.rect.height - 30))
                if self.rect.colliderect(barWall.rect) or self.rect.colliderect(bottomWall.rect) or self.rect.colliderect(houseWall.rect) or self.rect.colliderect(topWall.rect):
                    self.spawn(1999)
                self.spawned = True
                
    def draw(self):
        if self.spawned == True:
            if gameCanvas.scenery == "outside" and npc_kylling1.got == False and npc_kylling2.got == False:
                gameCanvas.game.blit(self.sprite, self.rect)
            if npc_kylling1.got == True or npc_kylling2.got == True:
                self.spawned = False
                npc_kylling1.got, npc_kylling2.got = False, False
                self.timer = 0
        else:
            self.rect.x = 9999
class Graphic:
    def __init__(self, color1, color2, color3, posx, posy, width, height, start, maxWidth, add):
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.start = start
        self.maxWidth = maxWidth
        self.add = add
    def draw(self):
        if self.width < (self.maxWidth / 3):
            pygame.draw.rect(gameCanvas.game, self.color1, (self.posx, self.posy, self.width, self.height))
        elif self.width < (self.maxWidth / 3) * 2:
            pygame.draw.rect(gameCanvas.game, self.color2, (self.posx, self.posy, self.width, self.height))
        else:
            pygame.draw.rect(gameCanvas.game, self.color3, (self.posx, self.posy, self.width, self.height))
    def update(self):
        if self.width <= self.maxWidth and self.width > 0:
            self.width += self.add
        if self.width > self.maxWidth:
            self.width = self.maxWidth
        if self.add < 0:
            if self.width <= 1:
                self.width = 1
    def create_timer(self, timer_duration):
        self.timer = 0
        self.timer_duration = timer_duration
    def sub_time(self, dt):
        self.timer += dt
        if self.timer >= self.timer_duration:
            self.timer = 0
            self.update()
    def reset(self):
        self.width = self.start
    def next_level(self):
        if self.add < 0:
            self.add *= 1.085
        else:
            self.add /= 1.2
        int(self.add)
        
class InvisibleWall:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.wall = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32) # Den dér pygame.SRCALPHA, 32 gør at væggende er usynlige.
        self.wall = self.wall.convert_alpha()
        self.rect = self.wall.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        gameCanvas.game.blit(self.wall, self.rect)

def gameOverAnim():
    pygame.mixer.music.fadeout(8000)
    images = [pygame.image.load('graphics//game_over_frame1.png').convert(), pygame.image.load('graphics//game_over_frame2.png').convert(),
              pygame.image.load('graphics//game_over_frame3.png').convert(), pygame.image.load('graphics//game_over_frame4.png').convert(),
              pygame.image.load('graphics//game_over_frame5.png').convert(), pygame.image.load('graphics//game_over_frame6.png').convert(),
              pygame.image.load('graphics//game_over_frame7.png').convert()]
    for x in images:
        gameCanvas.game.blit(x, (300, 200))
        pygame.display.update()
        pygame.time.wait(2000)
    menu.mainLoop()

def mainLoop():
    clock = pygame.time.Clock()
    pygame.mixer.music.load('sounds//COMPLETE.mp3')
    pygame.mixer.music.play(-1)
    while chicken.dead == False:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                chicken.dead = True
                pygame.quit()
        if timeBarFront.width == 1 or foodBarFront.width == foodBarFront.maxWidth:
            gameCanvas.change_background()
        gameCanvas.draw()
        korn.draw()
        korn.spawn(dt)
        npc_kylling1.draw(dt, korn.spawned, korn.rect.center, korn.rect)
        npc_kylling2.draw(dt, korn.spawned, korn.rect.center, korn.rect)
        chicken.draw(dt)
        gameCanvas.draw2()
        foodBarBack.draw()
        timeBarBack.draw()
        foodBarFront.draw()
        timeBarFront.draw()
        timeBarFront.sub_time(dt)
        barWall.draw()
        houseWall.draw()
        bottomWall.draw()
        topWall.draw()
        redeWall.draw()
        npc1Wall.draw()
        npc2Wall.draw()
        if gameCanvas.scenery == "inside":
            nightGameBack.draw()
            current_egg_text.__init__(390, 500, ("%s / %s" % (chicken.egg, chicken.req_egg)), WHITE, "helvetica", 24)
            current_egg_text.draw(gameCanvas.game)
            nightGame.draw(gameCanvas.game)
            nightGame.move()
            if nightGame.pind_stop == True:
                nightGame.add_egg(chicken, gameCanvas.game)
                nightGame.__init__(300, 30, 250, 450, foodBarFront.width)
            npc_kylling1.rect.clamp_ip(npc1Wall.rect)
            npc_kylling2.rect.clamp_ip(npc2Wall.rect)
        pygame.display.update()


#Classes
gameCanvas = Canvas(800, 600, 'graphics//background.png',
                              'graphics//hegn.png')
chicken = Player(['graphics//kyl_IDLE.png',
                  'graphics//kyl_WALK.png'],
                 3)
korn = Goal('graphics//korn.png')

npc_kylling1 = NPC.AI(['graphics//NPCchicken_IDLE.png',
                      'graphics//NPCchicken_WALK.png'],
                     2, gameCanvas.game, gameCanvas.rect)
npc_kylling2 = NPC.AI(['graphics//NPCchicken_IDLE.png',
                      'graphics//NPCchicken_WALK.png'],
                     2, gameCanvas.game, gameCanvas.rect)


#Graphic
foodBarBack = Graphic(BLACK, BLACK, BLACK, 20, 10, 120, 20, 0, 0, 0)
foodBarFront = Graphic(RED, YELLOW, GREEN, 21, 11, 1, 18, 1, 118, 25)
timeBarBack = Graphic(BLACK, BLACK, BLACK, 20, 40, 120, 20, 0, 0, 0)
timeBarFront = Graphic(BLUE, BLUE, BLUE, 21, 41, 118, 18, 118, 118, -1)
timeBarFront.create_timer(500)

#Wall
barWall = InvisibleWall(150, 70, 0, 0)
houseWall = InvisibleWall(125, 100, 530, 0)
bottomWall = InvisibleWall(800, 30, 0, 570)
topWall = InvisibleWall(800, 30, 0, 0)
redeWall = InvisibleWall(45, 40, 350, 235)
npc1Wall = InvisibleWall(45, 40, 100, 235)
npc2Wall = InvisibleWall(45, 40, 630, 235)

#nightGame = minigame.MiniGame(300, 30, 250, 450)
nightGame = minigame.MiniGame(300, 30, 250, 450, foodBarFront.width)
nightGameBack = Graphic(BLACK, BLACK, BLACK, 249, 449, 302, 33, 0, 0, 0)

#TEXT
gameOver = text.Text(260, 260, "GAME OVER!", RED, "helvetica", 55)
nightText = text.Text(330, 260, "NIGHT", WHITE, "helvetica", 55)
dayText = text.Text(352, 260, "DAY", WHITE, "helvetica", 55)
req_egg_text = text.Text(295, 100, ("Required eggs: %s" % chicken.req_egg), WHITE, "helvetica", 32)
current_egg_text = text.Text(370, 500, ("%s / %s" % (chicken.egg, chicken.req_egg)), WHITE, "helvetica", 24)
scoreText = text.Text(300, 90, ("Score: %s" % chicken.egg_highscore), WHITE, "helvetica", 45)
highscoreText = text.Text(290, 400, ("Highscore: %s" % load.load()), WHITE, "helvetica", 45)

#main
if __name__ == '__main__':
    mainLoop()
