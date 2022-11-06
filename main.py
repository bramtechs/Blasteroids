import math
import random

import pygame
import sys

BG = (0, 0, 0)
FG = (255, 255, 255)

FPS = 60

PL_ANGLE = 30

world = []


class Player:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    def update(self, delta):
        pass

    def draw(self, screen):
        global world

        # point ship at mouse
        mouse_pos = pygame.mouse.get_pos()
        angle = degrees_between_points(self.pos, mouse_pos)

        draw_cone(screen, self.pos, self.size, angle)

        # draw raycast
        ray_end = raycast_get_closest_point(self.pos, angle)
        pygame.draw.line(screen, (255, 0, 0), self.pos, ray_end)


class GameObject:
    def __init__(self):
        global world
        world.append(self)

    def overlaps(self, begin, end) -> (int, int):
        return None


class Asteroid(GameObject):
    def __init__(self, pos, radius, samples, seed=69):
        super().__init__()
        self.pos = pos
        self.radius = radius
        self.rot = 0
        self.seed = seed
        self.samples = samples
        self.closest = 0
        self.vertices = self.gen_vertices()

    def gen_vertices(self):
        inner_radius = 10
        random.seed(self.seed)

        vertices = []
        angle_per_seg = 360 / self.samples
        for i in range(self.samples):
            angle = angle_per_seg * i + self.rot
            x = self.radius * math.cos(math.radians(angle))
            y = self.radius * math.sin(math.radians(angle))

            inner_angle = random.randrange(0, 360)
            inner_x = math.cos(math.radians(inner_angle + self.rot)) * inner_radius
            inner_y = math.sin(math.radians(inner_angle + self.rot)) * inner_radius

            result = (self.pos[0] + x + inner_x, self.pos[1] + y + inner_y)
            vertices.append(result)
        return vertices

    def update(self, delta):
        self.rot += delta * 10
        self.vertices = self.gen_vertices()

    def draw(self, screen):
        for i in range(len(self.vertices) - 1):
            color = (0, 255, 0)
            if self.closest == i:
                color = (255, 0, 0)
            pygame.draw.line(screen, color, self.vertices[i], self.vertices[i + 1])

        pygame.draw.line(screen, (0, 255, 0), self.vertices[0], self.vertices[len(self.vertices) - 1])

        # pygame.draw.circle(screen, (0, 50, 255), self.pos, self.radius, 1)

    def overlaps(self, begin, end) -> (int, int):
        segments = []
        margin = 20
        smallest = sys.float_info.max
        smallest_index = 0
        for i in range(len(self.vertices) - 1):
            segments.append((self.vertices[i], self.vertices[i + 1]))
            dis = distance_point_to_line(end, self.vertices[i], self.vertices[i + 1])
            if smallest > dis:
                smallest = dis
                smallest_index = i
        if smallest < margin:
            # get intersection
            a = (self.vertices[smallest_index], self.vertices[smallest_index + 1])
            b = (begin, end)
            return line_intersection(a, b)
        return None


def draw_cone(screen, pos, radius, rot):
    x = math.cos(math.radians(rot + 180 + PL_ANGLE)) * radius + pos[0]
    y = math.sin(math.radians(rot + 180 + PL_ANGLE)) * radius + pos[1]
    top_left = (x, y)

    x = math.cos(math.radians(rot + 180 - PL_ANGLE)) * radius + pos[0]
    y = math.sin(math.radians(rot + 180 - PL_ANGLE)) * radius + pos[1]
    bot_left = (x, y)

    x = math.cos(math.radians(rot + 180 + PL_ANGLE / 2)) * radius + pos[0]
    y = math.sin(math.radians(rot + 180 + PL_ANGLE / 2)) * radius + pos[1]
    top_left_inner = (x, y)

    x = math.cos(math.radians(rot + 180 - PL_ANGLE / 2)) * radius + pos[0]
    y = math.sin(math.radians(rot + 180 - PL_ANGLE / 2)) * radius + pos[1]
    bot_left_inner = (x, y)

    x = math.cos(math.radians(rot)) * radius + pos[0]
    y = math.sin(math.radians(rot)) * radius + pos[1]
    right = (x, y)

    pygame.draw.line(screen, FG, top_left, right)
    pygame.draw.line(screen, FG, bot_left, right)
    pygame.draw.line(screen, FG, top_left_inner, right)
    pygame.draw.line(screen, FG, bot_left_inner, right)
    pygame.draw.line(screen, FG, top_left, top_left_inner)
    pygame.draw.line(screen, FG, bot_left, bot_left_inner)
    pygame.draw.line(screen, FG, top_left_inner, bot_left_inner)
    pygame.draw.line(screen, FG, bot_left_inner, right)
    pygame.draw.line(screen, FG, top_left, bot_left)

    # pygame.draw.circle(screen, (255, 0, 0), player["pos"], 2)
    # pygame.draw.circle(screen, (200, 60, 60), player["pos"], player["size"], 1)


def degrees_between_points(src, target):
    delta_x = target[0] - src[0]
    delta_y = target[1] - src[1]
    return math.degrees(math.atan2(delta_y, delta_x))


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


# https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
def line_intersection(first, second) -> (int, int):
    xdiff = (first[0][0] - first[1][0], second[0][0] - second[1][0])
    ydiff = (first[0][1] - first[1][1], second[0][1] - second[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*first), det(*second))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def raycast_get_closest_point(source, angle):
    steps = 100
    step_distance = 10

    scan_x = source[0]
    scan_y = source[1]
    touching = False

    i = 0
    while not touching and i < steps:
        scan_x = source[0] + math.cos(math.radians(angle)) * i * step_distance
        scan_y = source[0] + math.sin(math.radians(angle)) * i * step_distance
        for item in world:
            assert (issubclass(type(item), GameObject))
            overlaps = item.overlaps(source, (scan_x, scan_y))
            if overlaps is not None:
                scan_x = overlaps[0]
                scan_y = overlaps[1]
                touching = True
                break
        i += 1

    return scan_x, scan_y


def start():
    pygame.init()
    size = width, height = 640, 480

    player = Player((200, 200), 30)
    screen = pygame.display.set_mode(size)

    asteroid = Asteroid((450, 80), 70, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        delta = 1 / FPS

        screen.fill(BG)

        player.update(delta)
        player.draw(screen)

        asteroid.update(delta)
        asteroid.draw(screen)
        pygame.display.flip()

        pygame.time.wait(int(1000 / FPS))


if __name__ == '__main__':
    start()
