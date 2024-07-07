import pygame, random, time
from settings import *
from utils import *

# класс пулей
class Bullet:
    def __init__(self, speed, isVisible, color=(200, 0, 0), bulletType="p_common"):
        self.position = None
        self.speed = speed
        self.isVisible = isVisible
        self.color = color
        self.direction = None
        self.Type = "bullet"

        self.damage = 0
        self.bulletType = bulletType
        if "common" in bulletType:
            self.damage = 1

    def DrawBullet(self):
        if self.isVisible:
            pygame.draw.circle(window, self.color, self.position, 5)

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
                    if entity.Type == "player" and self.bulletType[0] == "e":
                        entity.health -= self.damage
                        self.isVisible = False
                        self.direction = None
                        self.position = None
                        return

                    elif entity.Type == "enemy" and self.bulletType[0] == "p":
                        entity.health -= self.damage
                        self.isVisible = False
                        self.direction = None
                        self.position = None
                        return

                    elif entity.Type == "object":
                        if entity.health != None and entity.health != 0:
                            entity.health -= min(self.damage, entity.health)
                        self.isVisible = False
                        self.direction = None
                        self.position = None
                        return

class Player:
    def __init__(self, position, speed, health=10):
        self.health = health

        self.Type = "player"
        self.position = position
        self.speed = speed
        self.lastShift = 0
        self.direction = 270
        self.hitbox = pygame.rect.Rect(self.position[0] - 30, self.position[1] - 30, 60, 60)

        self.bullets = [Bullet(playerBulletSpeed, False, bulletType="p_common") for i in range(7)]

    def Draw(self):
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


class Enemy:
    def __init__(self, position, health, speed, bulletType="e_common"):
        self.position = position
        self.direction = random.randint(0, 7) * 45
        self.hitbox = pygame.rect.Rect(self.position[0] - 20, self.position[1] - 20, 40, 40)
        self.Type = "enemy"

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
        pygame.draw.circle(window, (0, 200, 0), self.position, 20)

    def isAlive(self):
        return self.health > 0

    def Shoot(self):
        pass


class Minion(Enemy):
    def __init__(self, position, health, speed, bulletType="e_common"):
        Enemy.__init__(self, position, health, speed, bulletType)
        self.bullets = [Bullet(enemyBulletSpeed, False, color=(0, 200, 0), bulletType=bulletType)]

    def Shoot(self, hero):
        if hero.isVisible(self.position):
            direction = None
            x0, y0 = self.position[0], self.position[1]
            x, y = hero.position[0], hero.position[1]
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

# классы противников
enemyClasses = (Enemy, Minion)
