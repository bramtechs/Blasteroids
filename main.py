import sys

import pygame

import asteroid
import bullet
import spawner
from player import Player

BG = (0, 0, 0)
FG = (255, 255, 255)

SIZE = 640, 480
FPS = 60


def start():
    pygame.init()

    spawner.init()
    player = Player((500, 300), 30)
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("pygame asteroids")

    # TODO write a system for this
    pressing_space = False

    while True:
        delta = 1 / FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pressing_space = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    pressing_space = False

        screen.fill(BG)

        player.update(delta)
        if pressing_space:
            player.accelerate(delta)
        player.draw(screen, FG)

        bullet.update(delta)
        bullet.draw(screen, FG)

        asteroid.update(delta)
        asteroid.draw(screen, FG)

        spawner.update(player, delta)

        pygame.display.flip()

        pygame.time.wait(int(1000 / FPS))


if __name__ == '__main__':
    start()
