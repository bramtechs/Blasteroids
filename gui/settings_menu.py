import pygame

import gui.selector
import gui.labels

import main
import math
import meth


class SettingsMenu:
    def __init__(self):
        self.title = gui.labels.Label(
            (main.SIZE[0] / 2 - 100, 180), font_size=32, segments=10, reversed=False)

        y = 300
        h = 80
        margin = 280

        self.index = 0
        self.options = []
        self.selectors = []

        self.options.append(
            gui.labels.Label((main.SIZE[0] / 2 - margin, y), font_size=28, segments=10, reversed=False))

        sel_offset = 400
        self.selectors.append(
            gui.selector.Selector((main.SIZE[0]-sel_offset, y), [
                "Model 1",
                "Model 2",
                "Model 3",
            ]))

        y += h
        self.options.append(
            gui.labels.Label((main.SIZE[0] / 2 - margin, y), font_size=28, segments=10, reversed=False))
        self.selectors.append(gui.selector.Selector((main.SIZE[0]-sel_offset, y), [
            "Terminal",
            "Ocean",
            "Strawberry",
            "New Vegas",
        ]))

        y += h
        self.options.append(
            gui.labels.Label((main.SIZE[0] / 2 - margin, y), font_size=28, segments=10, reversed=False))
        self.selectors.append(gui.selector.Selector((main.SIZE[0]-sel_offset, y), [
            "ON",
            "OFF"
        ]))

    def update(self, delta, timer):
        radius = 1.5
        self.title.offset = (
            math.cos(timer) * radius,
            math.sin(timer) * radius
        )

        for i in range(len(self.options)):
            button = self.options[i]
            if i == self.index:
                boost = 1.5
            else:
                boost = 1

            button.offset = (
                (math.cos(timer) + 1) / 2 * radius * boost,
                -1
            )

        for sel in self.selectors:
            sel.update(delta, timer, radius)

    def pressed_key(self, key):
        if key == pygame.K_s or key == pygame.K_DOWN:
            self.index += 1
        if key == pygame.K_w or key == pygame.K_UP:
            self.index -= 1

        self.index = meth.clamp(self.index, 0, 2)

        for i in range(len(self.selectors)):
            self.selectors[i].focused = False
        self.selectors[self.index].focused = True

        # pass key input to selectors
        for sel in self.selectors:
            sel.pressed_key(key)

    def draw(self, screen, color):
        self.title.render(screen, color, "Settings")
        self.options[0].render(screen, color, "Spaceship")
        self.options[1].render(screen, color, "Colorscheme")
        self.options[2].render(screen, color, "Hard mode")

        # draw cursor
        pygame.draw.rect(screen, color,
                         (self.options[self.index].pos[0] - 50, self.options[self.index].pos[1], 30, 30))

        # draw selectors
        for sel in self.selectors:
            sel.render(screen, color)
