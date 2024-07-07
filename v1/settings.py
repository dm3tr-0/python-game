# скорость
FrameRate = 120
playerSpeed = int(150 / FrameRate * 10) / 10
enemyBulletSpeed = int(200 / FrameRate * 10) / 10
playerBulletSpeed = int(400 / FrameRate * 10) / 10
enemySpeed = int(50 / FrameRate * 10) / 10
shiftSpeed = 100

# направление в зависимости от зажатых клавиш wasd
worldSides = {
    "w": 270,
    "a": 180,
    "s": 90,
    "d": 0,
    "aw": 225,
    "dw": 315,
    "as": 135,
    "ds": 45
}

locationsBuffer = []
DEGREES = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]
sqrtTwo = (2 ** 0.5)
resolution = (800, 600)
