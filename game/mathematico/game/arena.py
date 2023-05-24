import time
from typing import List, Any

from .player import Player
from ._mathematico import Mathematico


class Arena:
    """
    This class allows simulating multiple rounds of the game Mathematico.

    Mehods
    ------
        reset: reset the results so far
        add_player: add a player to the arena
        run: run the simulation
    """

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

    def run(self, rounds: int = 100, verbose: bool = True, seed: Any = None):
        """
        Repeatedly play the game of Mathematico.

        Play Mathematico for the specified number of rounds and
        record the statistics (final score) for each of the players.

        Arguments
        ---------
            rounds: number of rounds to play
            verbose: if True, print the elapsed time, also passed
                to each round
            seed: the seed to play the same game from

        Returns
        -------
            result: 2d list, `results[idx]` is the list of scores
                obtained by `idx`-th player
        """
        start = time.time()

        for i in range(rounds):
            # initialize a new game
            game = Mathematico(seed=seed+i)
            for player in self.players:
                player.reset()
                game.add_player(player)

            # play the game and collect rewards
            results = game.play(verbose=False)
            for idx, result in enumerate(results):
                self.results[idx].append(result)

        if verbose:
            total_time = time.time() - start
            print(f"Steps run: {rounds}\tElapsed time: {total_time}")

        return self.results
