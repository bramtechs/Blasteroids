import time
import pygame

import meth


class Label:
    def __init__(self, pos, font="Ubuntu", segments=5, offset=(1, 1)):
        self.pos = pos
        self.segments = segments
        self.font = pygame.font.SysFont(font, 48)
        self.offset = offset

    def render(self, screen, color, text):
        for i in range(self.segments):
            alpha = (self.segments - i) / self.segments * 255
            img = self.font.render(str(text), True, color)
            img.set_alpha(alpha)
            pos = (self.pos[0] + self.offset[0] * i, self.pos[1] + self.offset[1] * i)
            screen.blit(img, pos)
