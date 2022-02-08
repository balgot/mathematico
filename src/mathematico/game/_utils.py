from collections import Counter
from typing import Iterable, Dict, Any


def rle(data: Iterable, ignore: Iterable[Any]) -> Dict[Any, int]:
    """
    Performs run length encoding on the data. Does not modify the original data.
    Expected time complexity: O(n).

    :param data: list of elements (in any order)
    :param ignore: list of elements to ignore
    :return: dictionary with keys being the elements of the data and values
        being the occurrences
    """
    counter = Counter(data)
    for key in ignore:
        counter.pop(key, None)
    return counter
