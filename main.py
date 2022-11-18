import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame import *
import pygame

import asteroid
import bullet
import particles
import spawner
from gui import labels
from opengl import surface_to_texture, texID
from player import Player

BG = (7, 12, 4)
FG = (0, 255, 0)

SIZE = 900, 720
FPS = 60


def start():
    # pygame opengl setup
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("pygame asteroids")

    # TODO write a system for this
    pressing_space = False

    player = Player((500, 300), 30)
    spawner.init()
    particles.init()

    gui_labels = labels.GUI(player)

    clock = pygame.time.Clock()

    # shaders

    while True:
        delta = clock.get_time() / 1000.0

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    pressing_space = True

            if ev.type == pygame.KEYUP:
                if ev.key == pygame.K_SPACE:
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

        particles.update(delta)
        particles.draw(screen, FG)

        spawner.update(player, delta)

        gui_labels.render(screen, delta, FG)

        pygame.display.flip()

        clock.tick(FPS)


if __name__ == '__main__':
    start()
