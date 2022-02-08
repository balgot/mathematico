"""
This package contains implementation of rules of the game Mathematico, that is
the game itself, evaluation and also the arena for playing.


Usage:
------
    * implement Player interface, subclassing Player, using Board for keeping
      the internal state, playing moves and calculating score

    * for playing one game, use class Mathematico - this shuffles the deck,
      picks next card and notifies its players

    * to play multiple games, use class Arena
"""
from .board import Board
from ._mathematico import Mathematico
from .player import Player
from .arena import Arena


__all__ = [
    "Mathematico",
    "Player",
    "Arena",
    "Board"
]
