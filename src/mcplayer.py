from player import Player, RandomPlayer
from board import Board
from game import Game
import random as rnd
from copy import deepcopy
from time import time
from typing import Tuple


class Node:
    """
    Represents a node in a game tree
    """
    def __init__(self, board: Board, move: Tuple[int, int], card: int, cards):
        self.board = deepcopy(board)
        self.score = 0
        self.board.make_move(move, card)
        self.available_cards = cards
        self.move = move

    def rollout(self):
        """
        Plays a random game from the current state, computes the score
        and updates total score of the node
        :return: None
        """
        player = RandomPlayer()
        player.board = deepcopy(self.board)
        game = Game()
        game.available_cards = self.available_cards
        rnd.shuffle(game.available_cards)
        game.add_player(player)
        self.score += game.start()


class SimulationMCTS(Player):
    """
    Simulates a part of Monte Carlo tree search in a way that
    from current state and next move to start, the player examines all
    possible moves in depth 1 by playing equal number of random games
    from each and picks the move with the highest score
    Note: the algorithm is forced to make move by time
    """
    MOVE_TIME = 30  # number of seconds

    def __init__(self):
        super().__init__()
        self.available_cards = {}  # stores number and amount of available cards
        for card in range(1, 14):
            self.available_cards[card] = 4

    def _get_cards(self):
        """
        From current state returns all cards that might be drawn
        :return: list of cards
        """
        cards = []
        for card, amount in self.available_cards.items():
            cards.extend(amount * [card])
        return cards

    def move(self, number: int):
        self.available_cards[number] -= 1
        start_time = time()

        cards = self._get_cards()
        nodes = [Node(self.board, move, number, cards) for move in self.board.possible_moves()]

        iters = 0
        while time() - start_time < self.MOVE_TIME:
            for node in nodes:
                node.rollout()
        print(iters)
        best_node = max(nodes, key=lambda n: n.score)
        self.board.make_move(best_node.move, number)


if __name__ == "__main__":
    player = SimulationMCTS()
    game = Game()
    game.add_player(player)
    game.start()
