import pygame, os, sys, time, math, random, threading
from enviroment import *
from entities import *
from settings import *

sys.setrecursionlimit(int(1e9))

def UpdateLocations():
    global locationsBuffer
    enemies1 = [Minion(window, [random.randint(100, resolution[0] - 100), random.randint(100, resolution[1] - 100)], 1, speed=enemySpeed) for i in range(random.randint(1, 3))]
    enemies2 = [Minion(window,[random.randint(100, resolution[0] - 100), random.randint(100, resolution[1] - 100)], 1, speed=enemySpeed) for i in range(random.randint(1, 3))]
    enemies3 = [Minion(window,[random.randint(100, resolution[0] - 100), random.randint(100, resolution[1] - 100)], 1, speed=enemySpeed) for i in range(random.randint(1, 3))]
    locationsBuffer = [Location(window,hero, [Objects(window,[random.randint(100, resolution[0] - 100), random.randint(100, resolution[1] - 100)], True) for i in range(random.randint(1, 5))], entities=enemies1, color=(0, 200, 200)),
                        Location(window,hero, [Objects(window,[random.randint(100, resolution[0] - 100), random.randint(100, resolution[1] - 100)], True) for i in range(random.randint(1, 5))], entities=enemies2, color=(0, 0, 200)),
                        Location(window,hero, [Objects(window,[random.randint(100, resolution[0] - 100), random.randint(100, resolution[1] - 100)], True) for i in range(random.randint(1, 5))], entities=enemies3, color=(100, 100, 200))]

def draw():
    currentlocation.Draw()
    pygame.display.update()

def main():
    global hero, window, gameOver, resolution, enemies, changeLocation, currentlocation, locationsBuffer
    pygame.init()
    window = pygame.display.set_mode(resolution)
    pygame.display.set_caption("")
    clock = pygame.time.Clock()
    # pygame.display.set_icon("")
    hero = Player(window, [resolution[0] / 2, resolution[1] / 2], playerSpeed)
    enemies = [Minion(window, [200, 200], 1, speed=enemySpeed)]
    currentlocation = Location(window, hero, [Objects(window,[random.randint(100, resolution[0] - 100), random.randint(100, resolution[1] - 100)], True) for i in range(random.randint(1, 5))], entities=enemies, color =(100,100,100))
    UpdateLocations()
    changeLocation = None

    gameOver = False

    while not gameOver:
        clock.tick(FrameRate)

        draw()
        hero.Move()
        changeLocation = currentlocation.LocationEvents()

        if changeLocation != None:
            currentlocation = locationsBuffer[changeLocation - 1]
            changeLocation = None
            UpdateLocations()
            hero.position = [resolution[0] / 2, resolution[1]]

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
                if event.key == pygame.K_DOWN:
                    hero.Usecase(1)

    pygame.quit()

if __name__ == '__main__':
    mainGame = threading.Thread(target=main)
    mainGame.start()
    mainGame.join()
