import pygame, random, time, threading
from settings import FrameRate, playerBulletSpeed, playerSpeed, enemyBulletSpeed, enemySpeed, shiftSpeed, worldSides, locationsBuffer,DEGREES, sqrtTwo, resolution
from entities.player import Player
from entities.enemy import Enemy, Minion
from environment.objects import Objects
from environment.location import Location
from environment.location import Location
import globals

def UpdateLocations():

    enemies1 = [Minion([random.randint(100, resolution[0] - 100), random.randint(100, resolution[1] - 100)], 1, speed=enemySpeed) for i in range(random.randint(1, 3))]
    enemies2 = [Minion([random.randint(100, resolution[0] - 100), random.randint(100, resolution[1] - 100)], 1, speed=enemySpeed) for i in range(random.randint(1, 3))]
    enemies3 = [Minion([random.randint(100, resolution[0] - 100), random.randint(100, resolution[1] - 100)], 1, speed=enemySpeed) for i in range(random.randint(1, 3))]
    locationsBuffer = [Location([Objects([random.randint(100, resolution[0] - 100), random.randint(100, resolution[1] - 100)], True) for i in range(random.randint(1, 5))], entities=enemies1, color=(0, 200, 200)),
                        Location([Objects([random.randint(100, resolution[0] - 100), random.randint(100, resolution[1] - 100)], True) for i in range(random.randint(1, 5))], entities=enemies2, color=(0, 0, 200)),
                        Location([Objects([random.randint(100, resolution[0] - 100), random.randint(100, resolution[1] - 100)], True) for i in range(random.randint(1, 5))], entities=enemies3, color=(100, 100, 200))]

def draw():
    currentlocation.Draw()
    pygame.display.update()

def main():
    global currentlocation
    pygame.init()
    resolution = (800, 600)
    globals.window = pygame.display.set_mode(resolution)
    pygame.display.set_caption("")
    clock = pygame.time.Clock()
    # pygame.display.set_icon("")
    globals.hero = Player([resolution[0] / 2, resolution[1] / 2], playerSpeed)
    enemies = [Minion([200, 200], 1, speed=enemySpeed)]
    currentlocation = Location([Objects([random.randint(100, resolution[0] - 100), random.randint(100, resolution[1] - 100)], True) for i in range(random.randint(1, 5))], entities=enemies, color =(100,100,100))
    UpdateLocations()
    changeLocation = 0

    gameOver = False

    while not gameOver:
        clock.tick(FrameRate)

        draw()
        globals.hero.Move()
        currentlocation.LocationEvents()

        if changeLocation:
            currentlocation = locationsBuffer[changeLocation - 1]
            changeLocation = 0
            UpdateLocations()
            globals.hero.position = [resolution[0] / 2, resolution[1]]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                globals.hero.Usecase(event.button)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameOver = True
                    break
                if event.key == pygame.K_DOWN:
                    globals.hero.Usecase(1)

    pygame.quit()

if __name__ == '__main__':
    mainGame = threading.Thread(target=main)
    mainGame.start()
    mainGame.join()