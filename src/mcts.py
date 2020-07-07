"""
In this file, we define a Monte Carlo algorithm for solving the game of
Mathematico. We will rely on the random roll-outs and the search will be limited
by the time.
"""
from .player import HistoryPlayer
from .board import Board
from .eval import Evaluator
from time import time
from typing import Tuple, Dict, List, Union
from copy import deepcopy
import random as rnd


class State:
    """
    Represents a single state of the game in the Monte Carlo Tree search. The
    implementation of the search will rely on the reusing the tree, so we can
    do as many simulations as possible. On the top of that, the deck is shuffled
    at the beginning of each simulation.

    Note: we keep separate states for the nature move
    """
    def __init__(self, parent: 'State', board: Board, deck: List[int],
                 nature_move: bool):
        """
        Initialize the state of the game.

        :param parent: parent node in the tree
        :param board: board to be referenced
        :param deck: available cards to be drawn
        :param nature_move: True if the card should be drawn, False if it should
            be placed on the board
        """
        self.parent = parent
        self.board = board
        self.deck = deck
        self.nature_move = nature_move
        self.is_terminal = all(all(cell is not None for cell in row)
                               for row in self.board.get())
        assert not self.is_terminal or self.nature_move
        self.fully_expanded = self.is_terminal
        self.visits: int = 0
        self.score: int = 0
        self.children: Dict[Union[int, Tuple[int, int]], 'State'] = {}

    def rollout(self) -> int:
        """
        Performs random simulation from the current board.

        :return: the score at the end of the simulation
        """
        rnd.shuffle(self.deck)
        deck = deepcopy(self.deck)
        board = deepcopy(self.board)

        iterations = 25 - board.occupied_cells
        for _ in range(iterations):
            card = deck.pop()
            move = rnd.choice(board.possible_moves())
            board.make_move(move, card)
        return Evaluator.evaluate(board)

    def select(self) -> 'State':
        """
        Finds the best child of the current node to examine.

        :return: best of the node's children
        """
        if self.is_terminal:
            return self
        if self.fully_expanded:



class MonteCarlo:
    """
    Using Monte Carlo Tree Search, finds the most promising move in the current
    state and plays it. Keeps the tree from the previous moves.
    """
    SIMULATIONS = 5

    def __init__(self, seconds: int = 5):
        """
        Initialises the Monte Carlo Tree Search.

        :param seconds: time limit for the search
        """
        self.time_limit = seconds

    def search(self, root: State) -> Tuple[int, int]:
        """
        Finds the most promising move from current state.

        :param root: initial search state
        :return: the best move for nature xor player
        """
        root.parent = None
        assert root.nature_move is False
        end_time = time() + self.time_limit
        while time() < end_time:
            self._round(root)
        best_move, best_child = self._get_best_child(root, 0)
        return best_move

    def _round(self, root: State) -> None:
        """
        Performs a single round of the MonteCarlo algorithm.

        :param root: initial state to search the game space from
        :return: None
        """
        node = self._select(root)
        reward = 0
        for _ in range(self.SIMULATIONS):
            reward += node.rollout()
        self._backpropagate(node, reward)

    def _backpropagate(self, node: State, reward: int) -> None:
        """
        Updates the information all the way back to the root of the tree.

        :param node: leaf node the simulation started at
        :param reward: simulated score
        :return: None
        """
        while node is not None:
            node.score += reward
            node.visits += self.SIMULATIONS
            node = node.parent

    def _get_best_child(self, exploration_value: int)\
            -> Tuple[Tuple[int, int], State]:
        pass



