from typing import List

from mathematico.game import Board
from mathematico.game.eval import FLUSH, FULL_HOUSE, FLUSH_1_10_11_12_13, \
    TWO_PAIRS, FOUR_ONES, THREE_OF_A_KIND, PAIR, DIAGONAL_BONUS, \
    FULL_HOUSE_1_13, FOUR_OF_A_KIND


def eval_list(array: List[List[int]]) -> int:
    """
    Simulates evaluation on the 2d list by creating grid artificially.

    :param array: array of grid to be evaluated
    :return: score of the grid
    """
    board = Board()
    for row in range(board.size):
        for col in range(board.size):
            board.make_move((row, col), array[row][col])
    return board.score()


def test_empty_board():
    """Empty board can be scored, and as there is no combination, returns 0."""
    board = Board()
    assert board.score() == 0


def test_evaluate_simple():
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 1],
        [2, 4, 6, 1, 3],
        [5, 2, 1, 3, 4],
        [1, 3, 5, 6, 2]
    ]
    assert eval_list(board) == FLUSH


def test_evaluate():
    board = [
        [1, 10, 12, 13, 11],
        [1, 2, 2, 13, 13],
        [1, 2, 3, 4, 5],
        [7, 7, 7, 8, 8],
        [1, 2, 12, 4, 3]
    ]
    assert eval_list(board) == sum([
        FLUSH_1_10_11_12_13,
        TWO_PAIRS,
        FLUSH,
        FULL_HOUSE,
        0,
        FOUR_ONES,
        THREE_OF_A_KIND,
        PAIR,
        TWO_PAIRS,
        0,
        PAIR + DIAGONAL_BONUS,
        0
    ])


def test_evaluate_all_combinations():
    # A pair
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 12],
        [2, 4, 6, 1, 3],
        [11, 2, 1, 3, 4],
        [1, 3, 5, 6, 2]
    ]
    assert eval_list(board) == PAIR

    # Two pairs
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 2, 4, 12],
        [2, 4, 6, 1, 3],
        [11, 2, 1, 3, 4],
        [1, 3, 5, 6, 2]
    ]
    assert eval_list(board) == TWO_PAIRS

    # Three of a kind
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 12],
        [2, 4, 6, 1, 12],
        [11, 2, 1, 3, 4],
        [1, 3, 5, 6, 2]
    ]
    assert eval_list(board) == THREE_OF_A_KIND

    # Full House
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 12],
        [2, 4, 6, 1, 12],
        [11, 2, 1, 3, 10],
        [1, 3, 5, 6, 10]
    ]
    assert eval_list(board) == FULL_HOUSE

    # Four of a kind
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 12],
        [2, 4, 6, 1, 12],
        [11, 2, 1, 3, 12],
        [1, 3, 5, 6, 10]
    ]
    assert eval_list(board) == FOUR_OF_A_KIND

    # Four ones
    board = [
        [8, 7, 2, 9, 1],
        [6, 5, 3, 4, 1],
        [2, 4, 6, 7, 1],
        [11, 2, 8, 3, 1],
        [9, 3, 5, 6, 10]
    ]
    assert eval_list(board) == FOUR_ONES

    # Straight - from previous test
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 1],
        [2, 4, 6, 1, 3],
        [5, 2, 1, 3, 4],
        [1, 3, 5, 6, 2]
    ]
    assert eval_list(board) == FLUSH

    # 1 1 1 13 13
    board = [
        [8, 7, 2, 5, 1],
        [6, 5, 3, 4, 1],
        [2, 4, 6, 1, 13],
        [5, 2, 1, 3, 13],
        [9, 3, 5, 6, 1]
    ]
    assert eval_list(board) == FULL_HOUSE_1_13

    # 1 10 11 12 13
    board = [
        [8, 7, 2, 5, 1],
        [6, 5, 3, 4, 10],
        [2, 4, 6, 1, 13],
        [5, 2, 1, 3, 12],
        [9, 3, 5, 6, 11]
    ]
    assert eval_list(board) == FLUSH_1_10_11_12_13
