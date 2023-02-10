import random


def inverse(r):
    """
    Inverse two edges, or the middle route.
    Where i and j are randomly picked from
    zero to the length of the input list.

    :param r: one dimensional array-like
    :return: one dimensional array-like after inversion

    Examples
    --------
    >>> i, j = 2, 5
    >>> A - B - F - E - D - C - G - H - A
    >>>         |    \ /    |
    >>>         |    / \    |
    >>> A - B - C - D - E - F - G - H - A
    """
    i, j = random_indices(len(r))

    r[i:j + 1] = r[j:i - 1:-1] if i != 0 else r[j::-1]
    return r


def random_indices(length):
    i = random.randint(0, length - 1)
    j = i
    while j == i:
        j = random.randint(0, length - 1)

    return (i, j) if i < j else (j, i)
