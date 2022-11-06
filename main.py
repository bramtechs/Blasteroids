import sys

import pygame

import asteroid
import bullet
from player import Player

BG = (0, 0, 0)
FG = (255, 255, 255)

FPS = 60


def start():
    pygame.init()
    size = width, height = 640, 480

    player = Player((500, 300), 30)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("pygame asteroids")

    asteroid.init_test()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        delta = 1 / FPS

        screen.fill(BG)

        player.update(delta)
        player.draw(screen, FG)

        bullet.update(delta)
        bullet.draw(screen, FG)

        asteroid.update(delta)
        asteroid.draw(screen, FG)

        pygame.display.flip()

        pygame.time.wait(int(1000 / FPS))


if __name__ == '__main__':
    start()
