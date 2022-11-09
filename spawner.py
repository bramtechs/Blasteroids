import asteroid
from player import Player

DURATION = 2
INTERVAL = 2
timer = 0


def init():
    global timer
    timer = 0


def update(player: Player, delta):
    global timer
    timer += delta

    slowness = asteroid.get_count() * 0.3
    if timer > INTERVAL + slowness:
        # spawn new asteroid
        asteroid.spawn(player)
        timer = 0
