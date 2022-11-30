import pygame
import gui.labels

import math
import audio


class Selector:
    def __init__(self, pos, options) -> None:
        self.pos = pos
        self.options = options
        self.index = 0
        self.focused = False

        # generate labels
        self.labels = []
        for _ in options:
            self.labels.append(
                gui.labels.Label(pos, font_size=28,
                                 segments=10, reversed=False)
            )

    def update(self, delta, timer, radius=1.2):
        for i in range(len(self.labels)):
            label = self.labels[i]
            if i == self.focused:
                boost = 1.5
            else:
                boost = 1
            label.offset = (
                (math.cos(timer) + 1) / 2 * radius * boost,
                -1
            )

    def pressed_key(self, key):
        if not self.focused:
            return
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.index -= 1
            audio.ins.cursor.play()
            print("left")
        if key == pygame.K_RIGHT or key == pygame.K_d:
            self.index += 1
            audio.ins.cursor.play()
            print("right")

        # wrap index around
        if self.index < 0:
            self.index = len(self.options)-1
        if self.index >= len(self.options):
            self.index = 0

    def render(self, screen, color):
        self.labels[self.index].render(screen, color, self.options[self.index])
