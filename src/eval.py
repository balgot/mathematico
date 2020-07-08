"""
In this file we provide the definition of the evaluator class which can be used
to assign the resulting scores to the board.
"""
from .board import Board
from typing import Union, List, Any, Dict
import numpy as np


class Points:
    """
    Defines the bonuses and their values as written in the game rules.
    """
    DIAGONAL_BONUS = 10
    PAIR = 10
    TWO_PAIRS = 20
    THREE_OF_A_KIND = 40
    FOUR_OF_A_KIND = 160
    FOUR_ONES = 200
    FULL_HOUSE = 80
    FULL_HOUSE_1_13 = 100
    FLUSH = 50
    FLUSH_1_10_11_12_13 = 150


def rle(data: Union[List[Any], np.ndarray]) -> Dict[Any, int]:
    """
    Performs run length encoding on the data. Does not modify the original data.
    Expected time complexity: O(n).

    :param data: list of elements (in any order)
    :return: dictionary with keys being the elements of the data and values
        being the occurrences
    """
    result = {}
    for elem in data:
        if elem in result:
            result[elem] += 1
        else:
            result[elem] = 1
    return result


def evaluate_line(line: Union[List[Any], np.ndarray]) -> int:
    """
    Evaluates a single line of the board. The rules are applied according
    to the number of different values in the line. Throws an exception if
    unexpected values or their occurrences are present. Does not modify the
    original line.

    :param line: single line of the board (row, column or diagonal)
    :return: score of the line as described in the rules
    """
    code = rle(line)
    if len(code) == 5:
        # Of each value is different, the only combination can be flush,
        # either straight or <1, 10, 11, 12, 13>
        if all(x in code for x in [1, 10, 11, 12, 13]):
            return Points.FLUSH_1_10_11_12_13
        if max(line) - min(line) == 5 - 1:
            return Points.FLUSH
        return 0
    elif len(code) == 4:
        # The only combination with four different values is a single pair,
        # and so we do not need to check any other
        return Points.PAIR
    elif len(code) == 3:
        # To have three different values, either two and two values are
        # same, or three are same
        if any(x == 3 for x in code.values()):
            return Points.THREE_OF_A_KIND
        else:
            return Points.TWO_PAIRS
    elif len(code) == 2:
        # The only possibility here is FULL_HOUSE or four of a kind, both of
        # must be checked, and special case (four 1s) must be handled, same
        # for <1, 1, 1, 13, 13> combination
        for key, value in code.items():
            if value == 4:
                return Points.FOUR_ONES if key == 1 else Points.FOUR_OF_A_KIND
        if 1 in code and 13 in code and code[1] == 3:
            return Points.FULL_HOUSE_1_13
        return Points.FULL_HOUSE
    else:
        # Note that we can't have more different values than five (length
        # of the line) and less than two (max four numbers of a kind), thus
        # if we get here, there is a mistake
        raise ValueError(f"Unknown combination of values: {line}")


def evaluate(board: Board) -> int:
    """
    Calculates the score over the whole board.

    :param board: game plan
    :return: result score
    """
    if board.occupied_cells != Board.SIZE ** 2:
        raise ValueError("Board is not empty")
    total_score = 0
    for i in range(Board.SIZE):
        total_score += evaluate_line(board.row(i))
        total_score += evaluate_line(board.col(i))

    main_diagonal_score = evaluate_line(board.diagonal(True))
    if main_diagonal_score != 0:
        total_score += Points.DIAGONAL_BONUS + main_diagonal_score
    anti_diagonal_score = evaluate_line(board.diagonal(False))
    if anti_diagonal_score != 0:
        total_score += Points.DIAGONAL_BONUS + anti_diagonal_score
    return total_score
