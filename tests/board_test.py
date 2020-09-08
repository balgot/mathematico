from src.game import Board
import numpy as np


def test_empty_board():
    """
    Checks basic properties of the empty board.
    """
    board = Board()
    assert board.occupied_cells == 0
    board.integrity_check()
    assert len(list(board.possible_moves())) == Board.SIZE ** 2


def test_str():
    """
    Tests string output of the board.
    """
    board = Board()
    assert str(board) == "+--+--+--+--+--+\n" \
                         "|  |  |  |  |  |\n" \
                         "+--+--+--+--+--+\n" \
                         "|  |  |  |  |  |\n" \
                         "+--+--+--+--+--+\n" \
                         "|  |  |  |  |  |\n" \
                         "+--+--+--+--+--+\n" \
                         "|  |  |  |  |  |\n" \
                         "+--+--+--+--+--+\n" \
                         "|  |  |  |  |  |\n" \
                         "+--+--+--+--+--+\n"
    board.make_move((0, 0), 1)
    board.make_move((1, 0), 12)
    assert str(board) == "+--+--+--+--+--+\n" \
                         "| 1|  |  |  |  |\n" \
                         "+--+--+--+--+--+\n" \
                         "|12|  |  |  |  |\n" \
                         "+--+--+--+--+--+\n" \
                         "|  |  |  |  |  |\n" \
                         "+--+--+--+--+--+\n" \
                         "|  |  |  |  |  |\n" \
                         "+--+--+--+--+--+\n" \
                         "|  |  |  |  |  |\n" \
                         "+--+--+--+--+--+\n"


def test_row():
    """
    Tests basic properties of the row() function.
    """
    board = Board()
    assert len(board.row(0)) == Board.SIZE
    for i in range(Board.SIZE):
        assert all(board.row(i) == np.full((Board.SIZE,), Board.EMPTY))
    board.make_move((0, 1), 1)
    board.integrity_check()
    board.make_move((0, 2), 3)
    board.integrity_check()
    board.make_move((0, 4), 13)
    board.integrity_check()
    expected_row = np.asarray([Board.EMPTY, 1, 3, Board.EMPTY, 13])
    assert all(board.row(0) == expected_row)


def test_row_rle():
    """
    Tests basic properties of the row_rle() function.
    """
    board = Board()
    board.make_move((0, 1), 1)
    board.make_move((0, 2), 3)

    for i in range(1, Board.SIZE):
        assert len(board.row_rle(i)) == 0
    assert board.row_rle(0) == {1: 1, 3: 1}


def test_col():
    """
    Tests basic properties of the col() function.
    """
    board = Board()
    assert len(board.col(0)) == Board.SIZE
    for i in range(Board.SIZE):
        assert all(board.col(i) == np.full((Board.SIZE,), Board.EMPTY))
    board.make_move((0, 1), 1)
    board.integrity_check()
    board.make_move((1, 1), 3)
    board.integrity_check()
    board.make_move((4, 1), 13)
    board.integrity_check()
    expected_col = np.asarray([1, 3, Board.EMPTY, Board.EMPTY, 13])
    assert all(board.col(1) == expected_col)


def test_col_rle():
    pass


def test_diag():
    pass


def test_make_move():
    """
    Tests making move and updating member variables.
    """
    board = Board()
    board.make_move((0, 0), 13)
    assert len(list(board.possible_moves())) == 5 * 5 - 1
    assert all(board.row(0) == board.col(0))
    assert (0, 0) not in board.possible_moves()
    assert board.occupied_cells == 1

    board.make_move((4, 4), 1)
    assert (4, 4) not in board.possible_moves()
    assert (4, 3) in board.possible_moves()

    raised = False
    try:
        board.make_move((4, 4), 5)
    except ValueError:
        raised = True
    assert raised


def test_unmake_move():
    pass


def test_possible_moves():
    """
    Tests single call of possible_moves() function on the board.
    """
    board = Board()
    for move in [(i, j) for i in range(4) for j in range(5)]:
        board.make_move(move, 1)
    expected_moves = [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    assert list(board.possible_moves()) == expected_moves
