import math
import random

import pygame
import sys

BG = (0, 0, 0)
FG = (255, 255, 255)

FPS = 60

PL_ANGLE = 30


class Player:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    def update(self,delta):
        pass

    def draw(self, screen):
        # point ship at mouse
        mouse_pos = pygame.mouse.get_pos()
        angle = degrees_between_points(self.pos, mouse_pos)

        draw_cone(screen, self.pos, self.size, angle)

        # draw raycast
        ray_end = raycast_get_closest_point(self.pos, angle)
        pygame.draw.line(screen, (255, 0, 0), self.pos, ray_end)


class Asteroid:
    def __init__(self, pos, radius, samples, seed=69):
        self.pos = pos
        self.radius = radius
        self.rot = 0
        self.vertices = self.gen_vertices(seed, samples)

    def gen_vertices(self, seed, samples):
        inner_radius = 10
        random.seed(seed)

        vertices = []
        angle_per_seg = 360 / samples
        for i in range(samples):
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
        pass

    def draw(self, screen):
        for i in range(len(self.vertices) - 1):
            pygame.draw.line(screen, (0, 255, 0), self.vertices[i], self.vertices[i + 1])
        pygame.draw.line(screen, (0, 255, 0), self.vertices[0], self.vertices[len(self.vertices) - 1])

        pygame.draw.circle(screen, (0, 50, 255), self.pos, self.radius, 1)


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


def raycast_get_closest_point(source, angle):
    max_range = 5000

    x = source[0] + math.cos(math.radians(angle)) * max_range
    y = source[0] + math.sin(math.radians(angle)) * max_range

    return (x, y)


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
