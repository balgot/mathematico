"""
Define simple class for playing a single game of Mathematico.
"""
from random import Random
from typing import Union, List
from .player import Player


class Mathematico:
    """
    Class Mathematico controls all card picking, and asks players about moves.

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
        self.players: List[Player] = []
        self._available_cards = [i for i in range(1, 14) for _ in range(4)]
        self._random = Random(seed)
        self._random.shuffle(self._available_cards)

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
            sufficient to fill the grid
        """
        if self.finished():
            return None
        # the cards are shuffled at the beginning
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
        Checks whether the game is finished either by filling the grid or by
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
        :return: list of final scores, the index corresponds to the index
            returned by `add_player`
        """
        while not self.finished():
            next_card = self.next_card()
            assert next_card is not None
            if verbose:
                print(self)
            for player in self.players:
                player.move(next_card)
        return [player.get_score() for player in self.players]
