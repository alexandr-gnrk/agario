from loguru import logger

from cell import Cell
from player import Player

class Model():
    """Class that represents game state."""

    def __init__(self, players, world_size=1000):
        # means that size of world is [-world_size, world_size] 
        self._world_size = world_size
        self._players = players
        self._cells = list()

    def update_velocity(self, player, angle, speed):
        """Update passed player velocity."""
        player.update_velocity(angle, speed)

    def shoot(self, player, angle):
        """Shoots into given direction."""
        if player.able_to_shoot():
            cell = player.shoot(angle)
            self._cells.append(cell)
            logger.debug(f'{player} shot')
        else:
            logger.debug(f'{player} tried to shoot, but he can\'t')

    def update(self):
        """Update game state."""
        # update cells
        for cell in self._cells:
            cell.move()
        # update players
        for player in self._players:
            player.move()
            for obj in self.objects:
                if Player.is_collided(player, obj):
                    logger.info(f'{player} ate {obj}')
                    player.feed(obj)
                    if isinstance(obj, Player):
                        self._players.remove(obj)
                    else:
                        self._cells.remove(obj)

    def spawn_cells(self, amount):
        """Spawn passed amount of cells on the field."""
        for _ in range(amount):
            self._cells.append(Cell.make_random(self.world_size))

    @property
    def world_size(self):
        return self._world_size

    @property
    def players(self):
        return self._players

    @property
    def cells(self):
        return self._cells

    @property
    def objects(self):
        return self._cells + self._players
    