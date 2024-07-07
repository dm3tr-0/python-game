import pygame, random, time, threading
from settings import *
from entities.player import Player
from entities.enemy import Enemy, Minion
from environment.objects import Objects
from environment.location import Location
import globals
from utils import DegreeToMove
enemyClasses = (Enemy, Minion)
class Bullet:
    def __init__(self, speed, isVisible, color=(200, 0, 0), bulletType="p_common"):
        self.position = None
        self.speed = speed
        self.isVisible = isVisible
        self.color = color
        self.direction = None

        self.damage = 0
        self.bulletType = bulletType
        if "common" in bulletType:
            self.damage = 1

    def DrawBullet(self):
        if self.isVisible:
            pygame.draw.circle(globals.window, self.color, self.position, 5)

    def MoveBullet(self):
        if self.isVisible:
            DegreeToMove(self.direction, self)

    def MakeVisible(self, position, direction):
        if not self.isVisible:
            self.isVisible = True
            self.position = position.copy()
            self.direction = direction

    # simple version
    def BulletColidepoint(self, entities):
        if self.isVisible:
            if self.position[0] < 0 or self.position[0] > resolution[0] \
                    or self.position[1] < 0 or self.position[1] > resolution[1]:
                self.isVisible = False
                self.direction = None
                self.position = None
                return

            for entity in entities:
                if entity.hitbox.collidepoint(self.position[0], self.position[1]):
                    if type(entity) == Player and self.bulletType[0] == "e":
                        entity.health -= self.damage
                        self.isVisible = False
                        self.direction = None
                        self.position = None
                        return

                    elif type(entity) in enemyClasses and self.bulletType[0] == "p":
                        entity.health -= self.damage
                        self.isVisible = False
                        self.direction = None
                        self.position = None
                        return

                    elif type(entity) == Objects:
                        if entity.health != None and entity.health != 0:
                            entity.health -= min(self.damage, entity.health)
                        self.isVisible = False
                        self.direction = None
                        self.position = None
                        return
