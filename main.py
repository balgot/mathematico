"""
The file with showcasing the game with a Human Player, Random Player and Simple
Simulation Player.
"""
from src.game import Game
from src.player import *


if __name__ == "__main__":
    game = Game()
    game.add_player(SimpleSimulationPlayer(verbose=True))

    scores = game.start()
    print(scores)
