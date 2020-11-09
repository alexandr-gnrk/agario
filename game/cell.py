import random
import math

from operator import add

class Cell():
    """Represents cell(food) state."""

    BORDER_WIDTH = 5
    FRICTION = 0.02
    MAX_SPEED = 10

    def __init__(self, pos, radius, color, border_color=None):
        # x, y position
        self._pos = pos
        # angle of speed in rad
        self._angle = 0
        # speed coeff [0, 1]
        self._speed = 0
        # radius(mass)
        self._radius = radius
        # rgb color
        self._color = color
        self._border_color = border_color if border_color else self._color

    def move(self):
        """Move according stored velocity."""
        # simulate friction
        self._speed -= 0.02
        if self._speed < 0:
            self._speed = 0
        # get cartesian vector
        vel = self._polar_to_cartesian(
            self._angle, 
            self._speed * self.MAX_SPEED)
        # change position
        self._pos = list(map(add, self._pos, vel))

    def update_velocity(self, angle=0, speed=0):
        """Set velocity as sum of self speed vector 
        and passed vector.
        """
        # convert to cartesian
        v1 = self._polar_to_cartesian(angle, speed)
        v2 = self._polar_to_cartesian(self._angle, self._speed)
        # adding vectors
        v3 = list(map(add, v1, v2))
        # convert to polar
        self._speed = math.sqrt(v3[0]**2 + v3[1]**2)
        self._angle = math.atan2(v3[1], v3[0])
        # normilize speed coeff
        if self._speed > 1:
            self._speed = 1

    @classmethod
    def make_random(cls, world_size):
        """Returns random cell."""
        pos = cls._random_pos(world_size)
        radius = random.choices((5, 7, 10), (70, 20, 10))[0]
        color = cls._random_color()
        border_color = None
        # border_color = cls._make_border_color(color)
        return cls(pos, radius, color, border_color)

    @classmethod
    def _random_color(cls):
        """Returns random safe color.

        Two random values of three RGB is 7 and 255
        and last is in range [0 - 255]
        """
        lights = (7, 255, random.randint(0, 255))
        return random.sample(lights, 3)

    @classmethod
    def _random_pos(cls, world_size):
        """Returns random pos in within game field."""
        return (random.randint(-world_size, world_size), 
            random.randint(-world_size, world_size))

    @classmethod
    def _make_border_color(self, color):
        """Creates border color from passed color.

        Simply maps 255 to 229 and 7 to 6.
        Third light is multiply by 0.9
        (255 -> 229, 7 -> 6, other -> 0.9*other)
        """
        mapper = lambda l: 229 if (l == 255) else 6 if (l == 7) else 0.9*l
        return list(map(mapper, color))

    @classmethod
    def _circle_area(cls, radius):
        """Returns area of circle."""
        return math.pi * radius**2

    @classmethod
    def _polar_to_cartesian(cls, angle, val):
        """Converts polar vector to cartesian pos."""
        return val * math.cos(angle), val * math.sin(angle)

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

    @property
    def area(self):
        return self._circle_area(self._radius)

    def __str__(self):
        return '<{} pos={} radius={}>'.format(
            self.__class__.__name__,
            list(map(int, self._pos)),
            int(self._radius))

    def __repr__(self):
        return '<{} pos={} radius={} color={}>'.format(
            self.__class__.__name__,
            list(map(int, self._pos)),
            int(self._radius),
            self._color)
