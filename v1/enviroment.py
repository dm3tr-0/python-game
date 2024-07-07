import pygame, random
from settings import *

class Objects:
    def __init__(self, window, position, isCollidable, health=None, texture=None, color=(50, 100, 200)):
        self.window = window
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
                pygame.draw.circle(self.window, self.color, self.position, 10)

            else:
                self.window.blit(self.texture, self.position)

    def Collidepoint(self, entities):
        if self.isCollidable:
            pass

    def Interact(self):
        pass

class Location:
    def __init__(self, window, hero, objects=[], texture=None, entities=[], color=(0,0,0)):
        self.window = window
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
                    self.doors += [Door(self.window, self.hero, [0, resolution[1] / 2], 1)]
                elif tempChoice == "w":
                    self.doors += [Door(self.window, self.hero,[resolution[0] / 2, 0], 2)]
                else:
                    self.doors += [Door(self.window, self.hero,[resolution[0], resolution[1] / 2], 3)]

            for door in self.doors:
                door.MakeVisible()


    def Draw(self):
        if self.texture != None:
            self.window.blit(self.texture, (0, 0))

        else:
            self.window.fill(self.color)

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
            changeLocation = door.PlayerCollidepoint()
            if changeLocation != None:
                return changeLocation

        return None

# класс дверей
class Door:
    def __init__(self, window, hero, position, side, texture=None, isVisible=False):
        self.window = window
        self.hero = hero
        self.texture = texture
        self.position = position
        self.side = side
        self.isVisible = isVisible # видна ли дверь
        self.hitbox = pygame.rect.Rect(self.position[0] - 50, self.position[1] - 50, 100, 100)

    # отрисовка текстуры двери
    def Draw(self):
        if self.isVisible:
            if self.texture != None:
                self.window.blit(self.texture, self.position)

            else:
                pygame.draw.circle(self.window, (200, 200, 200), self.position, 50)

    def MakeVisible(self):
        if not self.isVisible:
            self.isVisible = True

    def PlayerCollidepoint(self):
        if self.isVisible and self.hitbox.collidepoint(self.hero.position[0], self.hero.position[1]):
            self.isVisible = False
            return self.side

        return None

class Item:
    pass
