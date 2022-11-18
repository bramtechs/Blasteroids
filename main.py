import sys
import asyncio
import pygame

import asteroid
import bullet
import particles
import spawner
import player
import gui.labels

BG = (7, 12, 4)
FG = (0, 255, 0)

SIZE = 900, 720
FPS = 60


async def start():
    # pygame opengl setup
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("pygame asteroids")

    # TODO write a system for this
    pressing_space = False

    pl = player.Player((500, 300), 30)
    spawner.init()
    particles.init()

    gui_labels = gui.labels.GUI(pl)

    clock = pygame.time.Clock()

    keep_running = True
    while keep_running:
        delta = clock.get_time() / 1000.0

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                keep_running = False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    pressing_space = True

            if ev.type == pygame.KEYUP:
                if ev.key == pygame.K_SPACE:
                    pressing_space = False

        screen.fill(BG)

        pl.update(delta)
        if pressing_space:
            pl.accelerate(delta)
        pl.draw(screen, FG)

        bullet.update(delta)
        bullet.draw(screen, FG)

        asteroid.update(delta)
        asteroid.draw(screen, FG)

        particles.update(delta)
        particles.draw(screen, FG)

        spawner.update(pl, delta)

        gui_labels.render(screen, delta, FG)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    asyncio.run(start())
