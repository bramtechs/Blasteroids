import pygame
import main
import math
import gui.labels
import random

MAX_SCORES = 10

# {
# "name": "bram",
# "score": 6969,
# "level": 69
# },
# {
# "name": "bram2",
# "score": 6969,
# "level": 69
# }


def collect_scores():
    return [

    ]


class Leaderboard:
    def __init__(self) -> None:
        self.scores = collect_scores()
        self.labels = []
        self.timer = 0
        self.radius = 1.2
        self.title = gui.labels.Label((320, 20), font_size=28)
        self.title_msg = "You crashed :("

        x = main.SIZE[0] / 2 - 160
        y = 120
        for i in range(MAX_SCORES):
            self.labels.append(gui.labels.Label((x, y), font_size=26))
            y += 43

    def update(self, delta):
        for label in self.labels:
            label.offset = (
                math.cos(self.timer) * self.radius,
                math.sin(self.timer) * self.radius
            )

        self.title.offset = (
            math.cos(self.timer) * self.radius,
            math.sin(self.timer) * self.radius
        )

        self.timer += delta

    def draw(self, screen, color):
        for i in range(len(self.labels)):
            # get name if any
            if i < len(self.scores) - 1:
                name = self.scores[i]['name']
                score = self.scores[i]['score']
                level = self.scores[i]['level']
                text = "{}. {} - {} - lvl {}".format(i+1, name, score, level)
            else:
                text = "{}. ...".format(i+1)
            self.labels[i].render(screen, color, text)

        self.title.render(screen, color, self.title_msg)
