import math
import random

import pygame.mouse
import asteroid as ast
import main
import gui.labels
import meth
import gui.settings_menu
import gui.background

RED = (255, 0, 0)


class MainMenu:
    def __init__(self):
        self.title = gui.labels.Label(
            (main.SIZE[0] / 2 - 270, 50), font_size=72, segments=10, reversed=False)

        self.background = gui.background.Background()

        y = 300
        h = 80
        margin = 280

        self.buttons = []
        self.buttons.append(
            gui.labels.Label((main.SIZE[0] / 2 - margin, y), font_size=36, segments=10, reversed=False))
        y += h
        self.buttons.append(
            gui.labels.Label((main.SIZE[0] / 2 - margin, y), font_size=36, segments=10, reversed=False))
        y += h
        self.buttons.append(
            gui.labels.Label((main.SIZE[0] / 2 - margin, y), font_size=36, segments=10, reversed=False))

        self.editor = None
        self.settings = None
        self.timer = 0
        self.index = 0

        self.menuAction = -1

    def pressed_key(self, key, game):
        if self.settings is None:
            if key == pygame.K_F3:
                if self.editor is None:
                    self.editor = Editor()
                else:
                    self.editor = None

            if key == pygame.K_s or key == pygame.K_DOWN:
                self.index += 1
            if key == pygame.K_w or key == pygame.K_UP:
                self.index -= 1

            self.index = meth.clamp(self.index, 0, 2)

            # clickly clicky on those menu-items
            if key == pygame.K_RETURN:
                self.menuAction = self.index
                print("pressed menu item " + str(self.menuAction))
                # open settings
                if self.menuAction == 1:
                    self.settings = gui.settings_menu.SettingsMenu()

            if self.editor is not None:
                self.editor.pressed_key(key)
        else:
            self.settings.pressed_key(key)

    def update(self, delta):
        radius = 1.5
        self.title.offset = (
            math.cos(self.timer) * radius,
            math.sin(self.timer) * radius
        )
        for i in range(len(self.buttons)):
            button = self.buttons[i]
            if i == self.index:
                boost = 1.5
            else:
                boost = 1

            button.offset = (
                (math.cos(self.timer) + 1) / 2 * radius * boost,
                -1
            )

        if self.editor is not None:
            self.editor.update(delta)
        if self.settings is not None:
            self.settings.update(delta, self.timer)

        self.background.update(delta)

        self.timer += delta

    def draw(self, screen, color):
        #self.background.render(screen, color)
        self.title.render(screen, color, "Blasteroids!")

        if self.settings is None:
            self.buttons[0].render(screen, color, "Play")
            self.buttons[1].render(screen, color, "Settings")
            self.buttons[2].render(screen, color, "Quit")

            # draw cursor
            pygame.draw.rect(screen, color,
                             (self.buttons[self.index].pos[0] - 50, self.buttons[self.index].pos[1], 30, 30))
        else:
            self.settings.draw(screen, color)

        if self.editor is not None:
            self.editor.draw(screen, color)
