import time
import pygame

import main
import math
import meth
from gui.bar import Bar


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
            pos = (self.pos[0] + self.offset[0] * i,
                   self.pos[1] + self.offset[1] * i)
            screen.blit(img, pos)
