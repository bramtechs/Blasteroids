import math
import pygame
import sys

BG = (0, 0, 0)
FG = (255, 255, 255)

FPS = 60

PL_ANGLE = 30


def asteroid_draw(screen, rect, samples):
    half_width = rect[2] / 2
    half_height = rect[3] / 2

    next_angle = 0
    for i in range(samples):
        x = half_width * math.cos(math.radians(next_angle))
        y = half_height * math.sin(math.radians(next_angle))

        pygame.draw.circle(screen, (0, 255, 255), (rect[0] + x, rect[1] + y), 3)

        next_angle += 360 / samples


def draw_cone(screen, pos, radius, rot):
    x = math.cos(math.radians(rot + 180 + PL_ANGLE)) * radius + pos[0]
    y = math.sin(math.radians(rot + 180 + PL_ANGLE)) * radius + pos[1]
    top_left = (x, y)

    x = math.cos(math.radians(rot + 180 - PL_ANGLE)) * radius + pos[0]
    y = math.sin(math.radians(rot + 180 - PL_ANGLE)) * radius + pos[1]
    bot_left = (x, y)

    x = math.cos(math.radians(rot + 180 + PL_ANGLE / 2)) * radius + pos[0]
    y = math.sin(math.radians(rot + 180 + PL_ANGLE / 2)) * radius + pos[1]
    top_left_inner = (x, y)

    x = math.cos(math.radians(rot + 180 - PL_ANGLE / 2)) * radius + pos[0]
    y = math.sin(math.radians(rot + 180 - PL_ANGLE / 2)) * radius + pos[1]
    bot_left_inner = (x, y)

    x = math.cos(math.radians(rot)) * radius + pos[0]
    y = math.sin(math.radians(rot)) * radius + pos[1]
    right = (x, y)

    pygame.draw.line(screen, FG, top_left, right)
    pygame.draw.line(screen, FG, bot_left, right)
    pygame.draw.line(screen, FG, top_left_inner, right)
    pygame.draw.line(screen, FG, bot_left_inner, right)
    pygame.draw.line(screen, FG, top_left, top_left_inner)
    pygame.draw.line(screen, FG, bot_left, bot_left_inner)
    pygame.draw.line(screen, FG, top_left_inner, bot_left_inner)
    pygame.draw.line(screen, FG, bot_left_inner, right)
    pygame.draw.line(screen, FG, top_left, bot_left)

    # pygame.draw.circle(screen, (255, 0, 0), player["pos"], 2)
    # pygame.draw.circle(screen, (200, 60, 60), player["pos"], player["size"], 1)


def degrees_between_points(src, target):
    delta_x = target[0] - src[0]
    delta_y = target[1] - src[1]
    return math.degrees(math.atan2(delta_y, delta_x))


def player_draw(screen, player):
    # point ship at mouse
    mouse_pos = pygame.mouse.get_pos()
    angle = degrees_between_points(player["pos"], mouse_pos)

    draw_cone(screen, player["pos"], player["size"], angle)


def start():
    pygame.init()
    size = width, height = 640, 480

    player = {
        "pos": (200, 200),
        "size": 30,
        "rot": 40
    }
    screen = pygame.display.set_mode(size)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        delta = 1 / FPS

        screen.fill(BG)
        player_draw(screen, player)
        asteroid_draw(screen, (150, 50, 300, 50), 30)
        pygame.display.flip()

        player["rot"] += delta * 20

        pygame.time.wait(int(1000 / FPS))


if __name__ == '__main__':
    start()
