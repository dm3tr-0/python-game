import pygame
import time
from settings import playerSpeed, worldSides, resolution, shiftSpeed, sqrtTwo, playerBulletSpeed
from entities.bullet import Bullet

class Player:
    def __init__(self, position, speed, health=10):
        self.health = health

        self.position = position
        self.speed = speed
        self.lastShift = 0
        self.direction = 270
        self.hitbox = pygame.rect.Rect(self.position[0] - 30, self.position[1] - 30, 60, 60)

        self.bullets = [Bullet(playerBulletSpeed, False, bulletType="p_common") for i in range(7)]

    def Draw(self):
        global window
        pygame.draw.circle(
            surface=window,
            color=(200, 0, 0),
            center=self.position,
            radius=30
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

        if isShift and (time.time() - self.lastShift >= 2):
            self.lastShift = time.time()
            if len(currentDirection) == 2:
                if currentDirection[0] == "w":
                    self.position[1] -= min(shiftSpeed / sqrtTwo * self.speed, self.position[1])
                else:
                    self.position[1] += min(shiftSpeed / sqrtTwo * self.speed, resolution[1] - self.position[1])

                if (currentDirection[1] == "a"):
                    self.position[0] -= min(shiftSpeed / sqrtTwo * self.speed, self.position[0])
                else:
                    self.position[0] += min(shiftSpeed / sqrtTwo * self.speed, resolution[0] - self.position[0])

            elif len(currentDirection) == 1:
                if currentDirection[0] == "w":
                    self.position[1] -= min(shiftSpeed * self.speed, self.position[1])
                elif currentDirection[0] == "s":
                    self.position[1] += min(shiftSpeed * self.speed, resolution[1] - self.position[1])

                elif (currentDirection[0] == "a"):
                    self.position[0] -= min(shiftSpeed * self.speed, self.position[0])
                else:
                    self.position[0] += min(shiftSpeed * self.speed, resolution[0] - self.position[0])

        self.hitbox = pygame.rect.Rect(self.position[0] - 30, self.position[1] - 30, 60, 60)

    def Usecase(self, mouseKey):
        if mouseKey == 1:
            for bullet in self.bullets:
                if not bullet.isVisible:
                    bullet.MakeVisible(self.position, self.direction)
                    break

    def isVisible(self, position):
        return True
