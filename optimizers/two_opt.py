def two_opt(route, distances):
    """
    Two opt is a heuristic method that swap two edges in a graph.
    It iterates over the path and check if the swap is feasible,
    then swap the sub-route, otherwise continue iterates.

    :param route: one dimensional array-like
    :param distances: matrix of distances
    :return: the array-like that have been processed
    """
    improved = True
    while improved:
        improved = False
        for i in range(len(route) - 2):
            for j in range(i + 2, len(route)):
                len_delta = - distances[i][j + 1] - distances[j][j + 1] \
                            + distances[i + 1][j + 1] + distances[i][j]

                if len_delta < 0:
                    route = swap(route, i, j)
                    improved = True

    return route


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
