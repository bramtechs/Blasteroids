import math

TERMINAL = [(7, 12, 4), (0, 255, 0)]
MONOCHROME = [(0, 0, 0), (255, 255, 255)]
OCEAN = [(0, 2, 71), (69, 153, 255)]
STRAWBERRY = [(120, 30, 55), (255, 105, 200)]
NEW_VEGAS = [(31, 18, 0), (255, 234, 46)]
MIAMI = [(201, 0, 104), (0, 229, 255)]
WEREWOLF = [(38, 1, 0), (255, 4, 0)]
HOTPINK = [(255, 0, 255), (255, 255, 255)]
TOXIC = [(0, 255, 20), (255, 0, 208)]
LSD = [(255, 255, 255), (0, 0, 0)]

colors = [TERMINAL, MONOCHROME, OCEAN,
          STRAWBERRY, WEREWOLF, NEW_VEGAS, MIAMI,  HOTPINK, TOXIC, LSD]
active_color = (TERMINAL[0], TERMINAL[1])


def set_color(index: int, timer: float):
    global active_color
    active_color = colors[index]

    lsd_id = 9
    if index == lsd_id:
        colors[lsd_id][0] = (
            abs(math.sin(timer)*255),
            abs(math.cos(timer)*255),
            abs(math.sin(timer*2)*255),
        )
        colors[lsd_id][1] = (
            255-abs(math.sin(timer))*255,
            255-abs(math.cos(timer))*255,
            255-abs(math.sin(timer*2))*255,
        )
