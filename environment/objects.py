import pygame
import globals

class Objects:
    def __init__(self, position, isCollidable, health=None, texture=None, color=(50, 100, 200)):
        self.texture = texture
        self.health = health
        self.isCollidable = isCollidable
        self.position = position
        if self.texture != None:
            self.hitbox = pygame.rect.Rect(self.texture)
        else:
            self.hitbox = pygame.rect.Rect(self.position[0] - 10, self.position[1] - 10, 20, 20)
        # заглушка для отрисовки
        self.color = color

    def Draw(self):
        if (self.health != 0):
            if self.texture == None:
                pygame.draw.circle(globals.window, self.color, self.position, 10)

            else:
                globals.window.blit(self.texture, self.position)

    def Collidepoint(self, entities):
        if self.isCollidable:
            pass

    def Interact(self):
        pass
