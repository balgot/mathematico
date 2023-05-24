"""
In this file we provide the definition of the evaluator class which can be used
to assign the resulting scores to the grid.
"""
from typing import Dict


DIAGONAL_BONUS = 10
PAIR = 10
TWO_PAIRS = 20
THREE_OF_A_KIND = 40
FLUSH = 50
FULL_HOUSE = 80
FULL_HOUSE_1_13 = 100
FOUR_OF_A_KIND = 160
FLUSH_1_10_11_12_13 = 150
FOUR_ONES = 200


# Note: each method assumes the previous ones do not hold


def _has_four_ones(line_rle: Dict[int, int]) -> bool:
    return line_rle.get(1, 0) == 4


def _has_flush_1_10_11_12_13(line_rle: Dict[int, int]) -> bool:
    VALS = [1, 10, 11, 12, 13]
    return len(line_rle) == 5 and all(line_rle.get(x, 0) == 1 for x in VALS)


def _has_four_of_kind(line_rle: Dict[int, int]) -> bool:
    return 4 in line_rle.values()


def _has_full_house_1_13(line_rle: Dict[int, int]) -> bool:
    return line_rle.get(1, 0) == 3 and line_rle.get(13, 0) == 2


def _has_full_house(line_rle: Dict[int, int]) -> bool:
    return sum(line_rle.values()) == 5 and len(line_rle) == 2


def _has_flush(line_rle: Dict[int, int]) -> bool:
    return len(line_rle) == 5 and max(line_rle) - min(line_rle) == 4


def _has_three_of_kind(line_rle: Dict[int, int]) -> bool:
    return 3 in line_rle.values()


def _has_two_pairs(line_rle: Dict[int, int]) -> bool:
    return sum(v == 2 for v in line_rle.values()) == 2


def _has_pair(line_rle: Dict[int, int]) -> bool:
    return 2 in line_rle.values()


EVALS = [
    (FOUR_ONES, _has_four_ones),
    (FLUSH_1_10_11_12_13, _has_flush_1_10_11_12_13),
    (FOUR_OF_A_KIND, _has_four_of_kind),
    (FULL_HOUSE_1_13, _has_full_house_1_13),
    (FULL_HOUSE, _has_full_house),
    (FLUSH, _has_flush),
    (THREE_OF_A_KIND, _has_three_of_kind),
    (TWO_PAIRS, _has_two_pairs),
    (PAIR, _has_pair)
]


def evaluate_line(line_rle: Dict[int, int]) -> int:
    """
    Evaluates a single line of the grid. The rules are applied according
    to the number of different values in the line. Does not modify the
    original line.

    :param line_rle: rle of the line to evaluate
    :return: score of the line as described in the rules

    Note: removes 0 values from the dictionary.
    """
    items = line_rle.items()
    for k, v in items:
        if not v or not k:
            line_rle.pop(k)

    for points, scorer in EVALS:
        if scorer(line_rle):
            return points
    return 0
