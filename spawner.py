import asteroid

DURATION = 2
INTERVAL = 1.8
timer = 0
hardness = 0.8


def init():
    global timer
    timer = INTERVAL


def is_hard():
    return hardness > 0.8


def set_hard(hard: bool):
    global hardness

    if hard:
        hardness = 1.2
    else:
        hardness = 0.8


def update(player, delta):
    global timer
    increment = max(hardness + 0.05*player.level, 1.3)
    timer += delta*increment

    if timer > INTERVAL:
        # spawn new asteroid
        asteroid.spawn(player)
        timer = 0
