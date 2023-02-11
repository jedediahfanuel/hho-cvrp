def insertion(r, i, j):
    """
    Perform insertion of a node.

    :param r: one dimensional array-like
    :param i: first point (index)
    :param j: second point (index)
    :return: one dimensional array-like after inversion

    Examples
    --------
    >>> i, j = 1, 4
    >>> A - B - E - D - C - F - G - H - A
    >>> A - C - B - D - E - F - G - H - A
    """
    r[i+1:j+1], r[i] = r[i:j], r[j]
    return r


def inverse(r, i, j):
    """
    Inverse two edges, or the middle route.

    :param r: one dimensional array-like
    :param i: first point (index)
    :param j: second point (index)
    :return: one dimensional array-like after inversion

    Examples
    --------
    >>> i, j = 1, 4
    >>> A - B - E - D - C - F - G - H - A
    >>> A - E - C - D - B - F - G - H - A
    """
    r[i:j + 1] = r[j:i-1:-1]
    return r


def swap(r, i, j):
    """
    Swap two edges, or the middle route.

    :param r: one dimensional array-like
    :param i: first point (index)
    :param j: second point (index)
    :return: one dimensional array-like after inversion

    Examples
    --------
    >>> i, j = 1, 4
    >>> A - B - E - D - C - F - G - H - A
    >>> A - C - E - D - B - F - G - H - A
    """
    r[i], r[j] = r[j], r[i]
    return r


def two_opt_insertion(route, distances):
    """
    Two opt is a heuristic method that insert a node into another index.
    It iterates over the path and check if the insertion is feasible,
    then do insertion to the node, otherwise continue iterates.

    :param route: one dimensional array-like
    :param distances: matrix of distances
    :return: the array-like that have been processed
    """
    improved = True
    while improved:
        improved = False

        for i in range(len(route) - 2):
            for j in range(i + 2, len(route) - 1):
                len_delta = - distances[route[i - 1]][route[i]] \
                            - distances[route[j - 1]][route[j]] \
                            - distances[route[j]][route[j + 1]] \
                            + distances[route[i - 1]][route[j]] \
                            + distances[route[j]][route[i]] \
                            + distances[route[j - 1]][route[j + 1]]

                if len_delta < 0:
                    route = insertion(route, i, j)
                    improved = True

    return route


def two_opt_inverse(route, distances):
    """
    Two opt is a heuristic method that inverse two edges in a graph.
    It iterates over the path and check if the inverse is feasible,
    then inverse the sub-route, otherwise continue iterates.

    :param route: one dimensional array-like
    :param distances: matrix of distances
    :return: the array-like that have been processed
    """
    improved = True
    while improved:
        improved = False

        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                len_delta = - distances[route[i - 1]][route[i]] - distances[route[j]][route[j + 1]] \
                            + distances[route[i - 1]][route[j]] + distances[route[i]][route[j + 1]]

                if len_delta < 0:
                    route = inverse(route, i, j)
                    improved = True

    return route


def two_opt_swap(route, distances):
    """
    Two opt is a heuristic method that swap two node in a graph.
    It iterates over the path and check if the swap is feasible,
    then swap the two node, otherwise continue iterates.

    :param route: one dimensional array-like
    :param distances: matrix of distances
    :return: the array-like that have been swapped
    """
    improved = True
    while improved:
        improved = False

        for i in range(1, len(route)):
            for j in range(i + 1, len(route) - 1):
                if i + 1 == j:
                    len_delta = - distances[route[i - 1]][route[i]] - distances[route[j]][route[j + 1]] \
                                + distances[route[i - 1]][route[j]] + distances[route[i]][route[j + 1]]
                else:
                    len_delta = - distances[route[i - 1]][route[i]] - distances[route[i]][route[i + 1]] \
                                - distances[route[j - 1]][route[j]] - distances[route[j]][route[j + 1]] \
                                + distances[route[i - 1]][route[j]] + distances[route[j]][route[i + 1]] \
                                + distances[route[j - 1]][route[i]] + distances[route[i]][route[j + 1]]

                if len_delta < 0:
                    route = swap(route, i, j)
                    improved = True

    return route
