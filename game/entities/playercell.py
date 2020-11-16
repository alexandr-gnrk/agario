import math
import enum 
from operator import add, sub

from .. import gameutils as gu
from . import interfaces
from .cell import Cell


class PlayerCell(Cell, interfaces.Killer):
    """Represents player cell(part of player) state."""

    BORDER_WIDTH = 5
    MAX_SPEED = 10
    # size of player when created
    SIZES = (5,)
    SIZES_CUM = (1,)

    # min ratius of cell to be able shoot
    SHOOTCELL_COND_RADIUS = 40
    SHOOTCELL_RADIUS = 10
    SHOOTCELL_SPEED = Cell.MAX_SPEED

    # min ratius of cell to be able split
    SPLITCELL_COND_RADIUS = 40
    SPLITCELL_SPEED = 3
    # the time that must pass before сell can connect to another cell
    SPLIT_TIMETOUT = 240

    def __init__(self, pos, radius, color, angle=0, speed=0):
        super().__init__(pos, radius, color, angle, speed)
        # time after which it will be possible to connect to another cell
        self.split_timeout = self.SPLIT_TIMETOUT
        # food storage, to make the radius change smooth
        self.area_pool = 0

    def move(self):
        """Update cell state and move by stored velocity."""
        self.__split_timeout_tick()
        self.__add_area(self.__area_pool_give_out())
        super().move()

    def eat(self, cell):
        """Increase current cell area with passed cell area,
        by changing cell area.
        """
        self.area_pool += cell.area()
        self.__add_area(self.__area_pool_give_out())

    def __split_timeout_tick(self):
        """Simply changes timeout value by one."""
        if self.split_timeout > 0:
            self.split_timeout -= 1

    def __add_area(self, area):
        """Increase current cell area with passed area."""
        self.radius = math.sqrt((super().area() + area) / math.pi)

    def __area_pool_give_out(self, part=0.05):
        """Returns some part of food from area pool."""
        if self.area_pool > 0:
            area = self.area_pool * part
            self.area_pool *= 1 - part
        else:
            area = 0
        return area

    def spit_out(self, cell):
        """Decrease current cell area with passed cell area,
        by changing cell area.
        """
        self.radius = math.sqrt((super().area() - cell.area()) / math.pi)

    def able_to_emit(self, cond_radius):
        """Checks if cell able to emmit."""
        if self.radius >= cond_radius:
            return True
        return False

    def emit(self, angle, speed, radius, ObjClass):
        """Emit cell with given angle and emit type.
        Returns emmited object.
        """
        # create emmited object at pos [0, 0]
        obj = ObjClass(
            [0, 0], radius, 
            self.color, 
            angle, speed)
        # change current cell radius
        self.spit_out(obj)
        # find diff_xy to move spawn cell on current circle border
        diff_xy = gu.polar_to_cartesian(angle, self.radius + radius)
        # move created object
        obj.pos = list(map(add, self.pos, diff_xy))
        return obj

    def attempt_murder(self, victim):
        """Try to kill passed victim cell by self cell."""
        return victim.try_to_kill_by(self)

    def shoot(self, angle):
        """Shoot in the given angle.
        Returns the fired cell.
        """
        return self.emit(
            angle, 
            self.SHOOTCELL_SPEED,
            self.SHOOTCELL_RADIUS,
            Cell)

    def able_to_shoot(self):
        """Checks is cell able to shoot."""
        return self.able_to_emit(self.SHOOTCELL_COND_RADIUS)

    def split(self, angle):
        """Spit cell in the given angle.
        Returns the splitted part.
        """
        return self.emit(
            angle, 
            self.SPLITCELL_SPEED,
            self.radius/math.sqrt(2),
            PlayerCell)

    def able_to_split(self):
        """Checks is cell able to split."""
        return self.able_to_emit(self.SPLITCELL_COND_RADIUS)

    def regurgitate_from(self, cell):
        """Pushing current cell to edge of the passed cell.
        It is necessary to get rid of the collision beetwen them.
        """
        # get vector that connects two centers, to detemine direction
        centers_vec = list(map(
            sub,
            self.pos,
            cell.pos))
        # get angle of contact
        angle = gu.cartesian_to_polar(*centers_vec)[0]
        # intersection length
        delta = self.radius + cell.radius - self.distance_to(cell)
        # get delta in cartesian coordinate system
        d_xy = gu.polar_to_cartesian(angle, delta)
        # move current cell outside passed cell
        self.pos = list(map(
            add,
            self.pos,
            d_xy))

    def area(self):
        """Returns full PlayerCell area, including area stored in pool."""
        return super().area() + self.area_pool
