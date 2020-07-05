"""
In this file, we define the interface for a player,
as well as simple implementations of the player
"""
from board import Board
from eval import Evaluator
from time import time_ns
import random as rnd
from typing import List, Dict, Tuple
from copy import deepcopy
# import joblib


class Player:
    """
    The interface for a generic player class, which should provide
    methods for interaction with the <game> class
    """
    def __init__(self):
        self.board = Board()

    def move(self, number: int):
        """
        Given the next number, places the number on the board
        :param number: the next card to be played
        :return: None
        """
        pass

    def get_board(self):
        return self.board


class RandomPlayer(Player):
    """
    Random player plays moves randomly on empty positions.
    """
    def move(self, number: int):
        possible_moves = self.board.possible_moves()
        if not possible_moves:
            raise IndexError("No moves available")
        picked_move = rnd.choice(possible_moves)
        self.board.make_move(picked_move, number)


class HumanPlayer(Player):
    """
    Human player takes inputs from console after printing the
    board and the next move number
    """
    def move(self, number: int):
        print(self.board)
        print(f"Next card:\t{number}")
        row, col = None, None
        moves = self.board.possible_moves()

        while (row, col) not in moves:
            row = int(input(f"Row number [0, {Board.SIZE}):\t"))
            col = int(input(f"Column number [0, {Board.SIZE}):\t"))
        self.board.make_move((row, col), number)


class HistoryPlayer(Player):
    """
    HistoryPlayer, in addition to the default attributes
    and methods of Player, provides access to the cards
    already drawn and cards that might be drawn
    """
    def __init__(self):
        super().__init__()
        self.history: List[int] = []
        self.available_cards: Dict[int, int] = {}
        for card in range(1, 14):
            self.available_cards[card] = 4

    def _get_available_cards(self) -> List[int]:
        """
        From the current state of the game create a list of
        cards that might be drawn from <self.available_cards>
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
        :param number:
        :return: None
        """
        self.history.append(number)
        self.available_cards[number] -= 1


class SimpleSimulationPlayer(HistoryPlayer):
    """
    Simulates a part of Monte Carlo tree search in a way that
    from current state and next move to start, the player examines all
    possible moves in depth 1 by playing equal number of random games
    from each and picks the move with the highest score
    Note: the algorithm is forced to make move by time
    """
    MOVE_TIME = 10_000_000_000  # number of nano-seconds 10-9

    class Node:
        def __init__(self, board: Board, position: Tuple[int, int], available_cards: List[int]):
            """
            Initialize the node
            :param board: board to be referenced and changed with the move already played
            :param position: position of the move, used for finding the best position
            :param available_cards: cards that might be played
            """
            self.board = board
            self.position = position
            self.available_cards = available_cards
            self.total_score = 0
            self.simulations = 1  # prevents division by zero

        def simulate(self):
            """
            Performs single simulation from the current state
            :return: None, updates the total score
            """
            board = deepcopy(self.board)
            cards = deepcopy(self.available_cards)
            rnd.shuffle(cards)
            while board.possible_moves():
                card = cards.pop()
                position = rnd.choice(board.possible_moves())
                board.make_move(position, card)
            self.total_score += Evaluator.evaluate(board)
            self.simulations += 1

    def __init__(self, split: bool = False):
        """
        :param split: if True, cuts the number of nodes in halves by time
        :return: None
        """
        super().__init__()
        self.split = split

    def move(self, number: int):
        """
        For each possible position, simulates equal
        number of games and picks the one with the highest score
        :param number: the card picked
        :return: None
        """
        super().move(number)
        nodes = []
        cards = self._get_available_cards()
        for position in self.board.possible_moves():
            board = deepcopy(self.board)
            board.make_move(position, number)
            nodes.append(self.Node(board, position, cards))
        start_time = time_ns()
        delta = self.MOVE_TIME / len(nodes)
        mid_time = start_time + delta
        while time_ns() - start_time < self.MOVE_TIME:
            if len(nodes) == 1:
                break
            for node in nodes:
                node.simulate()
            if time_ns() >= mid_time and self.split:
                nodes.sort(key=lambda n: n.total_score, reverse=True)
                nodes.pop()
                mid_time += delta
        best_node = max(nodes, key=lambda n: n.total_score)
        print(f"{self.split}-Simulations:\t"
              f"{best_node.simulations:4d}\t"
              f"score\t{best_node.total_score / best_node.simulations:.2f}"
              f"\tnodes {len(nodes)}", flush=True)
        self.board.make_move(best_node.position, number)


if __name__ == "__main__":

    from game import Game
    game = Game()
    game.add_player(SimpleSimulationPlayer(split=False))
    game.add_player(SimpleSimulationPlayer(split=True))
    print(game.start())
    print("SPLIT=False", game.players[0].board, sep='\n')
    print("SPLIT=True", game.players[1].board, sep='\n')
    exit()

    from game import Game
    print("Simple Comparison of Available Non-Human Players")
    total_random, total_simulation = 0, 0
    ROUNDS = 10_000
    print('|', '-' * 18, '|', sep='')

    for i in range(ROUNDS):
        if i % (ROUNDS // 20) == 0:
            print('=', end='', flush=True)
        random_player = RandomPlayer()
        simulation_player = SimpleSimulationPlayer()

        game = Game()
        game.add_player(random_player)
        game.add_player(simulation_player)
        result = game.start()
        total_random += result[0]
        total_simulation += result[1]

    print("Random Player Average Score:", total_random / ROUNDS, sep='\t')
    print("Simulation Player Average Score:", total_simulation / ROUNDS, sep='\t')


    ###################################################
    #               INTERACTIVE GAME                  #
    ###################################################
    g = Game()
    g.add_player(HumanPlayer())
    print(g.start(verbose=True))

    # noinspection PyShadowingNames,PyShadowingNames
    def stats(rounds: int = 1000):
        total = 0
        for i in range(rounds):
            if i % (rounds / 20) == 0:
                print('=', end='', flush=True)
            player = RandomPlayer()
            game = Game()
            _ = game.add_player(player)
            total += game.start()[0]
        return total / rounds


    stats(100_000)
