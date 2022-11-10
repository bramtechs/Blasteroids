import asteroid
from player import Player

DURATION = 2
INTERVAL = 1.8
timer = 0


def init():
    global timer
    timer = 0


def update(player: Player, delta):
    global timer
    timer += delta

    if timer > INTERVAL:
        # spawn new asteroid
        asteroid.spawn(player)
        timer = 0
