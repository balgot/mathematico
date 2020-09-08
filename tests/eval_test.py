from src.game import Points, evaluate, Board
from typing import List


def eval_list(array: List[List[int]]) -> int:
    """
    Simulates evaluation on the 2d list by creating board artificially.

    :param array: array of board to be evaluated
    :return: score of the board
    """
    board = Board()
    for row in range(Board.SIZE):
        for col in range(Board.SIZE):
            board.make_move((row, col), array[row][col])
    return evaluate(board)


def test_raises():
    board = Board()
    raised = False
    try:
        evaluate(board)
    except ValueError:
        raised = True
    assert raised


def test_evaluate_simple():
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 1],
        [2, 4, 6, 1, 3],
        [5, 2, 1, 3, 4],
        [1, 3, 5, 6, 2]
    ]
    assert eval_list(board) == Points.FLUSH


def test_evaluate():
    board = [
        [1, 10, 12, 13, 11],
        [1, 2, 2, 13, 13],
        [1, 2, 3, 4, 5],
        [7, 7, 7, 8, 8],
        [1, 2, 12, 4, 3]
    ]
    assert eval_list(board) == sum([
        Points.FLUSH_1_10_11_12_13,
        Points.TWO_PAIRS,
        Points.FLUSH,
        Points.FULL_HOUSE,
        0,
        Points.FOUR_ONES,
        Points.THREE_OF_A_KIND,
        Points.PAIR,
        Points.TWO_PAIRS,
        0,
        Points.PAIR + Points.DIAGONAL_BONUS,
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
    assert eval_list(board) == Points.PAIR

    # Two pairs
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 2, 4, 12],
        [2, 4, 6, 1, 3],
        [11, 2, 1, 3, 4],
        [1, 3, 5, 6, 2]
    ]
    assert eval_list(board) == Points.TWO_PAIRS

    # Three of a kind
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 12],
        [2, 4, 6, 1, 12],
        [11, 2, 1, 3, 4],
        [1, 3, 5, 6, 2]
    ]
    assert eval_list(board) == Points.THREE_OF_A_KIND

    # Full House
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 12],
        [2, 4, 6, 1, 12],
        [11, 2, 1, 3, 10],
        [1, 3, 5, 6, 10]
    ]
    assert eval_list(board) == Points.FULL_HOUSE

    # Four of a kind
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 12],
        [2, 4, 6, 1, 12],
        [11, 2, 1, 3, 12],
        [1, 3, 5, 6, 10]
    ]
    assert eval_list(board) == Points.FOUR_OF_A_KIND

    # Four ones
    board = [
        [8, 7, 2, 9, 1],
        [6, 5, 3, 4, 1],
        [2, 4, 6, 7, 1],
        [11, 2, 8, 3, 1],
        [9, 3, 5, 6, 10]
    ]
    assert eval_list(board) == Points.FOUR_ONES

    # Straight - from previous test
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 1],
        [2, 4, 6, 1, 3],
        [5, 2, 1, 3, 4],
        [1, 3, 5, 6, 2]
    ]
    assert eval_list(board) == Points.FLUSH

    # 1 1 1 13 13
    board = [
        [8, 7, 2, 5, 1],
        [6, 5, 3, 4, 1],
        [2, 4, 6, 1, 13],
        [5, 2, 1, 3, 13],
        [9, 3, 5, 6, 1]
    ]
    assert eval_list(board) == Points.FULL_HOUSE_1_13

    # 1 10 11 12 13
    board = [
        [8, 7, 2, 5, 1],
        [6, 5, 3, 4, 10],
        [2, 4, 6, 1, 13],
        [5, 2, 1, 3, 12],
        [9, 3, 5, 6, 11]
    ]
    assert eval_list(board) == Points.FLUSH_1_10_11_12_13
