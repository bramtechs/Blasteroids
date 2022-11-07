import pygame


class Bar:
    def __init__(self, size=(50, 8)):
        self.size = size
        self.min = 0
        self.max = 1
        self.value = 0.5

    def update(self, delta, value, min, max):
        assert (min < max)
        self.min = min
        self.max = max
        self.value = value

    def get_rect(self, owner_pos, owner_size, w_perc):
        return (
            owner_pos[0] - self.size[0] / 2,
            owner_pos[1] - owner_size[1] / 4,
            self.size[0] * w_perc,
            self.size[1]
        )

    def draw(self, surface, color, owner_pos, owner_size):
        perc = (self.value - self.min) / (self.max - self.min)
        # draw outline
        rect = self.get_rect(owner_pos, owner_size, 1)
        pygame.draw.rect(surface, color, rect, 1)

        # draw inside
        rect = self.get_rect(owner_pos, owner_size, perc)
        pygame.draw.rect(surface, color, rect)
