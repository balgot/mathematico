"""
This file defines the grid of the game Mathematico alongside with the move
generation and formatting of the text output of the grid.
"""
from typing import Tuple, Iterator, Dict
import numpy as np
from collections import defaultdict

from ._utils import rle
from .eval import evaluate_line, DIAGONAL_BONUS


EMPTY_CELL = 0


class Board:
    """
    The Board of the game is 5x5 grid with integer values representing the moves
    of players. We encode the moves as tuples (x, y) denoting the real position
    inside our array.

    Attributes
        - grid: 2D array, empty values are stored as Board.EMPTY_CELL
        - occupied_cells: number of occupied cells
        - size: size of the board

    Methods
        - integrity_check: returns True if the integrity holds
        - row(n): n-th row as a list
        - col(n): n-th column as a list
        - diag: main/anti diagonal as a list
        - row_rle(n): rle encoding of the n-th row
        - col_rle(n): rle encoding of the n-th column
        - diag_rle: rle encoding of the diagonal
        - **make_move**: updates a grid with the move
        - **unmake_move**: undos the specified move
        - **possible_moves**: iterates over all possible moves
        - **score**: score of the filled up board
    """

    def __init__(self, size: int = 5):
        self.grid: np.ndarray = np.full((size, size), EMPTY_CELL)
        self.rows_rle = [defaultdict(int) for _ in range(size)]
        self.cols_rle = [defaultdict(int) for _ in range(size)]
        self.main_diagonal_rle = defaultdict(int)
        self.anti_diagonal_rle = defaultdict(int)
        self.occupied_cells: int = 0

    @staticmethod
    def cell_to_str(cell: int) -> str:
        """Return string representation of a cell"""
        if cell == EMPTY_CELL:
            return "  "
        return f"{cell:2d}"

    def __str__(self) -> str:
        """
        Creates string representation of the grid. The result should resemble
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

        :return: string representation of the grid
        """
        long_line = "+--" * len(self.grid) + "+"
        result = [long_line]
        for row in self.grid:
            line = "|" + "|".join(map(self.cell_to_str, row)) + "|"
            result.append(line)
            result.append(long_line)
        return "\n".join(result)

    def is_empty(self, row: int, col: int) -> bool:
        """Return whether cell at (row, col) is empty."""
        return self.grid[row][col] == EMPTY_CELL

    def integrity_check(self) -> None:
        """
        Run the integrity check of the grid.

        Check consistency of the attributes, the grid is taken as the reference
        point.

        :raises RuntimeError: if data mismatch
        """
        non_empty = sum([x != EMPTY_CELL for x in self.grid.flatten()])
        if non_empty != self.occupied_cells:
            raise RuntimeError("Occupied cells mismatch")

        for row in range(len(self.grid)):
            if self.rows_rle[row] != rle(self.row(row), [EMPTY_CELL]):
                raise RuntimeError("Rle of row mismatch")
        for col in range(len(self.grid)):
            if self.cols_rle[col] != rle(self.col(col), [EMPTY_CELL]):
                raise RuntimeError("Rle of col mismatch")
        if self.main_diagonal_rle != rle(self.diag(True), [EMPTY_CELL]):
            raise RuntimeError("Rle of main diagonal mismatch")
        if self.anti_diagonal_rle != rle(self.diag(False), [EMPTY_CELL]):
            raise RuntimeError("Rle of anti diagonal mismatch")

    def row(self, n: int) -> np.ndarray:
        """Return n-th row."""
        return self.grid[n]

    def row_rle(self, n: int) -> Dict[int, int]:
        """Return RLE of n-th row."""
        return self.rows_rle[n]

    def col(self, n: int) -> np.ndarray:
        """Return n-th column."""
        return self.grid.T[n]

    def col_rle(self, n: int) -> Dict[int, int]:
        """Return RLE of n-th column."""
        return self.cols_rle[n]

    def diag(self, main_diagonal: bool = True) -> np.ndarray:
        """
        Returns main diagonal or main anti diagonal of the grid.

        :param main_diagonal: if True returns main diagonal, else anti diagonal
        :return: array with elements on the corresponding diagonal
        """
        if main_diagonal:
            return self.grid.diagonal()
        return np.flipud(self.grid).diagonal()

    def diag_rle(self, main_diagonal: bool = True) -> Dict[int, int]:
        """Return RLE of a diagonal.

        :param main_diagonal: if True, the main diagonal is returned
        :return: rle encoding of the main/anti-diagonal
        """
        if main_diagonal:
            return self.main_diagonal_rle
        return self.anti_diagonal_rle

    def at(self, row: int, col: int) -> int:
        """Return symbol at (row, col) or EMPTY_CELL"""
        return self.grid[row][col]

    def make_move(self, position: Tuple[int, int], move: int) -> None:
        """
        Play the move in the grid.

        :param position: tuple of row, column coordinates
        :param move: integer to be placed
        :return: None
        :raises ValueError: if the position is not empty
        """
        row, col = position
        if not self.is_empty(row, col):
            raise ValueError(f"The position {position} is invalid")

        self.grid[position] = move
        self.occupied_cells += 1

        self.rows_rle[row][move] += 1
        self.cols_rle[col][move] += 1
        if row == col:
            self.main_diagonal_rle[move] += 1
        if row + col + 1 == len(self.grid):
            self.anti_diagonal_rle[move] += 1

    def unmake_move(self, position: Tuple[int, int]) -> int:
        """Unmake the move played at given position.

        :param position:
        :return: the card on the specified position
        """
        row, col = position
        if self.is_empty(row, col):
            raise ValueError(f"Undoing empty square {position}")

        cell = self.grid[position]
        self.grid[position] = EMPTY_CELL
        self.occupied_cells -= 1

        self.rows_rle[row][cell] -= 1
        self.cols_rle[col][cell] -= 1
        if row == col:
            self.main_diagonal_rle[cell] -= 1
        if row + col + 1 == len(self.grid):
            self.anti_diagonal_rle[cell] -= 1
        return cell

    def possible_moves(self) -> Iterator[Tuple[int, int]]:
        """
        Returns a list of possible moves from given position encoded as tuples
        of row and column coordinates, the result can be directly passed to
        <make_move>.

        :return: iterator over possible moves
        """
        size = len(self.grid)
        for row in range(size):
            for col in range(size):
                if self.is_empty(row, col):
                    yield row, col

    @property
    def size(self) -> int:
        """Return size of the board."""
        return len(self.grid)

    def score(self, remove_zeros: bool = False) -> int:
        """Calculate and return the score for the FULL board."""
        if self.occupied_cells != self.size ** 2:
            raise ValueError(f"Board is not full - {self}")

        total_score = 0
        for i in range(self.size):
            total_score += evaluate_line(self.row_rle(i), remove_zeros)
            total_score += evaluate_line(self.col_rle(i), remove_zeros)

        for use_main_diag in [True, False]:
            diag_score = evaluate_line(self.diag_rle(use_main_diag), remove_zeros)
            if diag_score != 0:
                total_score += DIAGONAL_BONUS + diag_score

        return total_score
