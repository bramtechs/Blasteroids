import sys
import asyncio
import pygame

import asteroid
import bullet
import particles
import spawner
import player
import gui.labels
import gui.main_menu

BG = (7, 12, 4)
FG = (0, 255, 0)

SIZE = 900, 720
FPS = 60

# states enum
STATE_MENU = 0
STATE_GAME = 1


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

    menu = gui.main_menu.MainMenu()

    keep_running = True
    while keep_running:
        delta = clock.get_time() / 1000.0

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                keep_running = False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    pressing_space = True
                if menu is not None:
                    menu.pressed_key(ev.key)

            if ev.type == pygame.KEYUP:
                if ev.key == pygame.K_SPACE:
                    pressing_space = False

        screen.fill(BG)

        # update player in game
        if menu is None:
            if pressing_space:
                pl.accelerate(delta)
            # update
            spawner.update(pl, delta)
            pl.update(delta)
            pl.draw(screen, FG)

        bullet.update(delta)
        bullet.draw(screen, FG)

        asteroid.update(delta)
        asteroid.draw(screen, FG)

        particles.update(delta)
        particles.draw(screen, FG)

        if menu is None:
            gui_labels.render(screen, delta, FG)

        if menu is not None:
            menu.update(delta)
            menu.draw(screen, FG)

        pygame.display.update()
        clock.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    asyncio.run(start())
