import math
from settings import *

def DegreeToMove(direction, entity):
    if entity.Type != "bullet":
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

def closest_degree(direction):
    dt = direction
    if dt < 0:
        dt += 360
    closestDeg = DEGREES[0]
    minDiff = abs(DEGREES[0] - dt)
    for deg in DEGREES:
        diff = abs(deg - dt)
        if diff < minDiff:
            minDiff = diff
            closestDeg = deg
    return closestDeg
