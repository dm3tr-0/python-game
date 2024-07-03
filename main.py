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
        direction = [1, -1]

        currentKey = pygame.key.get_pressed()
        isShift = pygame.key.get_mods() & pygame.KMOD_SHIFT

        if currentKey[pygame.K_w]:
            if self.position[1] - self.speed >= 0:
                self.position[1] -= self.speed
                direction = [1, -1]

        if currentKey[pygame.K_a]:
            if self.position[0] - self.speed >= 0:
                self.position[0] -= self.speed
                direction = [0, -1]

        if currentKey[pygame.K_s]:
            if self.position[1] + self.speed <= resolution[1]:
                self.position[1] += self.speed
                direction = [1, 1]

        if currentKey[pygame.K_d]:
            if self.position[0] + self.speed <= resolution[0]:
                self.position[0] += self.speed
                direction = [0, 1]

        if isShift:
            self.position[direction[0]] += direction[1] * 10 * self.speed

    def Usecase(self, mouseKey):
        pass
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


