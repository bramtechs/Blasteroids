#!/usr/bin/python
import random
import sys
import asyncio
import pygame

import asteroid
import bullet
import meth
import particles
import spawner
import player
import gui.labels
import gui.main_menu

SIZE = 900, 720
FPS = 60

# states enum
STATE_MENU = 0
STATE_GAME = 1


# OOP pain
class Game:

    def __init__(self):
        # dumb hack because global variables are weird
        self.shake_timer = 0
        self.shake_power = 0

    def shake(self, duration: float, power=3):
        self.shake_timer += duration
        self.shake_power = power
        print("shake")

    async def start(self):
        # pygame opengl setup

        pygame.init()
        screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("pygame asteroids")

        game_surf = pygame.surface.Surface(SIZE)

        base_color_fg = (0, 255, 0)
        base_color_bg = (7, 12, 4)

        # TODO write a system for this
        pressing_space = False

        pl = player.Player((500, 300), 30, self)
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
                    if ev.key == pygame.K_F4:
                        self.shake(3)
                    if ev.key == pygame.K_SPACE:
                        pressing_space = True
                    if menu is not None:
                        menu.pressed_key(ev.key, self)

                if ev.type == pygame.KEYUP:
                    if ev.key == pygame.K_SPACE:
                        pressing_space = False

            # apply screenshake if needed
            if self.shake_timer > 0:
                offset_x = random.randint(-self.shake_power, self.shake_power)
                offset_y = random.randint(-self.shake_power, self.shake_power)

                color_fg = meth.brighten_color(base_color_fg, 150)
                color_bg = meth.brighten_color(base_color_bg, 10)
                self.shake_timer -= delta
            else:
                self.shake_timer = 0
                color_fg = base_color_fg
                color_bg = base_color_bg
                offset_x = 0
                offset_y = 0

            game_surf.fill(color_bg)
            screen.fill(color_bg)

            # update player in game
            if menu is None:
                if pressing_space:
                    pl.accelerate(delta)
                # update
                spawner.update(pl, delta)
                pl.update(delta)
                pl.draw(game_surf, color_fg)

            bullet.update(delta)
            bullet.draw(game_surf, color_fg)

            asteroid.update(delta, self)
            asteroid.draw(game_surf, color_fg)

            particles.update(delta)
            particles.draw(game_surf, color_fg)

            if menu is None:
                gui_labels.render(game_surf, delta, color_fg)

            if menu is not None:
                menu.update(delta)
                menu.draw(game_surf, color_fg)
                if menu.menuAction == 0:  # start game
                    menu = None
                elif menu.menuAction == 2:  # quit game
                    keep_running = False
                    break

            screen.blit(game_surf, (offset_x, offset_y))

            pygame.display.update()
            clock.tick(FPS)
            await asyncio.sleep(0)

        pygame.quit()
        sys.exit(0)


if __name__ == '__main__':
    game = Game()
    asyncio.run(game.start())
