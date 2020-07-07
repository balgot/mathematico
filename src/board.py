"""
This file defines the board of the game Mathematico alongside with the move
generation and formatting of the text output of the board.
"""
from typing import Tuple, List, Union


class Board:
    """
    The Board of the game is 5x5 grid with integer values representing the moves
    of players. We encode the moves as tuples (x, y) denoting the real position
    inside our array.
    """
    SIZE = 5

    def __init__(self):
        self._board: List[List[Union[int, None]]] = [
            [None for _ in range(self.SIZE)] for _ in range(self.SIZE)
        ]
        self.occupied_cells = 0

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

        :param position: tuple of row, column coordinates
        :param move: integer to be placed
        :return: returns this object
        """
        row, col = position
        if self._board[row][col] is not None:
            raise ValueError(f"The position {(row, col)} is invalid")
        self._board[row][col] = move
        self.occupied_cells += 1
        return self

    def possible_moves(self) -> List[Tuple[int, int]]:
        """
        Returns a list of possible moves from given position encoded as tuples
        of row and column coordinates, the result can be directly passed to
        <make_move>.

        :return: list of empty positions on the board
        """
        moves = []
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self._board[i][j] is None:
                    moves.append((i, j))
        return moves

    def get(self) -> List[List[Union[int, None]]]:
        """
        Provides the access to the board representation in form of the 2D array.

        :return: the current board as 2D array
        """
        return self._board
