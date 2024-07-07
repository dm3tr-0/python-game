import pygame
from settings import locationsBuffer, resolution
from environment.door import Door

class Location:
    def __init__(self, objects=[], texture=None, entities=[], color=(0,0,0)):
        self.obiects = objects
        self.texture = texture
        self.doors = []
        self.entities = entities + [hero]
        self.color = color

    def MakeDoors(self):
        if len(self.doors) == 0:
            for element in range(random.randint(1, 3)):
                tempChoice = random.choice("awd")
                if tempChoice == "a":
                    self.doors += [Door([0, resolution[1] / 2], 1)]
                elif tempChoice == "w":
                    self.doors += [Door([resolution[0] / 2, 0], 2)]
                else:
                    self.doors += [Door([resolution[0], resolution[1] / 2], 3)]

            for door in self.doors:
                door.MakeVisible()


    def Draw(self):
        if self.texture != None:
            window.blit(self.texture, (0, 0))

        else:
            window.fill(self.color)

        for door in self.doors:
            door.Draw()

        for obj in self.obiects:
            obj.Draw()

        for entity in self.entities:
            for bullet in entity.bullets:
                bullet.DrawBullet()
            entity.Draw()

    def LocationEvents(self):
        for entity in self.entities:
            for bullet in entity.bullets:
                bullet.MoveBullet()
                bullet.BulletColidepoint(self.entities)
                bullet.BulletColidepoint(self.obiects)

            if type(entity) in enemyClasses:
                if entity.isAlive():
                    entity.Move()
                    entity.Shoot()
                else:
                    self.entities.remove(entity)

        if len(self.entities) <= 1:
            self.MakeDoors()

        for door in self.doors:
            door.PlayerCollidepoint()
