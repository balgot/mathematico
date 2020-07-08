"""
In this file, we will define a model that chooses the next move based on naive
statistic evaluation of all possible moves. The algorithm for evaluating any
(incomplete) position will be a generalisation of the main evaluation algorithm.
"""
from .eval import Evaluator
from typing import Dict, Union


def check_pair(line: Dict[Union[int, None], int], available: Dict[int, int])\
        -> float:
    """
    Checks whether the line might contain a pair and returns the probable score
    of such event, i.e. if there might be drawn a card that will create card,
    it will naively compute this probability and return bonus for pair
    multiplied by the probability.

    :param line: dictionary with all symbols in one line of board, including
        None for representing free space
    :param available: dictionary with available cards and their amount, these
        cards might be drawn in the future with weighted probability
    :return: expected score for drawing any (single) pair
    """
    if None not in line:  # no empty space left
        return 0
    available_cards = sum(available.values())
    value = 0
    for number, count in line.items():
        if count >= 2:  # no chance to have a pair here
            return 0
        if available[number] == 0:  # cannot make a pair with current number
            continue
        chance = Evaluator.PAIR / available_cards
        for i in range(line[None]):
            chance *= (available_cards - i - available[number])
            chance *= 1 / (available_cards - i - 1)
        value += chance
    # TODO: empty space
    return value


def check_two_pair(line: Dict[Union[int, None], int],
                   available: Dict[int, int]) -> float:
    """
    Checks whether un the future, there might be two pairs found in the line
    and computes expected score for such an event.

    :param line: dictionary with all symbols in one line of board, including
        None for representing free space
    :param available: dictionary with available cards and their amount, these
        cards might be drawn in the future with weighted probability
    :return: expected score for drawing two pair
    """
    if None not in line:  # no empty space left
        return 0
    available_cards = sum(available.values())
    value = 0
    pair_found = False
    for number, count in line.items():
        if count >= 3 or (pair_found and count == 2):
            # two pair present or impossible
            return 0

