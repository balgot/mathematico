"""
This file defines the board of the game Mathematico alongside with the move
generation and formatting of the text output of the board.
"""
from typing import Tuple, Iterator, Dict
import numpy as np


class Board:
    """
    The Board of the game is 5x5 grid with integer values representing the moves
    of players. We encode the moves as tuples (x, y) denoting the real position
    inside our array.

    Attributes
        - board: 2D array of the placed cards
        - occupied_cells: number of occupied cells

    Methods
        - integrity_check: returns True if the integrity holds
        - row(n): n-th row as a list
        - col(n): n-th column as a list
        - diag: main/anti diagonal as a list
        - row_rle(n): rle encoding of the n-th row
        - col_rle(n): rle encoding of the n-th column
        - diag_rle: rle encoding of the diagonal
        - **make_move**: updates a board with the move
        - **unmake_move**: undos the specified move
        - **possible_moves**: iterates over all possible moves
    """
    SIZE = 5
    EMPTY = 0

    def __init__(self):
        self.board: np.ndarray = np.full((Board.SIZE, Board.SIZE), Board.EMPTY)
        """Store the board as 5x5 np.ndarray, empty values are Board.EMPTY"""

        self.rows_rle = [dict() for _ in range(Board.SIZE)]
        self.cols_rle = [dict() for _ in range(Board.SIZE)]
        self.main_diagonal_rle = dict()
        self.anti_diagonal_rle = dict()

        self.occupied_cells: int = 0
        """Number of non-empty cells in the board"""

    def __str__(self) -> str:
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

    def integrity_check(self) -> Tuple[bool, str]:
        """
        :return: True if the integrity test passes
        """
        non_empty = len([x != Board.EMPTY for x in self.board.flatten()])
        if non_empty != self.occupied_cells:
            return False, "Occupied cells mismatch"
        from src.game import utils
        for row in range(self.SIZE):
            if self.rows_rle[row] != utils.rle(self.row(row)):
                return False, "Rle of row mismatch"
        for col in range(self.SIZE):
            if self.cols_rle[col] != utils.rle(self.col(col)):
                return False, "Rle of col mismatch"
        if self.main_diagonal_rle != utils.rle(self.diag(True)):
            return False, "Rle of main-diagonal mismatch"
        if self.anti_diagonal_rle != utils.rle(self.diag(False)):
            return False, "Rle of anti-diagonal mismatch"
        return True, ""

    def row(self, n) -> np.ndarray:
        """
        :param n: which row to return
        :return: n-th row of the board
        """
        return self.board[n]

    def row_rle(self, n: int) -> Dict[int, int]:
        """
        :param n: which row to return
        :return: rle of the n-th row
        """
        return self.rows_rle[n]

    def col(self, n: int) -> np.ndarray:
        """
        :param n: which column to return
        :return: n-th column of the board
        """
        return self.board.T[n]

    def col_rle(self, n: int) -> Dict[int, int]:
        """
        :param n: which column to return
        :return: n-th column's rle
        """
        return self.cols_rle[n]

    def diag(self, main_diagonal: bool = True) -> np.ndarray:
        """
        Returns main diagonal or main anti diagonal of the board.

        :param main_diagonal: if True returns main diagonal, else anti diagonal
        :return: array with elements on the corresponding diagonal
        """
        if main_diagonal:
            return self.board.diagonal()
        else:
            return np.flipud(self.board).diagonal()

    def diag_rle(self, main_diagonal: bool = True) -> Dict[int, int]:
        """TODO"""
        return self.main_diagonal_rle \
            if main_diagonal \
            else self.anti_diagonal_rle

    def make_move(self, position: Tuple[int, int], move: int) -> None:
        """
        Plays the move in the board.

        :param position: tuple of row, column coordinates
        :param move: integer to be placed
        :return: None
        :raises ValueError: if the position is not empty
        """
        if self.board[position] != Board.EMPTY:
            raise ValueError(f"The position {position} is invalid")
        self.board[position] = move
        self.occupied_cells += 1

        row, col = position
        self.rows_rle[row][move] = (self.rows_rle[row][move] or 0) + 1
        self.cols_rle[col][move] = (self.cols_rle[col][move] or 0) + 1
        if row == col:
            self.main_diagonal_rle[move] = \
                (self.main_diagonal_rle[move] or 0) + 1
        if row + col + 1 == Board.SIZE:
            self.anti_diagonal_rle[move] = \
                (self.anti_diagonal_rle[move] or 0) + 1

    def unmake_move(self, position: Tuple[int, int]) -> int:
        """

        :param position:
        :return: the card on the specified position
        """
        card = self.board[position]
        if card == Board.EMPTY:
            raise ValueError(f"Undoing empty square {position}")
        self.board[position] = Board.EMPTY
        self.occupied_cells -= 1
        row, col = position

        self.rows_rle[row][card] -= 1
        if self.rows_rle[row][card] == 0:
            self.rows_rle[row].pop(card)
        self.cols_rle[col][card] -= 1
        if self.cols_rle[col][card] == 0:
            self.cols_rle[col].pop(card)
        if row == col:
            self.main_diagonal_rle[card] -= 1
            if self.main_diagonal_rle[card] == 0:
                self.main_diagonal_rle.pop(card)
        if row + col + 1 == Board.SIZE:
            self.anti_diagonal_rle[card] -= 1
            if self.anti_diagonal_rle[card] == 0:
                self.anti_diagonal_rle.pop(card)
        return card

    def possible_moves(self) -> Iterator[Tuple[int, int]]:
        """
        Returns a list of possible moves from given position encoded as tuples
        of row and column coordinates, the result can be directly passed to
        <make_move>.

        :return: iterator over possible moves
        """
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.board[i][j] == Board.EMPTY:
                    yield i, j
