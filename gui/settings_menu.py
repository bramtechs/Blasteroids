import pygame
import palettes

import spawner

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

        self.should_quit = False
        self.index = 0
        self.options = []
        self.selectors = []

        sel_offset = 400
        self.options.append(
            gui.labels.Label((main.SIZE[0] / 2 - margin, y), font_size=28, segments=10, reversed=False))
        self.selectors.append(gui.selector.Selector((main.SIZE[0]-sel_offset, y), [
            "Terminal",
            "Monochrome",
            "Ocean",
            "Strawberry",
            "Werewolf",
            "New Vegas",
            "Miami",
            "Hotpink",
            "Toxic",
            "LSD",
        ]))

        y += h
        self.options.append(
            gui.labels.Label((main.SIZE[0] / 2 - margin, y), font_size=28, segments=10, reversed=False))
        self.selectors.append(gui.selector.Selector((main.SIZE[0]-sel_offset, y), [
            "ON",
            "OFF"
        ]))

        y += h

        self.options.append(
            gui.labels.Label((main.SIZE[0] / 2 - margin, y), font_size=28, segments=10, reversed=False))

    def update(self, delta, timer):
        radius = 1.2
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

        # apply settings
        palettes.set_color(self.selectors[0].index, timer)
        spawner.set_hard(self.selectors[1].index == 0)

    def pressed_key(self, key):
        if key == pygame.K_s or key == pygame.K_DOWN:
            self.index += 1
        if key == pygame.K_w or key == pygame.K_UP:
            self.index -= 1

        self.index = meth.clamp(self.index, 0, 2)

        for i in range(len(self.selectors)):
            self.selectors[i].focused = False

        if self.index < len(self.selectors):
            self.selectors[self.index].focused = True

        # pass key input to selectors
        for sel in self.selectors:
            sel.pressed_key(key)

        # check for back button pressed
        if key == pygame.K_RETURN and self.index == len(self.selectors):
            print("left settings")
            self.should_quit = True

    def draw(self, screen, color):
        self.title.render(screen, color, "Settings")
        self.options[0].render(screen, color, "Colorscheme")
        self.options[1].render(screen, color, "Hard mode")
        self.options[2].render(screen, color, "Back")

        # draw cursor
        pygame.draw.rect(screen, color,
                         (self.options[self.index].pos[0] - 50, self.options[self.index].pos[1], 30, 30))

        # draw selectors
        for sel in self.selectors:
            sel.render(screen, color)
