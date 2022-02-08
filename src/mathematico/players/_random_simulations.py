import random
from time import time_ns
from typing import Optional, Tuple, List, Any
import pprint

from mathematico.game import Player, Board


def swap(list_: List[Any], i: int, j: int):
    """Swap list_[i] and list_[j]"""
    list_[i], list_[j] = list_[j], list_[i]


class SimulationPlayer(Player):
    """
    Run many random simulations and pick the move that yield the best average
    score. The move time is bounded either by max move time or number
    of simulations.
    """

    def __init__(self, max_time: Optional[int], max_simulations: Optional[int]):
        """Note: time in nanoseconds"""
        assert max_time is not None or max_simulations is not None
        super().__init__()
        self.cards: List[int] = []
        self.last_valid_card_idx = -1
        self.reset_cards()
        self.max_time: int = max_time or 10e9  # 10 seconds
        self.max_simulations: int = max_simulations or 10e50
        self.verbose = False

    def reset_cards(self):
        self.cards = [i for i in range(1, 14) for _ in range(4)]
        self.last_valid_card_idx = len(self.cards) - 1

    def reset(self) -> None:
        self.reset_cards()
        self.board = Board()

    def invalidate_card(self, card_idx):
        swap(self.cards, card_idx, self.last_valid_card_idx)
        self.last_valid_card_idx -= 1

    def revalidate_card(self, card_idx: int):
        self.last_valid_card_idx += 1
        swap(self.cards, card_idx, self.last_valid_card_idx)

    def simulate_move(self, position: Tuple[int, int], move: int) -> int:
        """Note: return score, also clean up this move"""
        self.board.make_move(position, move)
        possible_moves = list(self.board.possible_moves())

        if not possible_moves:
            score = self.board.score(remove_zeros=True) 
            self.board.unmake_move(position)
            return score

        next_card_idx = random.randint(0, self.last_valid_card_idx)
        next_move = self.cards[next_card_idx]
        move_position = random.choice(possible_moves)
        self.invalidate_card(next_card_idx)

        score = self.simulate_move(move_position, next_move)

        self.revalidate_card(next_card_idx)
        self.board.unmake_move(position)
        return score
    
    def get_score(self) -> int:
        """Return score after the game is finished."""
        return self.board.score(remove_zeros=True)

    def move(self, number: int):
        move_index = self.cards.index(number, 0, self.last_valid_card_idx)
        self.invalidate_card(move_index)

        possible_moves = list(self.board.possible_moves())
        if len(possible_moves) == 1:
            self.board.make_move(possible_moves[0], number)
            return

        scores = [0] * len(possible_moves)
        simulations = [0] * len(possible_moves)
        total_simulations = 0
        start_time = time_ns()

        while (
            time_ns() - start_time < self.max_time
            and total_simulations <= self.max_simulations - 1000
        ):
            for _ in range(10):  # do not ask for time too many times
                for i, move in enumerate(possible_moves):
                    score = self.simulate_move(move, number)
                    scores[i] += score
                    simulations[i] += 1
                    total_simulations += 1

        final_scores = [score/it for score, it in zip(scores, simulations)]
        sorted_moves = sorted(zip(final_scores, possible_moves), reverse=True)
        best_move = sorted_moves[0][1]
        self.board.make_move(best_move, number)

        if self.verbose:
            print("Final scores:")
            pprint.pprint(final_scores)
