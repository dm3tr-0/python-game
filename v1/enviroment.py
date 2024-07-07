import pygame
from settings import *

class Objects:
    def __init__(self, position, isCollidable, health=None, texture=None, color=(50, 100, 200)):
        self.texture = texture
        self.health = health
        self.isCollidable = isCollidable
        self.position = position
        self.Type = "object"

        if self.texture != None:
            self.hitbox = pygame.rect.Rect(self.texture)
        else:
            self.hitbox = pygame.rect.Rect(self.position[0] - 10, self.position[1] - 10, 20, 20)
        # заглушка для отрисовки
        self.color = color

    def Draw(self):
        if (self.health != 0):
            if self.texture == None:
                pygame.draw.circle(window, self.color, self.position, 10)

            else:
                window.blit(self.texture, self.position)

    def Collidepoint(self, entities):
        if self.isCollidable:
            pass

    def Interact(self):
        pass

class Location:
    def __init__(self, hero, objects=[], texture=None, entities=[], color=(0,0,0)):
        self.obiects = objects
        self.texture = texture
        self.doors = []
        self.hero = hero
        self.entities = entities + [hero]
        self.color = color

    def MakeDoors(self):
        if len(self.doors) == 0:
            for element in range(random.randint(1, 3)):
                tempChoice = random.choice("awd")
                if tempChoice == "a":
                    self.doors += [Door([0, resolution[1] / 2], 1)]
                elif tempChoice == "w":
                    self.doors += [Door([resolution[0] / 2, 0], 2)]
                else:
                    self.doors += [Door([resolution[0], resolution[1] / 2], 3)]

            for door in self.doors:
                door.MakeVisible()


    def Draw(self):
        if self.texture != None:
            window.blit(self.texture, (0, 0))

        else:
            window.fill(self.color)

        for door in self.doors:
            door.Draw()

        for obj in self.obiects:
            obj.Draw()

        for entity in self.entities:
            for bullet in entity.bullets:
                bullet.DrawBullet()
            entity.Draw()

    def LocationEvents(self):
        for entity in self.entities:
            for bullet in entity.bullets:
                bullet.MoveBullet()
                bullet.BulletColidepoint(self.entities)
                bullet.BulletColidepoint(self.obiects)

            if entity.Type == "enemy":
                if entity.isAlive():
                    entity.Move()
                    entity.Shoot(self.hero)
                else:
                    self.entities.remove(entity)

        if len(self.entities) <= 1:
            self.MakeDoors()

        for door in self.doors:
            door.PlayerCollidepoint()

# класс дверей
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
                window.blit(self.texture, self.position)

            else:
                pygame.draw.circle(window, (200, 200, 200), self.position, 50)

    def MakeVisible(self):
        if not self.isVisible:
            self.isVisible = True

    def PlayerCollidepoint(self):
        global changeLocation
        if self.isVisible and self.hitbox.collidepoint(hero.position[0], hero.position[1]):
            self.isVisible = False
            changeLocation = self.side

class Item:
    pass
