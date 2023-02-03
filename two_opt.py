def two_opt(route, distances):
    pass


def swap(r, i, j):
    """
    Swap two edges, or inverse the middle route.
    example: i, j = 1, 3
    A - B - C - D - E
    A - D - C - B - E

    :param r: one dimensional array-like
    :param i: first point (index)
    :param j: second point (index)
    :return: one dimensional array-like after inversion
    """
    r[i:j+1] = r[j:i-1:-1] if i != 0 else r[j::-1]
    return r
