import math
from operator import add, sub

from cell import Cell

class Player(Cell):
    def __init__(self, nick, pos, radius, color, border_color):
        super().__init__(pos, radius, color, border_color)
        # angle of speed in rad
        self._angle = 0
        # speed coeff [0, 1]
        self._speed = 0
        # max possible speed
        self._max_speed = 5
        # nickname
        self._nick = nick

    def move(self, angle, speed):
        self._update_velocity(angle, speed)
        # get cartesian vector
        vel = self._polar_to_cartesian(
            self._angle, 
            self._speed * self._max_speed)
        # change player position
        self._pos = list(map(add, self._pos, vel))

    def feed(self, cell):
        self._update_radius(cell.radius)

    def _update_velocity(self, angle, speed):
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

    def _update_radius(self, radius):
        new_area = self._circle_area(self._radius) + \
            self._circle_area(radius)
        self._radius = math.sqrt(new_area / math.pi)

    @classmethod
    def make_random(cls, nick, world_size):
        pos = cls._random_pos(world_size)
        radius = 20
        color = cls._random_color()
        border_color = cls._make_border_color(color)
        return cls(nick, pos, radius, color, border_color)

    @classmethod
    def is_collided(cls, first, second):
        if cls._distance(first.pos, second.pos) <= first.radius - second.radius:
            return True
        return False

    @classmethod
    def _polar_to_cartesian(cls, angle, val):
        return val * math.cos(angle), val * math.sin(angle)

    @classmethod
    def _circle_area(cls, radius):
        return math.pi * radius**2

    @classmethod
    def _distance(cls, pos1, pos2):
        diff = list(map(lambda x, y: abs(x - y), pos1, pos2))
        return math.sqrt(diff[0]**2 + diff[1]**2)

    @property
    def nick(self):
        return self._nick
    