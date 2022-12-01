import math
import gui.labels


class Leaderboard:
    def __init__(self):
        self.timer = 0
        self.flash_timer = 0
        self.radius = 1.2
        self.title = gui.labels.Label((320, 130), font_size=28)
        self.title_msg = "You crashed :("

    def update(self, delta):
        self.title.offset = (
            math.cos(self.timer) * self.radius,
            math.sin(self.timer) * self.radius
        )

        self.timer += delta
        self.flash_timer += delta

    def draw(self, screen, color):
        if self.flash_timer < 1:
            self.title.render(screen, color, self.title_msg)
        elif self.flash_timer > 2:
            self.flash_timer = 0
