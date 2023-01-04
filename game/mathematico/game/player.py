from abc import abstractmethod, ABC
from .board import Board


class Player(ABC):
    """
    The interface for a generic player class, which should provide methods for
    interaction with the <game> class.
    """
    def __init__(self):
        self.board = Board()

    @abstractmethod
    def move(self, card_number: int) -> None:
        """Given the next number, places the number on the grid."""

    @abstractmethod
    def reset(self) -> None:
        """Resets the player to initial state at the beginning of the game."""

    def get_score(self) -> int:
        """Return score after the game is finished."""
        return self.board.score()
