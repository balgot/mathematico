"""
This file defines the board of the game Mathematico alongside with the move
generation and formatting of the text output of the board.
"""
from typing import Tuple, Iterator
import numpy as np


class Board:
    """
    The Board of the game is 5x5 grid with integer values representing the moves
    of players. We encode the moves as tuples (x, y) denoting the real position
    inside our array.
    """
    SIZE = 5
    EMPTY = 0

    def __init__(self):
        self.board: np.ndarray = np.full((Board.SIZE, Board.SIZE), Board.EMPTY)
        """Store the board as 5x5 np.ndarray, empty values are Board.EMPTY"""
        self.occupied_cells: int = 0
        """Number of non-empty cells in the board"""

    def __str__(self):
        """
        Creates string representation of the board. The result should resemble
        this formatting:
                       +--+--+--+--+--+
                       |13|11|10| 1| 3|
                       +--+--+--+--+--+
                       | 5| 6| 1|  | 3|
                       +--+--+--+--+--+
                       | 8| 9| 7| 6| 3|
                       +--+--+--+--+--+
                       | 5|  | 4| 1|13|
                       +--+--+--+--+--+
                       | 1| 9| 2| 6| 3|
                       +--+--+--+--+--+

        :return: string representation of the board
        """
        long_line = "+--+--+--+--+--+\n"
        result = long_line
        for row in self.board:
            result += '|'
            for col in row:
                result += '  ' if col == Board.EMPTY else f"{col:2d}"
                result += '|'
            result += '\n' + long_line
        return result

    def row(self, n) -> np.ndarray:
        """
        Returns particular row as np.ndarray. Does not perform boundaries check.

        :param n: which row to return
        :return: n-th row of the board
        """
        return self.board[n]

    def col(self, n) -> np.ndarray:
        """
        Returns particular column as np.ndarray. Does not perform boundaries
        checking.

        :param n: which column to return
        :return: n-th column of the board
        """
        return self.board.T[n]

    def diagonal(self, main_diagonal: bool = True) -> np.ndarray:
        """
        Returns main diagonal or main anti diagonal of the board.

        :param main_diagonal: if True returns main diagonal, else anti diagonal
        :return: array with elements on the corresponding diagonal
        """
        if main_diagonal:
            return self.board.diagonal()
        else:
            return np.flipud(self.board).diagonal()

    def make_move(self, position: Tuple[int, int], move: int) -> None:
        """
        Plays the move in the board.

        :param position: tuple of row, column coordinates
        :param move: integer to be placed
        :return: None
        """
        if self.board[position] != Board.EMPTY:
            raise ValueError(f"The position {position} is invalid")
        self.board[position] = move
        self.occupied_cells += 1

    def possible_moves(self) -> Iterator[Tuple[int, int]]:
        """
        Returns a list of possible moves from given position encoded as tuples
        of row and column coordinates, the result can be directly passed to
        <make_move>.

        :return: list of empty positions on the board
        """
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.board[i][j] == Board.EMPTY:
                    yield i, j
