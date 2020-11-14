from loguru import logger

from cell import Cell
from player import Player

class Model():
    """Class that represents game state."""

    def __init__(self, players, bounds=(1000, 1000)):
        # means that size of world is [-world_size, world_size] 
        self.bounds = bounds
        self.players = players
        self.cells = list()

    def update_velocity(self, player, angle, speed):
        """Update passed player velocity."""
        player.update_velocity(angle, speed)

    def shoot(self, player, angle):
        """Shoots into given direction."""
        emitted_cells = player.shoot(angle)
        self.cells.extend(emitted_cells)
        if emitted_cells:
            logger.debug(f'{player} shot')
        else:
            logger.debug(f'{player} tried to shoot, but he can\'t')

    def split(self, player, angle):
        """Splits player."""
        new_parts = player.split(angle)
        if new_parts:
            logger.debug(f'{player} splitted')
        else:
            logger.debug(f'{player} tried to split, but he can\'t')

    def update(self):
        """Updates game state."""
        # update cells
        for cell in self.cells:
            cell.move()
        # update players
        for player in self.players:
            player.move()

            for cell in self.cells:
                killed_cell = player.attempt_murder(cell)
                if killed_cell:
                    logger.debug(f'{player} ate {killed_cell}')
                    self.cells.remove(killed_cell)

            for another_player in self.players:
                if player == another_player:
                    continue
                killed_cell = player.attempt_murder(another_player)
                if killed_cell:
                    if len(another_player.parts) == 1:
                        logger.debug(f'{player} ate {another_player}')
                        another_player.remove_part(killed_cell)
                        self.players.remove(another_player)
                    else:
                        logger.debug(f'{player} ate {another_player} part {killed_cell}')

    def spawn_cells(self, amount):
        """Spawn passed amount of cells on the field."""
        for _ in range(amount):
            self.cells.append(Cell.make_random(self.bounds))
    