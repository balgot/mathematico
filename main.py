"""
The file with showcasing the game with a Human Player, Random Player and Simple
Simulation Player.
"""
from src.game import Game
from src.player import RandomPlayer, SimpleSimulationPlayer, HumanPlayer


if __name__ == "__main__":
    game = Game()
    game.add_player(RandomPlayer())
    game.add_player(SimpleSimulationPlayer(verbose=True))
    # game.add_player(HumanPlayer())

    scores = game.start()
    descriptions = ["Random", "SSim", "Human"]
    for player, score, name in zip(game.players, scores, descriptions):
        print(f"\n{name}\t{score}\n{player.board}")
