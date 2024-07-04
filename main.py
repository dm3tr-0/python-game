import pygame
import os
import sys
import time
import math
import random
import threading

sys.setrecursionlimit(int(1e9))

SPEED_ = 500
worldSides = {
    "w" : 270,
    "a" : 180,
    "s" : 90,
    "d" : 0,
    "aw" : 225,
    "dw" : 315,
    "as" : 135,
    "ds" : 45
}
sqrtTwo = (2 ** 0.5)


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
            pygame.draw.circle(window, self.color, self.position, 5)

    def MoveBullet(self):
        if self.isVisible:
            if self.direction == 0:
                self.position[0] += self.speed

            elif self.direction == 45:
                self.position[0] += self.speed / sqrtTwo
                self.position[1] += self.speed / sqrtTwo

            elif self.direction == 90:
                self.position[1] += self.speed

            elif self.direction == 135:
                self.position[0] -= self.speed / sqrtTwo
                self.position[1] += self.speed / sqrtTwo

            elif self.direction == 180:
                self.position[0] -= self.speed

            elif self.direction == 225:
                self.position[0] -= self.speed / sqrtTwo
                self.position[1] -= self.speed / sqrtTwo

            elif self.direction == 270:
                self.position[1] -= self.speed

            elif self.direction == 315:
                self.position[0] += self.speed / sqrtTwo
                self.position[1] -= self.speed / sqrtTwo

    def MakeVisible(self, position, direction):
        if not self.isVisible:
            self.isVisible = True
            self.position = position.copy()
            self.direction = direction

    # simple version
    def BulletColidepoint(self):
        global entities
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

                    elif type(entity) == Enemy and self.bulletType[0] == "p":
                        entity.health -= self.damage
                        self.isVisible = False
                        self.direction = None
                        self.position = None
                        return

class Player:
    def __init__(self, position, speed, health = 10):
        self.health = health

        self.position = position
        self.speed = speed
        self.shiftCooldown = 0
        self.direction = 270
        self.hitbox = pygame.rect.Rect(self.position[0] - 30, self.position[1] - 30, 60, 60)

        self.bullets = [Bullet(1, False, bulletType="p_common") for i in range(7)]

    def Draw(self):
        global window
        pygame.draw.circle(
            surface = window,
            color = (200,0,0),
            center = self.position,
            radius = 30
        )

    def Move(self):
        currentDirection = ""
        currentKey = pygame.key.get_pressed()
        isShift = pygame.key.get_mods() & pygame.KMOD_SHIFT

        if currentKey[pygame.K_w]:
            if self.position[1] - self.speed >= 0:
                currentDirection += "w"
                self.position[1] -= self.speed

        if currentKey[pygame.K_s]:
            if self.position[1] + self.speed <= resolution[1]:
                idx = currentDirection.find("w")
                if idx == -1:
                    currentDirection += "s"
                else:
                    currentDirection = currentDirection.replace("w", "")
                self.position[1] += self.speed

        if currentKey[pygame.K_a]:
            if self.position[0] - self.speed >= 0:
                currentDirection += "a"
                self.position[0] -= self.speed

        if currentKey[pygame.K_d]:
            if self.position[0] + self.speed <= resolution[0]:
                idx = currentDirection.find("a")
                if idx == -1:
                    currentDirection += "d"
                else:
                    currentDirection = currentDirection.replace("a", "")
                self.position[0] += self.speed

        if currentDirection != "":
            self.direction = worldSides["".join(sorted(currentDirection))]

        if isShift and (time.time() - self.shiftCooldown >= 2):
            self.shiftCooldown = time.time()
            if len(currentDirection) == 2:
                if currentDirection[0] == "w":
                    self.position[1] -= min(SPEED_ / (2 ** 0.5) * self.speed, self.position[1])
                else:
                    self.position[1] += min(SPEED_ / (2 ** 0.5) * self.speed, resolution[1]-self.position[1])

                if (currentDirection[1] == "a"):
                    self.position[0] -= min(SPEED_ / (2 ** 0.5) * self.speed, self.position[0])
                else:
                    self.position[0] += min(SPEED_ / (2 ** 0.5) * self.speed, resolution[0]-self.position[0])

            elif len(currentDirection) == 1:
                if currentDirection[0] == "w":
                    self.position[1] -= min(SPEED_ * self.speed, self.position[1])
                elif currentDirection[0] == "s":
                    self.position[1] += min(SPEED_ * self.speed, resolution[1]-self.position[1])

                elif (currentDirection[0] == "a"):
                    self.position[0] -= min(SPEED_ * self.speed, self.position[0])
                else:
                    self.position[0] += min(SPEED_ * self.speed, resolution[0]-self.position[0])

        self.hitbox = pygame.rect.Rect(self.position[0] - 30, self.position[1] - 30, 60, 60)

    def Usecase(self, mouseKey):
        if mouseKey == 1:
            for bullet in self.bullets:
                if not bullet.isVisible:
                    bullet.MakeVisible(self.position, self.direction)
                    break

class Enemy:
    def __init__(self, position, health, speed, bulletType ="e_common"):
        self.position = position
        self.hitbox = pygame.rect.Rect(self.position[0] - 20, self.position[1] - 20, 40, 40)

        self.health = health
        self.speed = speed
        bullet = Bullet(0.5, False, bulletType=bulletType)

    def Move(self):
        if hero.position[0] - self.position[0] > 0:
            self.position[0] += self.speed + (random.random() * 0.25 - 0.125)
        else:
            self.position[0] -= self.speed + (random.random() * 0.25 - 0.125)

        if hero.position[1] - self.position[1] > 0:
            self.position[1] += self.speed + (random.random() * 0.25 - 0.125)
        else:
            self.position[1] -= self.speed + (random.random() * 0.25 - 0.125)

        self.hitbox = pygame.rect.Rect(self.position[0] - 30, self.position[1] - 30, 60, 60)

    def Draw(self):
        pygame.draw.circle(window, (0, 200, 0), self.position, 20)

    def isAlive(self):
        return self.health > 0

class Location:
    pass

class Item:
    pass

class Door:
    pass

def draw():
    global hero
    window.fill((0, 0, 0))
    hero.Draw()

    for bullet in hero.bullets:
        bullet.DrawBullet()

    for enemy in enemies:
        enemy.Draw()

    pygame.display.update()

def main():
    global hero, window, gameOver, resolution, enemies, entities
    pygame.init()
    resolution = (800, 600)
    window = pygame.display.set_mode(resolution)
    hero = Player([resolution[0] / 2, resolution[1] / 2], 0.2)
    enemies = [Enemy([0, 0], 10, speed=0.1)]

    entities = [hero] + enemies

    gameOver = False

    while not gameOver:
        draw()
        hero.Move()
        for bullet in hero.bullets:
            bullet.MoveBullet()
            bullet.BulletColidepoint()

        for enemy in enemies:
            if enemy.isAlive():
                enemy.Move()
            else:
                enemies.remove(enemy)
                entities.remove(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                hero.Usecase(event.button)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameOver = True
                    break

    pygame.quit()

if __name__ == '__main__':
    mainGame = threading.Thread(target=main)
    mainGame.start()
    mainGame.join()
