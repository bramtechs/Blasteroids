import time
import pygame

import main
import meth
from gui.bar import Bar
from player import Player


class Label:
    def __init__(self, pos, font="FFFFORWA.TTF", font_size=48, segments=5, offset=(1, 1), reversed=True):
        self.pos = pos
        self.segments = segments
        self.font = pygame.font.Font(font, font_size)
        self.font_size = font_size
        self.offset = offset
        self.reversed = reversed

    def render(self, screen, color, text):
        for i in range(self.segments):
            if self.reversed:
                alpha = (self.segments - i) / self.segments * 200
            else:
                alpha = i / self.segments * 200
            img = self.font.render(str(text), True, color)
            img.set_alpha(alpha)
            pos = (self.pos[0] + self.offset[0] * i, self.pos[1] + self.offset[1] * i)
            screen.blit(img, pos)


class GUI:
    def __init__(self, player: Player):
        self.player = player
        self.prev_score = 0
        self.score = Label((10, 10))
        self.xpbar = Bar((main.SIZE[0] - 500, 10))

        self.xp_level = 0
        self.xp_label = Label((10, main.SIZE[1] - 55), font_size=32)
        self.xp_target = 300
        self.prev_xp_target = 0

    def render(self, screen, delta, color):
        # check if score changed
        if self.prev_score < self.player.score:
            print("score changed")
            if self.player.score > self.xp_target:
                self.prev_xp_target = self.xp_target
                self.xp_target *= 2
                self.xp_level += 1
        self.prev_score = self.player.score

        self.score.render(screen, color, int(self.player.score))
        self.xpbar.update(delta, self.player.score, self.prev_xp_target, self.xp_target)
        self.xpbar.draw(screen, color, (main.SIZE[0] / 2, main.SIZE[1] - 30), (main.SIZE[0], 30))
        self.xp_label.render(screen, color, "Level " + str(self.xp_level))
