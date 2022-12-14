# math was taken
import math


# do I look like a mathematician?
# https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
def distance_point_to_line(point, start, end):
    a = point[0] - start[0]
    b = point[1] - start[1]
    c = end[0] - start[0]
    d = end[1] - start[1]

    dot = a * c + b * d
    len_sq = c * c + d * d
    param = -1
    if len_sq != 0:
        param = dot / len_sq

    if param < 0:
        xx = start[0]
        yy = start[1]
    elif param > 1:
        xx = end[0]
        yy = end[1]
    else:
        xx = start[0] + param * c
        yy = start[1] + param * d

    dx = point[0] - xx
    dy = point[1] - yy
    return math.sqrt(dx * dx + dy * dy)


def degrees_between_points(src, target):
    delta_x = target[0] - src[0]
    delta_y = target[1] - src[1]
    return math.degrees(math.atan2(delta_y, delta_x))


def clamp(value, lower, upper):
    return max(lower, min(value, upper))


def scl_point(base, scl: float):
    return base[0] * scl, base[1] * scl


def div_point(base, div: float):
    return base[0] / div, base[1] / div


def add_points(base, adder):
    return base[0] + adder[0], base[1] + adder[1]


def sub_points(base, adder):
    return base[0] - adder[0], base[1] - adder[1]


def brighten_color(col, amount: int):
    return (
        min(col[0] + amount, 255),
        min(col[1] + amount, 255),
        min(col[2] + amount, 255),
    )
