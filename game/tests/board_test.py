import pytest

from mathematico.game import Board
from mathematico.game.board import EMPTY_CELL


def test_empty_board():
    """Check basic properties of the empty grid."""
    board = Board()
    assert board.occupied_cells == 0
    board.integrity_check()
    assert len(list(board.possible_moves())) == board.size ** 2


def test_str():
    """Test string output of the grid."""
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
                         "+--+--+--+--+--+"
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
                         "+--+--+--+--+--+"


def test_row():
    """Test basic properties of the row() function."""
    board = Board()
    assert len(board.row(0)) == board.size
    board.make_move((0, 1), 1)
    board.integrity_check()
    board.make_move((0, 2), 3)
    board.integrity_check()
    board.make_move((0, 4), 13)
    board.integrity_check()
    expected_row = [EMPTY_CELL, 1, 3, EMPTY_CELL, 13]
    assert board.row(0) == expected_row


def test_row_rle():
    """Test basic properties of the row_rle() function."""
    board = Board()
    board.make_move((0, 1), 1)
    board.make_move((0, 2), 3)

    for i in range(1, board.size):
        assert len(board.row_rle(i)) == 0
    assert board.row_rle(0) == {1: 1, 3: 1}


def test_col():
    """Test basic properties of the col() function."""
    board = Board()
    assert len(board.col(0)) == board.size
    for i in range(board.size):
        assert board.col(i) == [EMPTY_CELL]*board.size
    board.make_move((0, 1), 1)
    board.integrity_check()
    board.make_move((1, 1), 3)
    board.integrity_check()
    board.make_move((4, 1), 13)
    board.integrity_check()
    expected_col = [1, 3, EMPTY_CELL, EMPTY_CELL, 13]
    assert board.col(1) == expected_col


def test_col_rle():
    pass


def test_diag():
    """Test whether correct data are returned on the diagonal."""
    board = Board()
    EMPTY_DIAG = [EMPTY_CELL] * board.size
    assert board.diag(True) == EMPTY_DIAG
    assert board.diag(False) == EMPTY_DIAG

    board.make_move((1, 0), 5)  # outside both diagonals
    assert board.diag(True) == EMPTY_DIAG
    assert board.diag(False) == EMPTY_DIAG

    board.make_move((1, 1), 6)  # only the main
    MAIN = EMPTY_DIAG.copy()
    MAIN[1] = 6
    assert board.diag(True) == MAIN
    assert board.diag(False) == EMPTY_DIAG

    board.make_move((board.size-1, 0), 3)  # only the anti
    ANTI = EMPTY_DIAG.copy()
    ANTI[-1] = 3
    assert board.diag(True) == MAIN
    assert board.diag(False) == ANTI

    board.make_move((2, 2), 1)  # both
    assert board.size == 5
    ANTI[2] = 1
    MAIN[2] = 1
    assert board.diag(True) == MAIN
    assert board.diag(False) == ANTI


def test_make_move():
    """Test making move and updating member variables."""
    board = Board()
    board.make_move((0, 0), 13)
    assert len(list(board.possible_moves())) == 5 * 5 - 1
    assert board.row(0) == board.col(0)
    assert (0, 0) not in board.possible_moves()
    assert board.occupied_cells == 1

    board.make_move((4, 4), 1)
    assert (4, 4) not in board.possible_moves()
    assert (4, 3) in board.possible_moves()

    with pytest.raises(ValueError):
        board.make_move((4, 4), 5)


def test_unmake_move():
    pass


def test_possible_moves():
    """Test single call of possible_moves() function on the grid."""
    board = Board()
    for move in [(i, j) for i in range(4) for j in range(5)]:
        board.make_move(move, 1)
    expected_moves = [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    assert list(board.possible_moves()) == expected_moves
