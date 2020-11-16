from abc import ABC, abstractmethod


class Killer(ABC):
    """Interface of objects that could kill."""

    @abstractmethod
    def attempt_murder(self, victim):
        """Tries to kill passed victim. Retruns object
        that killed if attempt is successful, otherwise
        returns None. 
        """
        pass
        