import pygame
from settings import resolution
from entities.player import Player
import globals

class Door:
    def __init__(self, position, side, texture=None, isVisible=False):
        self.texture = texture
        self.position = position
        self.side = side
        self.isVisible = isVisible # видна ли дверь
        self.hitbox = pygame.rect.Rect(self.position[0] - 50, self.position[1] - 50, 100, 100)

    # отрисовка текстуры двери
    def Draw(self):
        if self.isVisible:
            if self.texture != None:
                globals.window.blit(self.texture, self.position)

            else:
                pygame.draw.circle(globals.window, (200, 200, 200), self.position, 50)

    def MakeVisible(self):
        if not self.isVisible:
            self.isVisible = True

    def PlayerCollidepoint(self):
        global changeLocation
        if self.isVisible and self.hitbox.collidepoint(globals.hero.position[0], globals.hero.position[1]):
            self.isVisible = False
            changeLocation = self.side
