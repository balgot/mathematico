from board import Board


def test_make_move():
    board = Board().make_move((0, 0), 13)
    assert len(board.possible_moves()) == 5 * 5 - 1
    board.make_move((4, 4), 0)
    assert (4, 4) not in board.possible_moves()
    assert (4, 3) in board.possible_moves()

    raised = False
    try:
        board.make_move((4, 4), 0)
    except ValueError:
        raised = True
    assert raised


def test_possible_moves():
    board = Board()
    for move in [(i, j) for i in range(4) for j in range(5)]:
        board.make_move(move, 1)
    assert board.possible_moves() == [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]


def test_str():
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
    board.make_move((0, 0), 1).make_move((1, 0), 12)
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