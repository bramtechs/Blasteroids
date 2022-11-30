from pygame import mixer


def load(name):
    return mixer.Sound("sfx/{}.wav".format(name))


# OOP singleton abuse
# I really need to ditch OOP sometime
ins = None

# TODO thruster sound


class Audio:
    def __init__(self) -> None:
        global ins
        ins = self

        mixer.init()
        self.death = load("death")
        self.levelup = load("levelup")
        self.loexplosion = load("lowexplosion")
        self.explosion = load("asteroidexplosion")
        self.select = load("select")
        self.hit = load("hit")
        self.shoot = load("laserShoot")
        self.select = load("select")
        self.cursor = load("cursor")
