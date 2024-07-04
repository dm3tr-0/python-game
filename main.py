import pygame, os, sys, time, math, random, threading

sys.setrecursionlimit(int(1e9))

#скорость
SPEED_ = 500
#направление в зависимости от зажатых клавиш wasd
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

DEGREES = [ 0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360 ]

#константа корень из двух
sqrtTwo = (2 ** 0.5)

#перемещение спрайта  заданом направлении
def DegreeToMove(direction, entity):
    if type(entity) != Bullet:
        if direction == 0:
            if entity.position[0] + entity.speed < resolution[0]:
                entity.position[0] += entity.speed
    
        elif direction == 45:
            if entity.position[0] + entity.speed < resolution[0]:
                entity.position[0] += entity.speed / sqrtTwo
            if entity.position[1] + entity.speed < resolution[1]:
                entity.position[1] += entity.speed / sqrtTwo
    
        elif direction == 90:
            if entity.position[1] + entity.speed < resolution[1]:
                entity.position[1] += entity.speed
    
        elif direction == 135:
            if entity.position[0] - entity.speed > 0:
                entity.position[0] -= entity.speed / sqrtTwo
            if entity.position[1] + entity.speed < resolution[1]:
                entity.position[1] += entity.speed / sqrtTwo
    
        elif direction == 180:
            if entity.position[0] - entity.speed > 0:
                entity.position[0] -= entity.speed
    
        elif direction == 225:
            if entity.position[0] - entity.speed > 0:
                entity.position[0] -= entity.speed / sqrtTwo
            if entity.position[1] - entity.speed > 0:
                entity.position[1] -= entity.speed / sqrtTwo
    
        elif direction == 270:
            if entity.position[1] - entity.speed > 0:
                entity.position[1] -= entity.speed
    
        elif direction == 315:
            if entity.position[0] + entity.speed < resolution[0]:
                entity.position[0] += entity.speed / sqrtTwo
            if entity.position[1] - entity.speed > 0:
                entity.position[1] -= entity.speed / sqrtTwo

    else:
        if direction == 0:
            entity.position[0] += entity.speed

        elif direction == 30:
            entity.position[0] += entity.speed / ((3 / 2) ** 0.5)
            entity.position[1] += entity.speed / (3 ** 0.5)

        elif direction == 45:
            entity.position[0] += entity.speed / sqrtTwo
            entity.position[1] += entity.speed / sqrtTwo

        elif direction == 60:
            entity.position[0] += entity.speed / (3 ** 0.5)
            entity.position[1] += entity.speed / ((3 / 2) ** 0.5)

        elif direction == 90:
            entity.position[1] += entity.speed

        elif direction == 120:
            entity.position[0] -= entity.speed / (3 ** 0.5)
            entity.position[1] += entity.speed / ((3 / 2) ** 0.5)

        elif direction == 135:
            entity.position[0] -= entity.speed / sqrtTwo
            entity.position[1] += entity.speed / sqrtTwo

        elif direction == 150:
            entity.position[0] -= entity.speed / ((3 / 2) ** 0.5)
            entity.position[1] += entity.speed / (3 ** 0.5)

        elif direction == 180:
            entity.position[0] -= entity.speed

        elif direction == 210:
            entity.position[0] -= entity.speed / ((3 / 2) ** 0.5)
            entity.position[1] -= entity.speed / (3 ** 0.5)

        elif direction == 225:
            entity.position[0] -= entity.speed / sqrtTwo
            entity.position[1] -= entity.speed / sqrtTwo

        elif direction == 240:
            entity.position[0] -= entity.speed / (3 ** 0.5)
            entity.position[1] -= entity.speed / ((3 / 2) ** 0.5)

        elif direction == 270:
            entity.position[1] -= entity.speed

        elif direction == 300:
            entity.position[0] += entity.speed / (3 ** 0.5)
            entity.position[1] -= entity.speed / ((3 / 2) ** 0.5)

        elif direction == 315:
            entity.position[0] += entity.speed / sqrtTwo
            entity.position[1] -= entity.speed / sqrtTwo

        elif direction == 330:
            entity.position[0] += entity.speed / ((3 / 2) ** 0.5)
            entity.position[1] -= entity.speed / (3 ** 0.5)

        elif direction == 360:
            entity.position[0] += entity.speed

#класс пулей
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
            DegreeToMove(self.direction, self)

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

                    elif type(entity) in (Enemy, Minion) and self.bulletType[0] == "p":
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
        self.lastShift = 0
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

        if isShift and (time.time() - self.lastShift >= 2):
            self.lastShift = time.time()
            if len(currentDirection) == 2:
                if currentDirection[0] == "w":
                    self.position[1] -= min(SPEED_ / sqrtTwo * self.speed, self.position[1])
                else:
                    self.position[1] += min(SPEED_ / sqrtTwo * self.speed, resolution[1]-self.position[1])

                if (currentDirection[1] == "a"):
                    self.position[0] -= min(SPEED_ / sqrtTwo * self.speed, self.position[0])
                else:
                    self.position[0] += min(SPEED_ / sqrtTwo * self.speed, resolution[0]-self.position[0])

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

    def isVisible(self, position):
        return True

class Enemy:
    def __init__(self, position, health, speed, bulletType ="e_common"):
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
        pygame.draw.circle(window, (0, 200, 0), self.position, 20)

    def isAlive(self):
        return self.health > 0

    def Shoot(self):
        pass

class Minion(Enemy):
    def __init__(self, position, health, speed, bulletType="e_common"):
        Enemy.__init__(self, position, health, speed, bulletType)
        self.bullets = [Bullet(0.2, False, color=(0, 200, 0), bulletType=bulletType)]

    def Shoot(self):
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
                direction = math.degrees(math.atan2( (y - y0), (x - x0) ))
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

class Location:
    pass

class Item:
    pass

class Door:
    pass

def draw():
    window.fill((0, 0, 0))

    for entity in entities:
        for bullet in entity.bullets:
            bullet.DrawBullet()

    for entity in entities:
        entity.Draw()

    pygame.display.update()

def main():
    global hero, window, gameOver, resolution, enemies, entities
    pygame.init()
    resolution = (800, 600)
    window = pygame.display.set_mode(resolution)
    pygame.display.set_caption("")
    # pygame.display.set_icon("")
    hero = Player([resolution[0] / 2, resolution[1] / 2], 0.2)
    enemies = [Minion([200, 200], 1, speed=0.1)]

    entities = [hero] + enemies

    gameOver = False

    while not gameOver:
        draw()
        hero.Move()

        for entity in entities:
            for bullet in entity.bullets:
                bullet.MoveBullet()
                bullet.BulletColidepoint()

        for enemy in enemies:
            if enemy.isAlive():
                enemy.Move()
                enemy.Shoot()
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
