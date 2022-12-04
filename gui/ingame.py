import gui.labels
import gui.bar

import main
import math
import audio


class GUI:
    def __init__(self, player):
        self.player = player
        self.prev_score = 0
        self.score = gui.labels.Label((10, 10))
        self.xpbar = gui.bar.Bar((main.SIZE[0] - 500, 10))

        self.xp_label = gui.labels.Label((10, main.SIZE[1] - 55), font_size=32)
        self.xp_target = 300
        self.prev_xp_target = 0

    def update(self, delta, timer):
        radius = 1.2
        self.score.offset = (
            math.cos(timer) * radius,
            math.sin(timer) * radius
        )
        self.xp_label.offset = (
            math.cos(timer) * radius,
            math.sin(timer) * radius
        )

    def render(self, screen, delta, color):
        # check if score changed
        if self.prev_score < self.player.score:
            #print("score changed")
            if self.player.score > self.xp_target:
                self.prev_xp_target = self.xp_target
                self.xp_target *= 2
                self.player.level += 1
                audio.ins.levelup.play()

        self.prev_score = self.player.score

        self.score.render(screen, color, int(self.player.score))
        self.xpbar.update(delta, self.player.score,
                          self.prev_xp_target, self.xp_target)
        self.xpbar.draw(
            screen, color, (main.SIZE[0] / 2, main.SIZE[1] - 30), (main.SIZE[0], 30))
        self.xp_label.render(screen, color, "Level " +
                             str(self.player.level+1))
