import math

import main
import meth
from poly import Polygon
import pygame

BOUNDS = 200
bullets = []


class Bullet(Polygon):
    def __init__(self, pos, vel, radius):
        super().__init__()
        self.pos = pos
        self.prev_pos = pos
        self.vel = vel
        self.radius = radius

    def update(self, delta):
        super().update(delta)
        self.prev_pos = self.pos
        scaled_vel = meth.scl_point(self.vel, delta)
        self.pos = meth.add_points(self.pos, scaled_vel)

        # remove out of bounds
        if self.pos[0] < -BOUNDS or self.pos[0] > main.SIZE[0] + BOUNDS or self.pos[1] < -BOUNDS or self.pos[1] > \
                main.SIZE[1] + BOUNDS:
            global bullets
            bullets.remove(self)

    def draw(self, screen, color):
        pygame.draw.line(screen, color, self.pos, self.prev_pos)
        pass

    def gen_vertices(self) -> []:
        return [self.pos, self.prev_pos]


def catch(client):
    for bullet in bullets:
        if bullet.overlaps(client):
            bullets.remove(bullet)
            return True
    return False


def shoot(spawn, angle, speed=400):
    vel = (
        math.cos(math.radians(angle)) * speed,
        math.sin(math.radians(angle)) * speed
    )
    bullets.append(Bullet(spawn, vel, 3))


def update(delta):
    for bullet in bullets:
        bullet.update(delta)


def draw(screen, color):
    for bullet in bullets:
        bullet.draw(screen, color)
