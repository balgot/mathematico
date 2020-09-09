"""
Define simple class for playing a single game of Mathematico.
"""
import random as rnd
from typing import Union, List
from abc import ABC, abstractmethod
import time

from .board import Board
from .eval import evaluate


class Player(ABC):
    """
    The interface for a generic player class, which should provide methods for
    interaction with the <game> class. Required methods are move() and
    get_board().
    """
    @abstractmethod
    def move(self, card_number: int) -> None:
        """
        Given the next number, places the number on the board.

        :param card_number: the next card to be played
        :return: None
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Resets the player to initial state at the beginning of the game.

        :return: None
        """
        pass

    @abstractmethod
    def get_board(self) -> Board:
        """
        :return: current board as a Board instance
        """
        pass


class Mathematico:
    """
    Class Mathematico controls all card picking, asks players about next moves
    and assigns scores at the end.

    Attributes
        - _available_cards: list with draw-able cards
        - moves_played: counter of moves played
        - players: list with players to play the game

    Functionality
        - next_card: picks next card
        - add_player: adds a player to the game
        - finished: true if game has finished
        - play: simulates a single game

    Notes
        - each player must conform to the interface in player.py
        - only handles a single game
    """
    def __init__(self, seed=None):
        self.moves_played = 0
        self.players = []
        self._available_cards = [i for i in range(1, 14) for _ in range(4)]
        # Reseed the random number generator
        rnd.seed(seed)
        # Shuffle the cards
        rnd.shuffle(self._available_cards)
        # Reset the random number generator
        rnd.seed()

    def __str__(self) -> str:
        """
        String representation of the game with full description of the current
        state of the game, including hidden information about the deck.

        :return: string representation of the current game state
        """
        r = f"Moves played:\t{self._available_cards[:self.moves_played]}\n"
        r += "Current card:\t"
        if self.finished():
            r += "None"
        else:
            r += str(self._available_cards[self.moves_played])
        r += f"\nMove number:\t{self.moves_played}\n"
        r += f"Players:\t{self.players}"
        return r

    def next_card(self) -> Union[None, int]:
        """
        Picks next card randomly from _available_cards.

        :return: the number of the next card or None if the number of moves is
            sufficient to fill the board
        """
        if self.finished():
            return None
        card = self._available_cards[self.moves_played]
        self.moves_played += 1
        return card

    def add_player(self, player: Player) -> int:
        """
        Adds the player to the game.

        :param player: player to be added
        :return: index of player in self.players
        :raises ValueError: if the game is in progress
        """
        if self.moves_played != 0:
            raise ValueError("Game is in progress")
        self.players.append(player)
        return len(self.players) - 1

    def finished(self) -> bool:
        """
        Checks whether the game is finished either by filling the board or by
        drawing all cards from the deck.

        :return: true if no more cards will be drawn
        """
        return self.moves_played >= 25 \
            or self.moves_played >= len(self._available_cards)

    def play(self, verbose=False) -> List[int]:
        """
        Simulates one game, for each round picks one card, lets players start
        their move and at the end computes final scores.

        :param verbose: if True, prints information about game
        :return: list of final scores, the index corresponds to the index return
            by <add_player>
        """
        while not self.finished():
            next_card = self.next_card()
            assert next_card is not None
            if verbose:
                print(self)
            for player in self.players:
                player.move(next_card)
        return [evaluate(player.get_board()) for player in self.players]


class Arena:
    def __init__(self):
        self.players = []
        self.results = []

    def reset(self):
        for player_results in self.results:
            player_results.clear()

    def add_player(self, player):
        self.players.append(player)
        self.results.append([])

    def run(self, steps=100, verbose=True, seed=None):
        self.reset()
        start = time.time()
        for _ in range(steps):
            game = Mathematico(seed=seed)
            for player in self.players:
                game.add_player(player)
            results = game.play(verbose=False)
            for idx, result in enumerate(results):
                self.results[idx].append(result)
            for player in self.players:
                player.reset()
        if verbose:
            total_time = time.time() - start
            print(f"Steps run: {steps}\tElapsed time: {total_time}")
        return self.results

