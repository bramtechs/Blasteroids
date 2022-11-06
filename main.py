import math
import random

import pygame
import sys

BG = (0, 0, 0)
FG = (255, 255, 255)

FPS = 60

PL_ANGLE = 30

world = []


class Polygon:
    def __init__(self):
        global world
        world.append(self)
        self.vertices = []

    def update(self, delta):
        self.vertices = self.gen_vertices()

    def draw(self, screen):
        pass

    def gen_vertices(self) -> []:
        pass

    # https://www.youtube.com/watch?v=7Ik2vowGcU0
    def overlaps(self, other) -> bool:
        assert (self is not other)
        poly1 = self
        poly2 = other

        for shape in range(2):
            if shape == 1:
                poly1 = other
                poly2 = self

            for a in range(len(poly1.vertices)):
                b = (a + 1) % len(poly1.vertices)

                # get the normal of the edge
                axis_proj = (
                    -(poly1.vertices[b][1] - poly1.vertices[a][1]),
                    poly1.vertices[b][0] - poly1.vertices[a][0]
                )

                # work out min and max 1D points for self
                min_r1 = sys.float_info.max
                max_r1 = sys.float_info.min

                for p in range(len(poly1.vertices)):
                    q = poly1.vertices[p][0] * axis_proj[0] + poly1.vertices[p][1] * axis_proj[1]
                    min_r1 = min(min_r1, q)
                    max_r1 = max(max_r1, q)

                # work out min and max 1D points for other
                min_r2 = sys.float_info.max
                max_r2 = sys.float_info.min

                for p in range(len(poly2.vertices)):
                    q = poly2.vertices[p][0] * axis_proj[0] + poly2.vertices[p][1] * axis_proj[1]
                    min_r2 = min(min_r2, q)
                    max_r2 = max(max_r2, q)

                # check if extents of shadows overlap
                if not (max_r2 >= min_r1 and max_r1 >= min_r2):
                    return False
        return True


class Player(Polygon):
    def __init__(self, pos, size):
        super().__init__()
        self.pos = pos
        self.size = size
        self.rot = 0
        self.vertices = self.gen_vertices()

    def gen_vertices(self) -> []:
        vertices = []
        # 0 top left
        x = math.cos(math.radians(self.rot + 180 + PL_ANGLE)) * self.size + self.pos[0]
        y = math.sin(math.radians(self.rot + 180 + PL_ANGLE)) * self.size + self.pos[1]
        vertices.append((x, y))

        # 1 bot left
        x = math.cos(math.radians(self.rot + 180 - PL_ANGLE)) * self.size + self.pos[0]
        y = math.sin(math.radians(self.rot + 180 - PL_ANGLE)) * self.size + self.pos[1]
        vertices.append((x, y))

        # 2 top left inner
        x = math.cos(math.radians(self.rot + 180 + PL_ANGLE / 2)) * self.size + self.pos[0]
        y = math.sin(math.radians(self.rot + 180 + PL_ANGLE / 2)) * self.size + self.pos[1]
        vertices.append((x, y))

        # 3 bot left inner
        x = math.cos(math.radians(self.rot + 180 - PL_ANGLE / 2)) * self.size + self.pos[0]
        y = math.sin(math.radians(self.rot + 180 - PL_ANGLE / 2)) * self.size + self.pos[1]
        vertices.append((x, y))

        # 4 right
        x = math.cos(math.radians(self.rot)) * self.size + self.pos[0]
        y = math.sin(math.radians(self.rot)) * self.size + self.pos[1]
        vertices.append((x, y))

        return vertices

    def update(self, delta):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            self.pos = mouse_pos

        # point ship at mouse
        mouse_pos = pygame.mouse.get_pos()
        self.rot = degrees_between_points(self.pos, mouse_pos)
        super().update(delta)

    def draw(self, screen):
        global world

        if self.overlaps(world[1]):
            color = (255, 0, 0)
        else:
            color = (255, 255, 255)

        pygame.draw.line(screen, color, self.vertices[0], self.vertices[4])
        pygame.draw.line(screen, color, self.vertices[1], self.vertices[4])
        pygame.draw.line(screen, color, self.vertices[2], self.vertices[4])
        pygame.draw.line(screen, color, self.vertices[3], self.vertices[4])
        pygame.draw.line(screen, color, self.vertices[0], self.vertices[2])
        pygame.draw.line(screen, color, self.vertices[1], self.vertices[3])
        pygame.draw.line(screen, color, self.vertices[2], self.vertices[3])
        pygame.draw.line(screen, color, self.vertices[3], self.vertices[4])
        pygame.draw.line(screen, color, self.vertices[0], self.vertices[1])


class Asteroid(Polygon):
    def __init__(self, pos, radius, samples, seed=69):
        super().__init__()
        self.pos = pos
        self.radius = radius
        self.rot = 0
        self.seed = seed
        self.samples = samples
        self.vertices = self.gen_vertices()

    def gen_vertices(self) -> []:
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
        super().update(delta)
        self.rot += delta * 10

    def draw(self, screen):
        for i in range(len(self.vertices) - 1):
            color = (0, 255, 0)
            pygame.draw.line(screen, color, self.vertices[i], self.vertices[i + 1])
        pygame.draw.line(screen, (0, 255, 0), self.vertices[0], self.vertices[len(self.vertices) - 1])


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
