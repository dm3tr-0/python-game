import pygame
import random
import time
import math
from settings import enemySpeed, resolution, DEGREES, enemyBulletSpeed
from utils import DegreeToMove, closest_degree
from entities.bullet import Bullet
from entities.player import Player
import globals

class Enemy:
    def __init__(self, position, health, speed, bulletType="e_common"):
        self.position = position
        self.direction = random.randint(0, 7) * 45
        self.hitbox = pygame.rect.Rect(self.position[0] - 20, self.position[1] - 20, 40, 40)

        self.lastMove = 0
        self.health = health
        self.speed = speed

    def Move(self):
        if (time.time() - self.lastMove >= 2):
            self.lastMove = time.time()
            self.direction = random.randint(0, 7) * 45
        DegreeToMove(self.direction, self)

        self.hitbox = pygame.rect.Rect(self.position[0] - 30, self.position[1] - 30, 60, 60)

    def Draw(self):
        pygame.draw.circle(globals.window, (0, 200, 0), self.position, 20)

    def isAlive(self):
        return self.health > 0

    def Shoot(self):
        pass


class Minion(Enemy):
    def __init__(self, position, health, speed, bulletType="e_common"):
        Enemy.__init__(self, position, health, speed, bulletType)
        self.bullets = [Bullet(enemyBulletSpeed, False, color=(0, 200, 0), bulletType=bulletType)]

    def Shoot(self):
        if globals.hero.isVisible(self.position):
            direction = None
            x0, y0 = self.position[0], self.position[1]
            x, y = globals.hero.position[0], globals.hero.position[1]
            if (x == x0):
                if (y > y0):
                    direction = 270
                else:
                    direction = 90
            else:
                direction = math.degrees(math.atan2((y - y0), (x - x0)))
                if direction < 0:
                    direction += 360
                closestDeg = DEGREES[0]
                minDiff = abs(DEGREES[0] - direction)
                for deg in DEGREES:
                    diff = abs(deg - direction)
                    if diff < minDiff:
                        minDiff = diff
                        closestDeg = deg
                direction = closestDeg

            self.bullets[0].MakeVisible(self.position, direction)

