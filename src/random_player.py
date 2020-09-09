from .game import Player, Board
import random as rnd


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.board: Board = Board()
        self.seed = seed

    def get_board(self) -> Board:
        return self.board

    def move(self, card_number: int) -> None:
        possible_moves = list(self.board.possible_moves())
        if not possible_moves:
            raise IndexError("No more moves possible")
        picked_move = rnd.Random(self.seed).choice(possible_moves)
        return picked_move
