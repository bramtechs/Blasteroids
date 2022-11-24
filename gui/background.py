import pygame

import main


# TODO fix
class Background:
    def __init__(self, h_lines=20, v_lines=10, squeeze=2) -> None:
        self.v_lines = v_lines
        self.h_lines = h_lines
        self.squeeze = squeeze
        self.horizon_y = 0.2  # factor of main.SIZE[1]
        self.timer = 0
        self.speed = 100
        self.spacing = 40

    def update(self, delta):
        self.timer += delta

    def render(self, screen, color):
        horizon = main.SIZE[1]*self.horizon_y
        # vertical lines
        center = main.SIZE[0]/2
        half = int(self.v_lines/2)
        for i in range(-half, half):
            top_x = center + i * 50
            bot_x = center + i * 250
            pygame.draw.line(
                screen, color, (top_x, horizon), (bot_x, main.SIZE[1]))

        # horizontal lines
        for i in range(self.v_lines):
            lerp = (self.timer * self.speed + i *
                    self.spacing) % (main.SIZE[1]-horizon)
            y = horizon + lerp
            pygame.draw.line(
                screen, color, (0, y), (main.SIZE[0], y))
