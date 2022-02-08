import time
from typing import List, Any

from .player import Player
from ._mathematico import Mathematico


class Arena:
    def __init__(self):
        self.players: List[Player] = []
        self.results: List[List[int]] = []

    def reset(self):
        """Clear the previous results, keep the players."""
        for player_results in self.results:
            player_results.clear()

    def add_player(self, player: Player):
        """Add new player to the arena."""
        self.players.append(player)
        self.results.append([])

    def run(self, steps: int = 100, verbose: bool = True, seed: Any = None):
        start = time.time()

        for _ in range(steps):
            game = Mathematico(seed=seed)
            for player in self.players:
                player.reset()
                game.add_player(player)
                
            results = game.play(verbose=False)
            for idx, result in enumerate(results):
                self.results[idx].append(result)

        if verbose:
            total_time = time.time() - start
            print(f"Steps run: {steps}\tElapsed time: {total_time}")

        return self.results
