from abc import ABC, abstractmethod


class Victim(ABC):
    """Interface of objects that could be killed."""

    @abstractmethod
    def try_to_kill_by(self, killer):
        """Gets objects that tries to kill and returns
        None if killer couldn't kill otherwise return
        object that was killed.
        """ 
        pass
        