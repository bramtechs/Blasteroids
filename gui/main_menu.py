import random

import pygame.mouse
import asteroid as ast
import main
import gui.labels

RED = (255, 0, 0)


# unused
class Editor:
    def __init__(self):
        self.title = gui.labels.Label((10, main.SIZE[1] / 2))
        self.points = [[]]
        self.timer = 0

        self.colors = []
        for i in range(128):
            col = (
                random.randint(150, 255),
                random.randint(150, 255),
                random.randint(150, 255),
                255
            )
            self.colors.append(col)

    def update(self, delta):
        self.timer += delta

    def pressed_key(self, key):
        if key == pygame.K_RETURN:
            self.editor.place_vertex()
        if key == pygame.K_SPACE:
            self.editor.place_new()
        if key == pygame.K_BACKSPACE:
            self.editor.undo()
        if key == pygame.K_p:
            self.editor.export()

    def draw(self, screen, color):
        i = 0
        for a in self.points:
            col = (255, 255, 255, 255)
            if i < len(self.colors):
                col = self.colors[i]

            if len(a) >= 2:
                pygame.draw.polygon(screen, col, a, 1)
            i += 1
        self.title.render(screen, RED, "editor")

    def place_vertex(self):
        if len(self.points) == 0:
            self.points.append([])

        self.points[len(self.points) - 1].append([*pygame.mouse.get_pos()])
        print("Placed point")

    def place_new(self):
        # don't allow new asteroid if current asteroid has no vertices
        if len(self.points[len(self.points) - 1]) > 0:
            self.points.append([])
            print("Placed new asteroid")

    def export(self):
        for point in self.points:
            print(point)
            ast.asteroids.append(ast.CustomAsteroid(point))
        print("export")

    def undo(self):
        if len(self.points) > 0:
            last = len(self.points) - 1
            if len(self.points[last]) > 0:
                self.points[len(self.points) - 1].pop()
            else:
                self.points.pop()
                print("popped last vertex")
        print("Undo")


class MainMenu:
    def __init__(self):
        self.title = gui.labels.Label((main.SIZE[0]/2-200, 30), font_size=72, segments=10)
        self.editor = None

    def pressed_key(self, key):
        if key == pygame.K_F3:
            if self.editor is None:
                self.editor = Editor()
            else:
                self.editor = None

        if self.editor is not None:
            self.editor.pressed_key(key)

    def update(self, delta):
        if self.editor is not None:
            self.editor.update(delta)

    def draw(self, screen, color):
        self.title.render(screen, color, "Blasteroids!")

        if self.editor is not None:
            self.editor.draw(screen, color)
