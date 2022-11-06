from poly import Polygon
import math
import meth
import bullet
import pygame

PL_ANGLE = 30
SHOOT_INTERVAL = 0.2


class Player(Polygon):
    def __init__(self, pos, size):
        super().__init__()
        self.pos = pos
        self.size = size
        self.rot = 0
        self.vertices = self.gen_vertices()
        self.shoot_timer = 0

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

        # point ship at mouse
        self.rot = meth.degrees_between_points(self.pos, mouse_pos)
        super().update(delta)

        if pygame.mouse.get_pressed()[0] and self.shoot_timer > SHOOT_INTERVAL:
            bullet.shoot(self.vertices[4], self.rot)
            self.shoot_timer = 0
        self.shoot_timer += delta

    def draw(self, screen, color):
        pygame.draw.line(screen, color, self.vertices[0], self.vertices[4])
        pygame.draw.line(screen, color, self.vertices[1], self.vertices[4])
        pygame.draw.line(screen, color, self.vertices[2], self.vertices[4])
        pygame.draw.line(screen, color, self.vertices[3], self.vertices[4])
        pygame.draw.line(screen, color, self.vertices[0], self.vertices[2])
        pygame.draw.line(screen, color, self.vertices[1], self.vertices[3])
        pygame.draw.line(screen, color, self.vertices[2], self.vertices[3])
        pygame.draw.line(screen, color, self.vertices[3], self.vertices[4])
        pygame.draw.line(screen, color, self.vertices[0], self.vertices[1])
