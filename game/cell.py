import random

class Cell():
    BORDER_WIDTH = 5
    def __init__(self, pos, radius, color, border_color=None):
        # x, y position
        self._pos = pos
        # radius (a.k.a mass)
        self._radius = radius
        # rgb color
        self._color = color
        self._border_color = border_color if border_color else self._color

    @classmethod
    def make_random(cls, world_size):
        pos = cls._random_pos(world_size)
        radius = random.choices((5, 7, 10), (70, 20, 10))[0]
        color = cls._random_color()
        border_color = None
        # border_color = cls._make_border_color(color)
        return cls(pos, radius, color, border_color)

    @classmethod
    def _random_color(cls):
        # set two random fields with 7 and 255
        # last field set [0 - 255]
        lights = (7, 255, random.randint(0, 255))
        return random.sample(lights, 3)

    @classmethod
    def _random_pos(cls, world_size):
        return (random.randint(-world_size, world_size), 
            random.randint(-world_size, world_size))

    @classmethod
    def _make_border_color(self, color):
        # makes border color by passed color
        # 255 -> 229, 7 -> 6, other -> 0.9*other
        mapper = lambda l: 229 if (l == 255) else 6 if (l == 6) else 0.9*l
        return list(map(mapper, color))

    @property
    def pos(self):
        return self._pos

    @property
    def radius(self):
        return self._radius
    
    @property
    def color(self):
        return self._color

    @property
    def border_color(self):
        return self._border_color    