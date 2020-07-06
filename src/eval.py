"""
In this file we provide the definition of the evaluator class which can be used
to assign the resulting scores to the board.
"""
from .board import Board
from typing import Union, List, Any, Dict


def rle(data: List[Any]) -> Dict[Any, int]:
    """
    Performs run length encoding on the data. Does not modify the original data.

    :param data: sorted list
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


class Evaluator:
    """
    In this class, the bonuses are defined as well as the points. Given the FULL
    Board (i.e. without empty cells), the Evaluator calculates the final score.
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

    @staticmethod
    def evaluate_line(line: List[int]):
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
                return Evaluator.FLUSH_1_10_11_12_13
            if max(line) - min(line) == 5 - 1:
                return Evaluator.FLUSH
            return 0

        elif len(code) == 4:
            # The only combination with four different values is a single pair,
            # and so we do not need to check any other
            return Evaluator.PAIR

        elif len(code) == 3:
            # To have three different values, either two and two values are
            # same, or three are same
            if any(x == 3 for x in code.values()):
                return Evaluator.THREE_OF_A_KIND
            else:
                return Evaluator.TWO_PAIRS

        elif len(code) == 2:
            # The only possibility here is FULL_HOUSE or four of a kind, both of
            # must be checked, and special case (four 1s) must be handled, same
            # for <1, 1, 1, 13, 13> combination
            for key, value in code.items():
                if value == 4:
                    return Evaluator.FOUR_ONES if key == 1 \
                        else Evaluator.FOUR_OF_A_KIND
            if 1 in code and 13 in code and code[1] == 3:
                return Evaluator.FULL_HOUSE_1_13
            return Evaluator.FULL_HOUSE

        else:
            # Note that we can't have more different values than five (length
            # of the line) and less than two (max four numbers of a kind), thus
            # if we get here, there is a mistake
            raise ValueError(f"Unknown combination of values: {line}")

    @staticmethod
    def _evaluate_diagonals(board: list) -> int:
        """
        Calculates the score over two main diagonals.

        :param board: game state
        :return: score of diagonals based on constants
        """
        score = 0
        main_diagonal = [board[i][i] for i in range(Board.SIZE)]
        anti_diagonal = [board[i][-i - 1] for i in range(Board.SIZE)]

        main_diagonal_score = Evaluator.evaluate_line(main_diagonal)
        anti_diagonal_score = Evaluator.evaluate_line(anti_diagonal)

        if main_diagonal_score != 0:
            score += main_diagonal_score + Evaluator.DIAGONAL_BONUS
        if anti_diagonal_score != 0:
            score += anti_diagonal_score + Evaluator.DIAGONAL_BONUS
        return score

    @staticmethod
    def evaluate(board: Union[list, Board]) -> int:
        """
        Calculates the score over the whole board.

        :param board: game plan
        :return: result score
        """
        if isinstance(board, Board):
            board = board.get()
        if any(any(x is None for x in row) for row in board):
            raise ValueError(f"Board must not have empty cells {board}")
        score = 0
        for row in board:
            score += Evaluator.evaluate_line(row)
        board_copy = list(map(list, zip(*board)))
        for col in board_copy:
            score += Evaluator.evaluate_line(col)
        score += Evaluator._evaluate_diagonals(board)

        return score
