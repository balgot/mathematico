from typing import Iterable, Any, Dict


def rle(data: Iterable) -> Dict[Any, int]:
    """
    Performs run length encoding on the data. Does not modify the original data.
    Expected time complexity: O(n).

    :param data: list of elements (in any order)
    :return: dictionary with keys being the elements of the data and values
        being the occurrences
    """
    result = {}
    for elem in data:
        result[elem] = (result[elem] or 0) + 1
    return result
