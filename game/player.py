import functools
import operator
import math

from victim import Victim
from killer import Killer
from playercell import PlayerCell
import gameutils as gu

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
            cell.move()
            for another_cell in self.parts:
                if cell != another_cell and cell.is_intersects(another_cell):
                    centers_vec = list(map(
                        operator.sub,
                        cell.pos,
                        another_cell.pos))
                    angle = gu.cartesian_to_polar(*centers_vec)[0]
                    delta = cell.radius + another_cell.radius - cell.distance_to(another_cell)
                    d_xy = gu.polar_to_cartesian(angle, delta)
                    cell.pos = list(map(
                        operator.add,
                        cell.pos,
                        d_xy))
                    # corr_vec = list(map(
                    #     operator.add,
                    #     gu.polar_to_cartesian(cell.angle, cell.speed),
                    #     gu.polar_to_cartesian(another_cell.angle, another_cell.speed)))
                    # corr_vec = gu.cartesian_to_polar(*corr_vec)
                    # corr_vec[1] *= cell.MAX_SPEED
                    # corr_vec = gu.polar_to_cartesian(*corr_vec)
                    # print("corr", gu.cartesian_to_polar(*corr_vec)[::-1])
                    # cell.pos = list(map(
                    #     operator.add,
                    #     cell.pos,
                    #     corr_vec))


                            

    # def update_velocity(self, angle, speed):
    #     """Update velocity of each part."""
    #     core_cell = self.biggest_part()
    #     core_cell.update_velocity(angle, speed)
    #     for cell in self.parts:
    #         if cell != core_cell:
    #             # get realtive velocity
    #             # cell.update_velocity(angle, speed)
    #             rel_angle, rel_speed = core_cell.velocity_relative_to(cell)
    #             # print(gu.polar_to_cartesian(rel_angle, rel_speed))
    #             print(rel_angle, rel_speed)
    #             cell.update_velocity(rel_angle, rel_speed)
    #             # cell.angle = rel_angle
    #             # cell.speed = rel_speed

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
        """Returns center median position of all player cells."""
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

    def biggest_part(self):
        return max(self.parts, key=lambda x: x.radius)

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