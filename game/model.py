
from cell import Cell
from player import Player

class Model():
    """Class that represents game state."""

    def __init__(self, player, world_size=1000):
        # means that size of world is [-world_size, world_size] 
        self._world_size = world_size
        self._player = player
        # self._players = players.append(player)
        self._cells = list()

    def move(self, angle, speed):
        """Make player movement.""" 
        self.player.move(angle, speed)
        for cell in self._cells:
            if Player.is_collided(self._player, cell):
                self._player.feed(cell)
                self._cells.remove(cell)

    def spawn_cells(self, amount):
        """Spawn passed amount of cells on the field."""
        for _ in range(amount):
            self._cells.append(Cell.make_random(self.world_size))

    @property
    def world_size(self):
        return self._world_size

    @property
    def player(self):
        return self._player

    @property
    def cells(self):
        return self._cells
    