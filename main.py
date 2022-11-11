import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame import *
import pygame

import asteroid
import bullet
import particles
import spawner
from opengl import surface_to_texture, texID
from player import Player

BG = (0, 0, 0)
FG = (255, 255, 255)

SIZE = 640, 480
FPS = 60


def start():
    # pygame opengl setup
    pygame.init()
    pygame.display.set_mode(SIZE, HWSURFACE | OPENGL | DOUBLEBUF)
    pygame.display.set_caption("pygame asteroids")

    # basic opengl configuration
    glViewport(0, 0, SIZE[0], SIZE[1])
    glDepthRange(0, 1)
    glMatrixMode(GL_PROJECTION)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_BLEND)

    # make "render texture"
    screen_buffer = pygame.Surface(SIZE)

    # TODO write a system for this
    pressing_space = False

    player = Player((500, 300), 30)
    spawner.init()
    particles.init()

    clock = pygame.time.Clock()

    while True:
        delta = clock.get_time() / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pressing_space = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    pressing_space = False

        screen_buffer.fill(BG)

        player.update(delta)
        if pressing_space:
            player.accelerate(delta)
        player.draw(screen_buffer, FG)

        bullet.update(delta)
        bullet.draw(screen_buffer, FG)

        asteroid.update(delta)
        asteroid.draw(screen_buffer, FG)

        particles.update(delta)
        particles.draw(screen_buffer, FG)

        spawner.update(player, delta)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # prepare to render the texture-mapped rectangle
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # glClearColor(0, 0, 0, 1.0)

        # draw texture openGL Texture
        surface_to_texture(screen_buffer)
        glBindTexture(GL_TEXTURE_2D, texID)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(-1, 1)
        glTexCoord2f(0, 1)
        glVertex2f(-1, -1)
        glTexCoord2f(1, 1)
        glVertex2f(1, -1)
        glTexCoord2f(1, 0)
        glVertex2f(1, 1)
        glEnd()

        pygame.display.flip()

        clock.tick(FPS)


if __name__ == '__main__':
    start()
