"""
This package contains implementation of rules of the game Mathematico, that is
the game itself, evaluation and also the arena for playing.
"""
from ._board import Board
from ._eval import evaluate, Points
from ._mathematico import Player, Mathematico, Arena


__all__ = [
    "Mathematico",
    "Player",
    "Arena",
    "evaluate",
    "Points",
    "Board"
]
