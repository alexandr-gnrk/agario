import math
from operator import sub

from .. import gameutils as gu


class Circle():
    """Class that describes circle figure."""

    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius

    def distance_to(self, circle):
        """Returns distance to passed circle."""
        diff = tuple(map(sub, self.pos, circle.pos))
        return math.hypot(*diff)

    def is_intersects(self, circle):
        """Returns True if circles intersects, otherwise False."""
        if self.distance_to(circle) < self.radius + circle.radius:
            return True
        return False

    def area(self):
        """Return circle area."""
        return math.pi * self.radius**2