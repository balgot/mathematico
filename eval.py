"""
In this file we provide the definition of the
evaluator class which can be used to assign the
resulting scores to the board
"""
from board import Board

from copy import deepcopy
from typing import Union


def rle(data: list):
    """
    Performs run length encoding
    :param data: sorted list
    :return: list with rle pair (number, count)
    """
    result = []
    current = data[0]
    count = 0
    for num in data:
        if num == current:
            count += 1
        else:
            result.append((current, count))
            count = 1
            current = num
    result.append((current, count))
    return result


class Evaluator:
    """
    In this class, the bonuses are defined as well as
    the points. Given the FULL Board (i.e. without empty
    cells), the Evaluator calculates the final score.
    """
    DIAGONAL_BONUS = 10
    TWO_OF_A_KIND = 10
    TWO_OF_A_KIND_TWICE = 20
    THREE_OF_A_KIND = 40
    FOUR_OF_A_KIND = 160  # excluding case 1 1 1 1
    FOUR_ONES = 200
    FULL_HOUSE = 80  # x, x, x, y, y
    FULL_HOUSE_1_1_1_13_13 = 100
    STRAIGHT_FLUSH = 50  # like 1 2 3 4 5
    FLUSH_1_10_11_12_13 = 150

    @staticmethod
    def evaluate_line(line: list):
        line.sort()
        code = rle(line)

        if len(code) == 5:
            # flush only or nothing
            if line == [1, 10, 11, 12, 13]:
                return Evaluator.FLUSH_1_10_11_12_13
            elif line[-1] - line[0] == 5 - 1:
                return Evaluator.STRAIGHT_FLUSH
            else:
                return 0
        elif len(code) == 4:
            # only double
            return Evaluator.TWO_OF_A_KIND
        elif len(code) == 3:
            # possible: TWO_OF_A_KIND_TWICE, THREE_OF_A_KIND
            if any(code[i][1] == 3 for i in range(3)):
                return Evaluator.THREE_OF_A_KIND
            else:
                return Evaluator.TWO_OF_A_KIND_TWICE
        elif len(code) == 2:
            # possible: FULL_HOUSE, FOUR_OF_A_KIND
            if code[0] == (1, 4):  # FOUR_ONES
                return Evaluator.FOUR_ONES
            elif line == [1, 1, 1, 13, 13]:  # FULL_HOUSE_1_1_1_13_13
                return Evaluator.FULL_HOUSE_1_1_1_13_13
            elif code[0][1] == 4 or code[1][1] == 4:  # FOUR_OF_A_KIND
                return Evaluator.FOUR_OF_A_KIND
            else:  # FULL_HOUSE left
                return Evaluator.FULL_HOUSE
        else:
            raise ValueError("Unknown input")

    @staticmethod
    def _evaluate_diagonals(board: list) -> int:
        """
        Calculates the score over two main diagonals
        :param board: game state
        :return: score of diagonals based on constants
        """
        score = 0
        main_diagonal = [board[i][i] for i in range(Board.SIZE)]
        anti_diagonal = [board[i][Board.SIZE - i - 1] for i in range(Board.SIZE)]

        main_diagonal_score = Evaluator.evaluate_line(main_diagonal)
        anti_diagonal_score = Evaluator.evaluate_line(anti_diagonal)

        if main_diagonal_score != 0:
            score += main_diagonal_score + Evaluator.DIAGONAL_BONUS
        if anti_diagonal_score != 0:
            score += anti_diagonal_score + Evaluator.DIAGONAL_BONUS
        return score

    @staticmethod
    def evaluate(board: Union[list, Board]) -> int:
        """
        Calculates the score over the whole board.
        :param board: game plan
        :return: result score
        """
        if isinstance(board, Board):
            board = board.get()
        if any(any(x is None for x in row) for row in board):
            raise ValueError("Board must not have empty cells")
        score = 0
        board_copy = deepcopy(board)
        for row in board_copy:
            score += Evaluator.evaluate_line(row)
        board_copy = list(map(list, zip(*board)))
        for col in board_copy:
            score += Evaluator.evaluate_line(col)
        score += Evaluator._evaluate_diagonals(board)

        return score
