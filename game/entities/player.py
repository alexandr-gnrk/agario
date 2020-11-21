import functools
import operator
import math

from .. import gameutils as gu
from . import interfaces
from .playercell import PlayerCell
from .circle import Circle


class Player(interfaces.Victim, interfaces.Killer):
    """Class that represents player game state."""

    START_SIZE = 40
    BORDER_WIDTH = 5

    LAST_ID = -1

    def __init__(self, nick, player_cell):
        self.id = self.new_id()
        self.nick = nick
        # cells of which player consists
        self.parts = [player_cell]
        # self.parts = [PlayerCell(pos, radius, color, border_color)]

    def move(self):
        """Move each part of player and check parts for collision."""
        for i, cell in enumerate(self.parts):
            cell.move()
            for another_cell in self.parts[i + 1:]:
                # cells shoud intersects and not be the same
                if cell == another_cell or \
                        not cell.is_intersects(another_cell):
                    continue

                # merge cells if their timeout is zero
                # otherwise get rid off colission between them
                if cell.split_timeout == 0 and \
                        another_cell.split_timeout == 0:
                    cell.eat(another_cell)
                    self.parts.remove(another_cell)
                else:
                    cell.regurgitate_from(another_cell)

    def update_velocity(self, angle, speed):
        """Update velocity of each part."""
        center_pos = self.center()
        for cell in self.parts:
            # get realtive velocity
            rel_vel = gu.velocity_relative_to_pos(
                center_pos,
                angle,
                speed,
                cell.pos)
            # update velocity of cell
            cell.update_velocity(*rel_vel)

    def shoot(self, angle):
        """Shoots with cells to given direction."""
        emmited = list()
        for cell in self.parts:
            if cell.able_to_shoot():
                emmited.append(cell.shoot(angle))

        return emmited

    def split(self, angle):
        new_parts = list()
        for cell in self.parts:
            if cell.able_to_split():
                new_parts.append(cell.split(angle))

        self.parts.extend(new_parts)
        return new_parts

    def center(self):
        """Returns median position of all player cells."""
        xsum = sum((cell.pos[0] for cell in self.parts))
        ysum = sum((cell.pos[1] for cell in self.parts))
        center = [
            xsum/len(self.parts),
            ysum/len(self.parts)]
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

    @classmethod
    def new_id(cls):
        cls.LAST_ID += 1
        return cls.LAST_ID

    def remove_part(self, cell):
        """Removes passed player cell from player parts list."""
        self.parts.remove(cell)

    def reset(self):
        self.parts = self.parts[:1]
        self.parts[0].area_pool = 0
        self.parts[0].radius = self.START_SIZE

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