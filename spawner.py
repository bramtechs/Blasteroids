import asteroid
from player import Player

DURATION = 2
INTERVAL = 1.8
timer = 0
hardness = 0.8


def init():
    global timer
    timer = INTERVAL


def set_hard(hard: bool):
    global hardness

    if hard:
        hardness = 1.3
    else:
        hardness = 0.8


def update(player: Player, delta):
    global timer
    timer += delta*hardness + 0.1*player.level

    if timer > INTERVAL:
        # spawn new asteroid
        asteroid.spawn(player)
        timer = 0
