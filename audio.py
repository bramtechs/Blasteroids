import pygame

# OOP singleton abuse
# I really need to ditch OOP sometime
ins = None

# TODO thruster sound

volume = 0.1


def is_playing():
    if volume == 0.1:
        return 1
    return 0


def mute(yes=True):
    global volume
    if yes:
        volume = 0
    else:
        volume = 0.1

    global ins

    for sound in ins.sounds:
        sound.set_volume(volume)


class Audio:
    def __init__(self) -> None:
        global ins
        ins = self

        pygame.mixer.init()

        self.sounds = []
        self.death = self.load("death")
        self.levelup = self.load("levelup")
        self.loexplosion = self.load("lowexplosion")
        self.explosion = self.load("asteroidexplosion")
        self.select = self.load("select")
        self.hit = self.load("hit")
        self.shoot = self.load("laserShoot")
        self.select = self.load("select")
        self.cursor = self.load("cursor")

    def load(self, name):
        snd = pygame.mixer.Sound("sfx/{}.wav".format(name))
        snd.set_volume(volume)
        self.sounds.append(snd)
        return snd
