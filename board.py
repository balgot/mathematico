"""
This file defines the board of the game Mathematico alongside with
the move-gen.
"""
from typing import Tuple, List


class Board:
    """
    The Board of the game is 5x5 grid with integer values representing
    the moves of players. We encode the moves as tuples (x, y) denoting
    the real position inside our array.
    """
    SIZE = 5

    def __init__(self):
        self._board = [[None for _ in range(self.SIZE)]
                       for _ in range(self.SIZE)]

    def __str__(self):
        """
        Creates string representation of the board. The result
        should resemble this formatting:
            +--+--+--+
            |13| 1| 3|
            +--+--+--+
            | 5| 1| 3|
            +--+--+--+
            |12|11| 3|
            +--+--+--+
        """
        long_line = "+--+--+--+--+--+\n"
        result = long_line
        for row in self._board:
            result += '|'
            for col in row:
                result += '  ' if col is None else f"{col:2d}"
                result += '|'
            result += '\n' + long_line
        return result

    def make_move(self, position: Tuple[int, int], move: int):
        """
        Plays the move in the board.
        :param position: tuple of row, col coordinates
        :param move: integer to be placed
        :return: return this object
        """
        row, col = position
        if self._board[row][col] is not None:
            raise ValueError(f"The position {(row, col)} is invalid")
        self._board[row][col] = move
        return self

    def possible_moves(self) -> List[Tuple[int, int]]:
        """
        Returns a list of possible moves from given position
        encoded as tuples to be passed to <make_move>
        :return: all possible moves
        """
        moves = []
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                if self._board[i][j] is None:
                    moves.append((i, j))
        return moves

    def get(self):
        """
        :return: the current board as 2D array
        """
        return self._board
