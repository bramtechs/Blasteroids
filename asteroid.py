import bullet
import main
import meth
from gui.bar import Bar
from player import Player
from poly import Polygon
import random
import math
import pygame

MIN_RADIUS = 20
SPLIT_FACTOR = 2
asteroids = []

OOB = main.SIZE[0] + 400
SPAWN_RANGE = main.SIZE[0] + 200


class Asteroid(Polygon):
    def __init__(self, pos, radius=100, samples=30, vel=(0, 0), game=None):
        super().__init__()
        self.pos = pos
        self.vel = vel
        self.radius = radius
        assert (self.radius > MIN_RADIUS)
        self.rot = 0
        self.seed = random.randint(0, 10000)
        self.rot_speed = random.randint(-30, 30)
        self.samples = samples

        # ewww
        self.game = game
        assert (self.game is not None)

        self.rand_angles = []
        for i in range(self.samples):
            self.rand_angles.append(random.randrange(0, 360))

        self.health = radius
        self.max_health = self.health

        self.vertices = self.gen_vertices()
        self.bounds = (self.pos[0] - self.radius, self.pos[1] - self.radius, self.radius * 2, self.radius * 2)

        self.bar = Bar()

    def gen_vertices(self) -> []:
        inner_radius = 10
        vertices = []
        angle_per_seg = 360 / self.samples
        for i in range(self.samples):
            angle = angle_per_seg * i + self.rot
            x = self.radius * math.cos(math.radians(angle))
            y = self.radius * math.sin(math.radians(angle))

            inner_angle = self.rand_angles[i]
            inner_x = math.cos(math.radians(inner_angle + self.rot)) * inner_radius
            inner_y = math.sin(math.radians(inner_angle + self.rot)) * inner_radius

            result = (self.pos[0] + x + inner_x, self.pos[1] + y + inner_y)
            vertices.append(result)
        return vertices

    def update(self, delta, game):
        super().update(delta)
        self.rot += delta * self.rot_speed

        global asteroids

        # catch incoming bullets
        player = bullet.catch(self)
        if player is not None:
            self.health -= 10
            if self.health > 0:
                player.score += 10
            else:
                player.score += self.radius
                self.game.shake(0.2, 3)

        if self.health <= 0:
            if self.radius / SPLIT_FACTOR > MIN_RADIUS:
                # spawn two new ones
                pos = self.vertices[random.randint(0, int(len(self.vertices) / 2))]
                pos_alter = self.vertices[random.randint(int(len(self.vertices) / 2), int(len(self.vertices) - 1))]
                samples = random.randint(5, 15)
                asteroids.append(Asteroid(pos, self.radius / SPLIT_FACTOR, samples, self.vel, game))
                asteroids.append(Asteroid(pos_alter, self.radius / SPLIT_FACTOR, samples, self.vel, game))
            # ded
            asteroids.remove(self)
            self.game.shake(0.1, 1)
            return

        # remove when out of bounds
        dist = math.dist(self.pos, meth.scl_point(main.SIZE, 0.5))
        if dist > OOB:
            asteroids.remove(self)

        # drift through space
        vel_scaled = meth.scl_point(self.vel, delta)
        self.pos = meth.add_points(self.pos, vel_scaled)

        # crash into other asteroids
        other = overlaps_get(self, self)
        if other is not None and other.radius > self.radius:
            self.health -= other.radius

        self.bar.update(delta, self.health, 0, self.max_health)

    def draw(self, screen, color):
        pygame.draw.polygon(screen, color, self.vertices, 1)

        self.bar.draw(screen, color, self.pos, (self.bounds[2], self.bounds[3]))
        # pygame.draw.rect(screen, (255, 0, 0), self.bounds, 1)


class CustomAsteroid(Asteroid):
    def __init__(self, vertices, radius=100, samples=30, vel=(0, 0)):
        super().__init__((0, 0), radius, samples, vel)
        self.vertices = vertices

    def gen_vertices(self) -> []:
        return self.vertices


def overlaps(other: Polygon, exclude: Asteroid = None) -> bool:
    return overlaps_get(other, exclude) is not None


def overlaps_get(other: Polygon, exclude: Asteroid = None) -> Polygon | None:
    for asteroid in asteroids:
        if other.overlaps(asteroid) and asteroid is not exclude:
            return asteroid
    return None


def init_test():
    asteroids.append(Asteroid((450, 80), 70, 30))
    asteroids.append(Asteroid((40, 300), 40, 10))
    asteroids.append(Asteroid((240, 260), 80, 20))


def spawn(player: Player):
    # spawn the new asteroid
    radius = random.randint(21, 80)

    # choose spawn
    angle = random.randint(0, 359)
    pos = (
        math.cos(math.radians(angle)) * SPAWN_RANGE + main.SIZE[0] * 0.5,
        math.sin(math.radians(angle)) * SPAWN_RANGE + main.SIZE[1] * 0.5
    )
    samples = random.randint(8, 15)
    deg_towards = meth.degrees_between_points(pos, player.pos)
    power = random.randint(30, 150)
    vel = (
        math.cos(math.radians(deg_towards)) * power,
        math.sin(math.radians(deg_towards)) * power
    )
    asteroids.append(Asteroid(pos, radius, samples, vel, player.game))


def get_count() -> int:
    return len(asteroids)


def update(delta, game):
    for ast in asteroids:
        ast.update(delta, game)


def draw(screen, color):
    for ast in asteroids:
        ast.draw(screen, color)
