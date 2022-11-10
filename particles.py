import math
import random

import pygame

import meth

POOL_SIZE = 1024

particles = []


class Particle:
    def __init__(self, pos, vel, radius, is_active=False):
        self.pos = pos
        self.vel = vel
        self.start_radius = radius
        self.life_time = 0
        self.radius = 0
        self.timer = 0.0
        self.is_active = False

    def activate(self, pos, power, radius, life_time):
        self.pos = pos
        self.timer = 0.0
        self.radius = 0
        self.is_active = True
        self.start_radius = radius
        self.life_time = 2

        # rng
        rng = 2
        power += random.randint(power - power / rng, power + power / rng)

        angle = random.randint(0, 359)
        self.vel = (
            math.cos(math.radians(angle)) * power,
            math.sin(math.radians(angle)) * power
        )
        self.is_active = True

    def update(self, delta):
        # deactivate when radius too small
        self.radius = (self.life_time - self.timer) / self.life_time * self.start_radius
        if self.radius <= 0:
            self.is_active = False
        self.timer += delta

        # moving
        vel_scaled = meth.scl_point(self.vel, delta)
        self.pos = meth.add_points(self.pos, vel_scaled)

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, self.pos, self.radius)


def create_empty() -> Particle:
    return Particle(
        (0, 0),
        (0, 0),
        0
    )


def init():
    for i in range(POOL_SIZE):
        particles.append(create_empty())


def emit(pos, power, radius, life_time, amount=1):
    done = 0
    for part in particles:
        if not part.is_active:
            if done > amount:
                return
            part.activate(pos, power, radius, life_time)
            done += 1
    print("not enough particles")


def update(delta):
    for part in particles:
        if part.is_active:
            part.update(delta)


def draw(screen, color):
    for part in particles:
        if part.is_active:
            part.draw(screen, color)
