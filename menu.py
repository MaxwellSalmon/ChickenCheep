import pygame
import text,game, load

pygame.init()
pygame.mixer.init()

gameExit = False

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = pygame.display.set_mode((self.width,self.height))
        self.rect = self.canvas.get_rect()
        pygame.display.set_caption("Chicken Cheep")
        self.image = pygame.image.load("graphics//menubackground.png")
        self.imageON = False
    def draw(self):
        self.canvas.blit(self.image, self.rect)

class Button:
    def __init__(self, width, height, y, color, command):
        self.width = width
        self.height = height
        self.box = pygame.Surface([self.width, self.height]).convert()
        self.rect = self.box.get_rect(center=menuCanvas.rect.center)
        self.rect.y = y
        self.color = color
        self.command = command
        self.sound = pygame.mixer.Sound("sounds//plop.ogg")
        self.image = pygame.image.load("graphics//menuoptions.png")
    def draw(self):
        global gameExit
        self.box.fill(self.color)
        menuCanvas.canvas.blit(self.box, self.rect)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = (220,220,220)
            if pygame.mouse.get_pressed()[0]:
                self.sound.play()
                if self.command == "start":
                    game.mainLoop()
                elif self.command == "options":
                    menuCanvas.imageON = True
                elif self.command == 'exit':
                    gameExit = True
                    pygame.quit()
                    quit()
                elif self.command == 'close':
                    menuCanvas.imageON = False
        else:
            self.color = (245,245,245)
        

def mainLoop():
    global gameExit
    highscoreText.__init__(300, 400, ("Highscore: %s" % load.load()), (75, 180, 50), "helvetica", 30)
    clock = pygame.time.Clock()
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()
        menuCanvas.draw()
        
        playButton.draw()
        playText.draw(menuCanvas.canvas)

        optionsButton.draw()
        optionsText.draw(menuCanvas.canvas)

        exitButton.draw()
        exitText.draw(menuCanvas.canvas)

        maxwellText.draw(menuCanvas.canvas)
        highscoreText.draw(menuCanvas.canvas)
        linctusText.draw(menuCanvas.canvas)
        soundcloudText.draw(menuCanvas.canvas)

        if menuCanvas.imageON == True:
            menuCanvas.canvas.blit(optionsButton.image, menuCanvas.rect)
            optionsCloseButton.draw()
            optionsCloseText.draw(menuCanvas.canvas)
        
        pygame.display.update()
        clock.tick(60)

menuCanvas = Canvas(800, 600)

playButton = Button(200, 50, 200, (245,245,245), "start")
playText = text.Text(380, 210, "Play", (0, 0, 0), "helvetica", 24)

optionsButton = Button(200, 50, 260, (245,245,245), "options")
optionsText = text.Text(366, 268, "Options", (0, 0, 0), "helvetica", 24)

optionsCloseButton = Button(200, 50, 400, (245,245,245), "close")
optionsCloseText = text.Text(370, 409, "Close", (0, 0, 0), "helvetica", 24)

exitButton = Button(200, 50, 320, (245,245,245), "exit")
exitText = text.Text(382, 329, "Exit", (0, 0, 0), "helvetica", 24)

maxwellText = text.Text(310, 535, "A game by MaxwellSalmon", (0, 0, 0), "helvetica", 18)
highscoreText = text.Text(300, 400, ("Highscore: %s" % load.load()), (75, 180, 50), "helvetica", 30)
linctusText = text.Text(309, 560, "With music from White Linctus", (0, 0, 0), "helvetica", 16)
soundcloudText = text.Text(310, 580, "https://soundcloud.com/emonadeinctuz", (50, 50, 50), "helvetica", 13)
    
if __name__ == '__main__':
    mainLoop()
