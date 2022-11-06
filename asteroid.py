import bullet
from poly import Polygon
import random
import math
import pygame

asteroids = []


class Asteroid(Polygon):
    def __init__(self, pos, radius, samples):
        super().__init__()
        self.pos = pos
        self.radius = radius
        self.rot = 0
        self.seed = random.randint(0, 10000)
        self.rot_speed = random.randint(-30, 30)
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
        self.rot += delta * self.rot_speed

        # catch incoming bullets
        bullet.catch(self)

    def draw(self, screen, color):
        for i in range(len(self.vertices) - 1):
            pygame.draw.line(screen, color, self.vertices[i], self.vertices[i + 1])
        pygame.draw.line(screen, color, self.vertices[0], self.vertices[len(self.vertices) - 1])


def init_test():
    asteroids.append(Asteroid((450, 80), 70, 30))
    asteroids.append(Asteroid((40, 300), 40, 10))
    asteroids.append(Asteroid((240, 260), 80, 20))


def update(delta):
    for ast in asteroids:
        ast.update(delta)


def draw(screen, color):
    for ast in asteroids:
        ast.draw(screen, color)
