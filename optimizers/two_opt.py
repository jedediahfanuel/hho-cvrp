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
    z = 0
    while improved:
        improved = False
        print(route)
        for i in range(len(route) - 2):
            for j in range(i + 2, len(route) - 1):
                len_delta = - distances[i][i + 1] - distances[j][j + 1] \
                            + distances[i + 1][j + 1] + distances[i][j]

                if len_delta < 0:
                    route = swap(route, i, j)
                    improved = True

    return route


def swap(r, i, j):
    """
    Swap two edges, or inverse the middle route.
    example: i, j = 1, 4
    A - B - E - D - C - F - G - H - A
    A - B - C - D - E - F - G - H - A

    :param r: one dimensional array-like
    :param i: first point (index)
    :param j: second point (index)
    :return: one dimensional array-like after inversion
    """
    r[i+1:j+1] = r[j:i:-1]
    return r
