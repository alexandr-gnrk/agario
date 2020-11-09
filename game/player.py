import math
from operator import add

from cell import Cell


class Player(Cell):
    """Class that represents player game state."""

    MAX_SPEED = 5
    SHOOTCELL_RADIUS = 10

    def __init__(self, nick, pos, radius, color, border_color):
        super().__init__(pos, radius, color, border_color)
        # nickname
        self._nick = nick

    def feed(self, cell):
        """Increase player radius with passed cell."""
        self._update_radius(cell.radius)

    def shoot(self, angle):
        """Shoots with cell to given direction."""
        cell_radius = self.SHOOTCELL_RADIUS
        cell_speed = Cell.MAX_SPEED
        self._update_radius(cell_radius, sub=True)
        # find delta to move spawn cell outside player circle
        delta = self._radius*math.cos(angle), self._radius*math.sin(angle)
        # delta = 50, 50
        cell_pos = list(map(add, self._pos, delta))
        # spawn cell
        cell = Cell(cell_pos, cell_radius, self.color)
        cell.update_velocity(angle, cell_speed)
        return cell

    def able_to_shoot(self):
        """Checks if player able to shoot."""
        if self._radius > 40:
            return True
        return False

    def _update_radius(self, radius, sub=False):
        """Update according to eaten or loosed circle radius."""
        new_area = self._circle_area(self._radius)
        if not sub:
            new_area += self._circle_area(radius)
        else:
            new_area -= self._circle_area(radius)
        self._radius = math.sqrt(new_area / math.pi)

    @classmethod
    def make_random(cls, nick, world_size):
        """Returns random player."""
        pos = cls._random_pos(world_size)
        radius = 20
        color = cls._random_color()
        border_color = cls._make_border_color(color)
        return cls(nick, pos, radius, color, border_color)

    @classmethod
    def is_collided(cls, first, second):
        """Check is there a colision between first and second objects."""
        if first.area >= 2*second.area and \
            cls._distance(first.pos, second.pos) <= first.radius - second.radius:
            return True
        return False


    @classmethod
    def _distance(cls, pos1, pos2):
        """Returns distance between two dots."""
        diff = list(map(lambda x, y: abs(x - y), pos1, pos2))
        return math.sqrt(diff[0]**2 + diff[1]**2)

    @property
    def nick(self):
        return self._nick

    def __str__(self):
        return '<{} nick={} pos={} radius={}>'.format(
            self.__class__.__name__,
            self._nick,
            list(map(int, self._pos)),
            int(self._radius))

    def __repr__(self):
        return '<{} nick={} pos={} radius={} color={}>'.format(
            self.__class__.__name__,
            self._nick,
            list(map(int, self._pos)),
            int(self._radius),
            self._color)
    