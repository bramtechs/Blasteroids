import pygame

import main


# TODO fix
# https://math.stackexchange.com/questions/4337918/using-perspective-rendering-to-render-a-3d-point

class Background:
    def __init__(self, cells=40) -> None:
        self.timer = 0
        self.cells = cells
        self.size = 100

    def update(self, delta):
        self.timer += delta

    def render(self, screen, color):
        pass
