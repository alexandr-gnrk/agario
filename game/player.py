import functools
import operator
import math

from victim import Victim
from killer import Killer
from playercell import PlayerCell
# from gameutils import apply

class Player(Victim, Killer):
    """Class that represents player game state."""

    START_SIZE = 40
    BORDER_WIDTH = 5


    def __init__(self, nick, player_cell):
        self.nick = nick
        # cells of which player consists
        self.parts = [player_cell]
        # self.parts = [PlayerCell(pos, radius, color, border_color)]

    def move(self):
        """Move each part of player and check parts for collision."""
        for cell in self.parts:
            # check for collisison
            cell.move()

    def update_velocity(self, angle, speed):
        """Update velocity of each part."""
        for cell in self.parts:
            cell.update_velocity(angle, speed)

    def shoot(self, angle):
        """Shoots with cells to given direction."""
        emmited = list()
        for cell in self.parts:
            if cell.able_to_shoot():
                emmited.append(cell.shoot(angle))

        return emmited

    def center(self):
        """Returns center median position of all player cells."""
        pos_sum = functools.reduce(
            operator.add,
            (cell.pos for cell in self.parts))
        center = [
            pos_sum[0]/len(self.parts),
            pos_sum[1]/len(self.parts)]
        return center

    def score(self):
        """Returns player score.
        Score is radius of circle that consists of all parts area sum.
        """
        radius_sqr = functools.reduce(
            operator.add,
            (cell.radius**2 for cell in self.parts))
        return math.sqrt(radius_sqr)

    def attempt_murder(self, victim):
        """Try to kill passed victim by player parts. 
        Returns killed Cell if can, otherwise return None.
        """
        for cell in self.parts:
            killed_cell = victim.try_to_kill_by(cell)
            if killed_cell:
                # feed player cell with killed cell
                cell.eat(killed_cell)
                return killed_cell
        return None

    def try_to_kill_by(self, killer):
        """Check is killer cell could eat some of player parts.
        Returns killed player part or None.
        """
        for cell in self.parts:
            killed_cell = killer.attempt_murder(cell)
            if killed_cell:
                return killed_cell
        return None

    def remove_part(self, cell):
        """Removes passed player cell from player parts list."""
        self.parts.remove(cell)

    @classmethod
    def make_random(cls, nick, bounds):
        """Returns random player with given nick."""
        player_cell = PlayerCell.make_random(bounds)
        player_cell.radius = cls.START_SIZE
        return cls(nick, player_cell)

    def __repr__(self):
        return '<{} nick={} score={}>'.format(
            self.__class__.__name__,
            self.nick,
            int(self.score()))