from mathematico.game import Player, Board
import random


class RandomPlayer(Player):
    """
    Random player plays moves randomly on empty positions.
    """

    def reset(self) -> None:
        self.board = Board()

    def move(self, number: int):
        possible_moves = list(self.board.possible_moves())
        if not possible_moves:
            raise IndexError("No moves available")
        picked_move = random.choice(possible_moves)
        self.board.make_move(picked_move, number)
