from pygame import *
from poly import Polygon

import main
import math
import meth
import bullet
import asteroid
import pygame

PL_ANGLE = 30
SHOOT_INTERVAL = 0.2
THRUST = 10
CRASH_SPEED = 30
WRAP_BOUNDS = 60


class Player(Polygon):
    def __init__(self, pos, size):
        super().__init__()
        self.pos = pos
        self.size = size
        self.rot = 0
        self.vel = (0, 0)
        self.vertices = self.gen_vertices()
        self.shoot_timer = 0
        self.alive = True

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
        if not self.alive:
            return

        mouse_pos = pygame.mouse.get_pos()

        # point ship at mouse
        self.rot = meth.degrees_between_points(self.pos, mouse_pos)
        super().update(delta)

        # wrap ship around
        if self.pos[0] - self.size < -WRAP_BOUNDS:
            self.pos = meth.add_points(self.pos, (main.SIZE[0], 0))
        if self.pos[0] > main.SIZE[0] + WRAP_BOUNDS:
            self.pos = meth.add_points(self.pos, (-main.SIZE[0], 0))

        if self.pos[1] > main.SIZE[1] + WRAP_BOUNDS:
            self.pos = meth.add_points(self.pos, (0, -main.SIZE[0]))
        if self.pos[1] - self.size < -WRAP_BOUNDS:
            self.pos = meth.add_points(self.pos, (0, main.SIZE[0]))

        # shoot when holding left mouse button
        if pygame.mouse.get_pressed()[0] and self.shoot_timer > SHOOT_INTERVAL:
            bullet.shoot(self.vertices[4], self.rot)
            self.shoot_timer = 0
        self.shoot_timer += delta

        # apply velocity to position
        scaled_vel = meth.scl_point(self.vel, delta)
        self.pos = meth.add_points(self.pos, scaled_vel)

        # detect crashes
        # speed = math.sqrt(self.vel[0] * self.vel[0] + self.vel[1] * self.vel[1])
        if asteroid.overlaps(self):
            self.died()

    def accelerate(self, delta):
        # thrust while holding spacebar
        self.vel = meth.add_points(self.vel, (
            math.cos(math.radians(self.rot)) * THRUST,
            math.sin(math.radians(self.rot)) * THRUST
        ))

    def died(self):
        self.alive = False
        print("died")

    def draw(self, screen, color):
        if not self.alive:
            return

        pygame.draw.line(screen, color, self.vertices[0], self.vertices[4])
        pygame.draw.line(screen, color, self.vertices[1], self.vertices[4])
        pygame.draw.line(screen, color, self.vertices[2], self.vertices[4])
        pygame.draw.line(screen, color, self.vertices[3], self.vertices[4])
        pygame.draw.line(screen, color, self.vertices[0], self.vertices[2])
        pygame.draw.line(screen, color, self.vertices[1], self.vertices[3])
        pygame.draw.line(screen, color, self.vertices[2], self.vertices[3])
        pygame.draw.line(screen, color, self.vertices[3], self.vertices[4])
        pygame.draw.line(screen, color, self.vertices[0], self.vertices[1])
