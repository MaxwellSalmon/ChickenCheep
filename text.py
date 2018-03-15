import pygame
pygame.init()

class Text:
    def __init__(self, posx, posy, text, color, font, size):
        self.posx = posx
        self.posy = posy
        self.text = text
        self.color = color
        self.size = size
        self.font = pygame.font.SysFont(font,self.size)
        self.layout = self.font.render(self.text, True, self.color)
    def draw(self, canvas):
        canvas.blit(self.layout,(self.posx, self.posy))
