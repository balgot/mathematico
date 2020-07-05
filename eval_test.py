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
    assert Evaluator.evaluate(board) == Evaluator.STRAIGHT_FLUSH


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
        Evaluator.TWO_OF_A_KIND_TWICE,
        Evaluator.STRAIGHT_FLUSH,
        Evaluator.FULL_HOUSE,
        0,
        Evaluator.FOUR_ONES,
        Evaluator.THREE_OF_A_KIND,
        Evaluator.TWO_OF_A_KIND,
        Evaluator.TWO_OF_A_KIND_TWICE,
        0,
        Evaluator.TWO_OF_A_KIND + Evaluator.DIAGONAL_BONUS,
        0
    ])
