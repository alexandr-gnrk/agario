import math
import enum 
from operator import add

# from victim import Victim
from killer import Killer
from cell import Cell
import gameutils as gu

class PlayerCell(Cell, Killer):
    """Represents player cell(part of player) state."""

    BORDER_WIDTH = 5
    MAX_SPEED = 10
    SIZES = (5,)
    SIZES_CUM = (1,)
    SHOOTCELL_COND_RADIUS = 40
    SHOOTCELL_RADIUS = 10
    SHOOTCELL_SPEED = Cell.MAX_SPEED

    SPLITCELL_COND_RADIUS = 40
    SPLITCELL_SPEED = MAX_SPEED
    # SHOOT_MIN_RADIUS = 40

    def __init__(self, pos, radius, color, angle=0, speed=0):
        super().__init__(pos, radius, color, angle, speed)
    
    # def can_eat(self, cell):
    #     """Checks if current cell could eat passed cell."""
    #     
    def eat(self, cell):
        """Increase current cell area with passed cell area,
        by changing cell area."""
        self.radius = math.sqrt((self.area() + cell.area()) / math.pi)

    def spit_out(self, cell):
        """Decrease current cell area with passed cell area,
        by changing cell area."""
        self.radius = math.sqrt((self.area() - cell.area()) / math.pi)

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
        return self.emit(
            angle, 
            self.SHOOTCELL_SPEED,
            self.SHOOTCELL_RADIUS,
            Cell)

    def able_to_shoot(self):
        return self.able_to_emit(self.SHOOTCELL_COND_RADIUS)

    def split(self, angle):
        return self.emit(
            angle, 
            self.SPLITCELL_SPEED,
            self.radius/math.sqrt(2),
            PlayerCell)

    def able_to_split(self):
        return self.able_to_emit(self.SPLITCELL_COND_RADIUS)

