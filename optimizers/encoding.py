def random_key(arr):
    """
    This function takes a 1-dimensional list or array as input
    and returns  a list of indices that correspond to the sorted
    elements in the original list or array. The returned list of indices
    can be used to access the sorted elements in the original list or array.
    The sorting is performed in ascending order on the values of the elements.

    :param arr: 1-dimensional array-like
    :return: 1-dimensional array-like

    Examples
    --------
    >>> ary = [0.1, 0.5, 0.3, 0.7, 0.2]
    >>> print(random_key(ary))
    [1, 5, 3, 2, 4]

    """
    return [i + 1 for i, x in sorted(enumerate(arr), key=lambda x: x[1])]
