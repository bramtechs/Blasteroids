import asteroid
from player import Player

DURATION = 2
INTERVAL = 1.8
timer = 0
hardness = 1.0


def init():
    global timer
    timer = INTERVAL


def set_hard(hard: bool):
    global hardness

    if hard:
        hardness = 1.4
    else:
        hardness = 1.0


def update(player: Player, delta):
    global timer
    timer += delta*hardness

    if timer > INTERVAL:
        # spawn new asteroid
        asteroid.spawn(player)
        timer = 0
