"""
In this file, we define the interface for a player, as well as simple
implementations of the player.
"""
from .board import Board
from .eval import evaluate
from time import time_ns
import random as rnd
from typing import List, Dict, Tuple, Union
from copy import deepcopy
from abc import abstractmethod, ABC
import numpy as np




class HumanPlayer(RandomPlayer):
    """
    Human player takes inputs from console after printing the board and the
    next move number.
    """
    def move(self, number: int):
        print(self.board, f"Next card:\t{number}", sep='\n')
        row, col = None, None
        moves = list(self.board.possible_moves())

        while (row, col) not in moves:
            row = int(input(f"Row number [0, {Board.SIZE}):\t"))
            col = int(input(f"Column number [0, {Board.SIZE}):\t"))
        self.board.make_move((row, col), number)


class HistoryPlayer(Player):
    """
    HistoryPlayer, in addition to the default attributes and methods of Player,
    provides access to the cards already drawn and cards that might be drawn.
    """
    def __init__(self):
        self.board = Board()
        self.history: List[int] = []
        self.available_cards: Dict[int, int] = {}
        for card in range(1, 14):
            self.available_cards[card] = 4

    def _get_available_cards(self) -> List[int]:
        """
        From the current state of the game create a list of cards that might be
        drawn from <self._available_cards>.

        :return: list of available cards with repetition
        """
        cards = []
        for card, amount in self.available_cards.items():
            cards.extend(amount * [card])
        return cards

    def move(self, number: int):
        """
        Takes care of updating the attributes.
        Note: This method must be always overridden

        :param number: drawn cards number
        :return: None
        """
        self.history.append(number)
        self.available_cards[number] -= 1

    def get_board(self):
        return self.board


class SimpleSimulationPlayer(HistoryPlayer):
    """
    Simulates a part of Monte Carlo tree search in a way that from current state
    and next move to start, the player examines all possible moves in depth 1 by
    playing equal number of random games from each and picks the move with the
    highest score.

    Note: the algorithm is forced to make move by time
    """
    MOVE_TIME = 15_000_000_000  # number of nano-seconds 10-9

    class Node:
        def __init__(self, board: Board, position: Tuple[int, int],
                     available_cards: List[int]):
            """
            Initialize the node.
            
            :param board: board to be referenced and changed with the move
                already played
            :param position: position of the move, used for finding the best
                position
            :param available_cards: cards that might be played
            """
            self.board = board
            self.position = position
            self.available_cards = available_cards
            self.scores = []

        def simulate(self):
            """
            Performs single simulation from the current state.

            :return: None, updates the total score
            """
            board = deepcopy(self.board)
            cards = deepcopy(self.available_cards)
            moves = list(board.possible_moves())
            rnd.shuffle(cards)
            rnd.shuffle(moves)

            for move in moves:
                board.make_move(move, cards.pop())
            self.scores.append(evaluate(board))

    def __init__(self, split: bool = False, verbose: bool = False):
        """
        :param split: if True, cuts the number of nodes in halves by time
        :param verbose: if True, prints information during the <make_move>
        :return: None
        """
        super().__init__()
        self.split = split
        self.verbose = verbose

    def _spawn_nodes(self, number: int) -> List[Node]:
        """
        Spawn nodes as the children from the current state, which will simulate
        the game to pick the best action.

        :param number: number of card to be placed in the current state
        :return: list of all children nodes
        """
        nodes = []
        cards = self._get_available_cards()
        for empty_position in self.board.possible_moves():
            board = deepcopy(self.board)
            board.make_move(empty_position, number)
            nodes.append(self.Node(board, empty_position, cards))
        return nodes

    def _run_simulations(self, nodes: List[Node]) -> None:
        """
        For given time starting from now, repeatedly simulates one game from
        each node until all time is exhausted.

        :param nodes: the children that should be simulated
        :return: None
        """
        start_time = time_ns()
        end_time = start_time + self.MOVE_TIME
        while time_ns() < end_time:
            for _ in range(10):
                for node in nodes:
                    node.simulate()

    def move(self, number: int):
        """
        For each possible position, simulates equal number of games and picks
        the one with the highest score.

        :param number: the card picked
        :return: None
        """
        super().move(number)
        nodes = self._spawn_nodes(number)
        if len(nodes) != 1:
            self._run_simulations(nodes)
        best_node = max(nodes, key=lambda n: sum(n.scores))
        if self.verbose and len(nodes) > 1:
            mean = np.mean(best_node.scores)
            std = np.std(best_node.scores)
            confidence95 = 1.960 * std / np.sqrt(len(best_node.scores))
            print(
                f"Simulations:{len(best_node.scores):5d}\t|\t"
                f"95% of score: {mean:.2f} ± {confidence95:.2f}"
            )
        self.board.make_move(best_node.position, number)
