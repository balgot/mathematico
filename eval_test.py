from eval import Evaluator


def test_raises():
    board = [[None] * 5] * 5
    raised = False
    try:
        Evaluator.evaluate(board)
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
    assert Evaluator.evaluate(board) == Evaluator.FLUSH


def test_evaluate():
    board = [
        [1, 10, 12, 13, 11],
        [1, 2, 2, 13, 13],
        [1, 2, 3, 4, 5],
        [7, 7, 7, 8, 8],
        [1, 2, 12, 4, 3]
    ]
    assert Evaluator.evaluate(board) == sum([
        Evaluator.FLUSH_1_10_11_12_13,
        Evaluator.TWO_PAIRS,
        Evaluator.FLUSH,
        Evaluator.FULL_HOUSE,
        0,
        Evaluator.FOUR_ONES,
        Evaluator.THREE_OF_A_KIND,
        Evaluator.PAIR,
        Evaluator.TWO_PAIRS,
        0,
        Evaluator.PAIR + Evaluator.DIAGONAL_BONUS,
        0
    ])


def test_evaluate_does_not_change_board():
    from copy import deepcopy
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 1],
        [2, 4, 6, 1, 3],
        [5, 2, 1, 3, 4],
        [1, 3, 5, 6, 2]
    ]
    board_copy = deepcopy(board)
    _ = Evaluator.evaluate(board)
    assert board_copy == board


def test_evaluate_all_combinations():
    # A pair
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 12],
        [2, 4, 6, 1, 3],
        [11, 2, 1, 3, 4],
        [1, 3, 5, 6, 2]
    ]
    assert Evaluator.evaluate(board) == Evaluator.PAIR

    # Two pairs
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 2, 4, 12],
        [2, 4, 6, 1, 3],
        [11, 2, 1, 3, 4],
        [1, 3, 5, 6, 2]
    ]
    assert Evaluator.evaluate(board) == Evaluator.TWO_PAIRS

    # Three of a kind
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 12],
        [2, 4, 6, 1, 12],
        [11, 2, 1, 3, 4],
        [1, 3, 5, 6, 2]
    ]
    assert Evaluator.evaluate(board) == Evaluator.THREE_OF_A_KIND

    # Full House
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 12],
        [2, 4, 6, 1, 12],
        [11, 2, 1, 3, 10],
        [1, 3, 5, 6, 10]
    ]
    assert Evaluator.evaluate(board) == Evaluator.FULL_HOUSE

    # Four of a kind
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 12],
        [2, 4, 6, 1, 12],
        [11, 2, 1, 3, 12],
        [1, 3, 5, 6, 10]
    ]
    assert Evaluator.evaluate(board) == Evaluator.FOUR_OF_A_KIND

    # Four ones
    board = [
        [8, 7, 2, 9, 1],
        [6, 5, 3, 4, 1],
        [2, 4, 6, 7, 1],
        [11, 2, 8, 3, 1],
        [9, 3, 5, 6, 10]
    ]
    assert Evaluator.evaluate(board) == Evaluator.FOUR_ONES

    # Straight - from previous test
    board = [
        [8, 7, 2, 5, 12],
        [6, 5, 3, 4, 1],
        [2, 4, 6, 1, 3],
        [5, 2, 1, 3, 4],
        [1, 3, 5, 6, 2]
    ]
    assert Evaluator.evaluate(board) == Evaluator.FLUSH

    # 1 1 1 13 13
    board = [
        [8, 7, 2, 5, 1],
        [6, 5, 3, 4, 1],
        [2, 4, 6, 1, 13],
        [5, 2, 1, 3, 13],
        [9, 3, 5, 6, 1]
    ]
    assert Evaluator.evaluate(board) == Evaluator.FULL_HOUSE_1_13

    # 1 10 11 12 13
    board = [
        [8, 7, 2, 5, 1],
        [6, 5, 3, 4, 10],
        [2, 4, 6, 1, 13],
        [5, 2, 1, 3, 12],
        [9, 3, 5, 6, 11]
    ]
    assert Evaluator.evaluate(board) == Evaluator.FLUSH_1_10_11_12_13
