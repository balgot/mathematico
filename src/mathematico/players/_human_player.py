from typing import Tuple
from mathematico.game import Player, Board


class HumanPlayer(Player):
    """
    Human player takes inputs from console after printing the
    board and the next move number
    """

    def reset(self) -> None:
        self.board = Board()

    def get_next_move(self, card: int) -> Tuple[int, int]:
        """Get next move and return (row, col)"""
        print(self.board)
        print(f"Next card:\t{card}")

        row, col = None, None
        moves = set(self.board.possible_moves())
        while (row, col) not in moves:
            row = int(input(f"Row number [0, {self.board.size}):\t"))
            col = int(input(f"Column number [0, {self.board.size}):\t"))
        return row, col

    def move(self, number: int):
        row, col = self.get_next_move(number)
        self.board.make_move((row, col), number)