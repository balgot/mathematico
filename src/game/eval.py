"""
In this file we provide the definition of the evaluator class which can be used
to assign the resulting scores to the board.
"""
from typing import Dict
from .board import Board


class Points:
    """
    Defines the bonuses and their values as written in the game rules.
    TODO: derive from Enum?
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


def evaluate_line(line_rle: Dict[int, int]) -> int:
    """
    Evaluates a single line of the board. The rules are applied according
    to the number of different values in the line. Does not modify the
    original line.

    :param line_rle: rle of the line to evaluate
    :return: score of the line as described in the rules
    """
    if len(line_rle) == 5:
        # TODO: https://stackoverflow.com/a/35329416 use map instead of dict
        # If each value is different, the only combination is be flush.
        if all(x in line_rle for x in [1, 10, 11, 12, 13]):
            return Points.FLUSH_1_10_11_12_13
        if max(line_rle.keys()) - min(line_rle.keys()) == 5 - 1:
            return Points.FLUSH
        return 0
    elif len(line_rle) == 4:
        # The only combination with four different values is a single pair,
        # and so we do not need to check any other
        return Points.PAIR
    elif len(line_rle) == 3:
        # To have three different values, either two and two values are
        # same, or three are same
        if any(x == 3 for x in line_rle.values()):
            return Points.THREE_OF_A_KIND
        else:
            return Points.TWO_PAIRS
    elif len(line_rle) == 2:
        # The only possibility here is FULL_HOUSE or four of a kind, both of
        # must be checked, and special case (four 1s) must be handled, same
        # for <1, 1, 1, 13, 13> combination
        for key, value in line_rle.items():
            if value == 4:
                return Points.FOUR_ONES if key == 1 else Points.FOUR_OF_A_KIND
        if 1 in line_rle and 13 in line_rle and line_rle[1] == 3:
            return Points.FULL_HOUSE_1_13
        return Points.FULL_HOUSE
    else:
        # Note that we can't have more different values than five (length
        # of the line) and less than two (max four numbers of a kind), thus
        # if we get here, there is a mistake
        raise ValueError(f"Unknown combination of values: {line_rle}")


def evaluate(board: Board) -> int:
    """
    Calculates the score over the whole board.

    :param board: game plan
    :return: result score
    """
    if board.occupied_cells != Board.SIZE ** 2:
        raise ValueError(f"Board is not full - {board}")

    total_score = 0
    for i in range(Board.SIZE):
        total_score += evaluate_line(board.row_rle(i))
        total_score += evaluate_line(board.col_rle(i))

    main_diagonal_score = evaluate_line(board.diag_rle(True))
    if main_diagonal_score != 0:
        total_score += Points.DIAGONAL_BONUS + main_diagonal_score
    anti_diagonal_score = evaluate_line(board.diag_rle(False))
    if anti_diagonal_score != 0:
        total_score += Points.DIAGONAL_BONUS + anti_diagonal_score
    return total_score
