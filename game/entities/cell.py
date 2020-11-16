import random
from operator import add, sub

from .. import gameutils as gu
from . import interfaces
from .circle import Circle


class Cell(Circle, interfaces.Victim):
    """Represents cell(food) state."""

    BORDER_WIDTH=0
    FRICTION = 0.1
    MAX_SPEED = 5
    SIZES = (5, 7, 10)
    SIZES_CUM = (70, 20, 10)

    def __init__(self, pos, radius, color, angle=0, speed=0):
        super().__init__(pos, radius)
        # cell color [r, g, b]
        self.color = color
        # angle of speed in rad
        self.angle = angle
        # speed coeff from 0.0 to 1.0
        self.speed = speed

    def move(self):
        """Move accroding to stored velocity."""
        self.speed -= self.FRICTION
        if self.speed < 0:
            self.speed = 0
        # get cartesian vector
        diff_xy = gu.polar_to_cartesian(self.angle, self.speed*self.MAX_SPEED)
        # change position
        self.pos = list(map(add, self.pos, diff_xy))

    def update_velocity(self, angle, speed):
        """Add self velocity vector with passed velocity vector."""
        # convert to cartesian
        before_speed = self.speed
        v1 = gu.polar_to_cartesian(angle, speed)
        v2 = gu.polar_to_cartesian(self.angle, self.speed)
        # adding vectors
        v3 = list(map(add, v1, v2))
        # convert to polar
        self.angle, self.speed = gu.cartesian_to_polar(*v3)
        # normilize speed coeff
        if before_speed <= 1 and self.speed > 1:
            self.speed = 1
        elif before_speed > 1 and self.speed > before_speed:
            self.speed = before_speed

    def try_to_kill_by(self, killer):
        """Check is killer cell could eat current cell."""
        if 2*self.area() <= killer.area() and \
                self.distance_to(killer) <= killer.radius - self.radius:
            return self
        return None

    @classmethod
    def make_random(cls, bounds):
        """Creates random cell."""
        pos = gu.random_pos(bounds)
        radius = random.choices(cls.SIZES, cls.SIZES_CUM)[0]
        color = gu.random_safe_color()
        return cls(pos, radius, color)

    def __repr__(self):
        return '<{} pos={} radius={}>'.format(
            self.__class__.__name__,
            list(map(int, self.pos)),
            int(self.radius))