from mathematico.game import Player, Board


class HumanPlayer(Player):
    """
    Human player takes inputs from console after printing the
    board and the next move number
    """

    def reset(self) -> None:
        self.board = Board()

    def move(self, number: int):
        print(self.board)
        print(f"Next card:\t{number}")

        row, col = None, None
        moves = set(self.board.possible_moves())
        while (row, col) not in moves:
            row = int(input(f"Row number [0, {self.board.size}):\t"))
            col = int(input(f"Column number [0, {self.board.size}):\t"))
        assert row is not None and col is not None
        self.board.make_move((row, col), number)
