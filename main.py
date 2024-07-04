import pygame
import os
import sys
import time
import math
import random

sys.setrecursionlimit(int(1e9))

class Player:
    def __init__(self, position, speed):
        self.position = position
        self.speed = speed

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

        if isShift:
            if len(currentDirection) == 2:
                if currentDirection[0] == "w":
                    self.position[1] -= 7 * self.speed
                else:
                    self.position[1] += 7 * self.speed

                if (currentDirection[1] == "a"):
                    self.position[0] -= 7 * self.speed
                else:
                    self.position[0] += 7 * self.speed

            elif len(currentDirection) == 1:
                if currentDirection[0] == "w":
                    self.position[1] -= 10 * self.speed
                elif currentDirection[0] == "s":
                    self.position[1] += 10 * self.speed

                elif (currentDirection[0] == "a"):
                    self.position[0] -= 10 * self.speed
                else:
                    self.position[0] += 10 * self.speed

    def Usecase(self, mouseKey):
        pass

class Enemies:
    pass

class Location:
    pass

def draw():
    global hero
    window.fill((0, 0, 0))
    hero.Draw()

    pygame.display.update()

def main():
    global hero, window, gameOver, resolution
    pygame.init()
    resolution = (800, 600)
    window = pygame.display.set_mode(resolution)
    hero = Player([0, 0], 0.1)
    gameOver = False
    while not gameOver:
        draw()
        hero.Move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                hero.Usecase(event.button)

    pygame.quit()
if __name__ == '__main__':
    main()


