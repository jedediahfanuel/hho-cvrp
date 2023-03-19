def rke(arr):
    """
    Return a list of indices that correspond to the sorted elements in the original sequence.

    The function takes a 1-dimensional list or array of real numbers as input and returns a list of indices that
    correspond to the sorted elements in the original sequence. The returned list of indices can be used to access
    the sorted elements in the original sequence.

    :param arr: A 1-dimensional list or array of real numbers.
    :return: A list of indices that correspond to the sorted elements in the original sequence.

    Examples
    --------
    >>> ary = [0.1, 0.5, 0.3, 0.7, 0.2]
    >>> print(rke(ary))
    [1, 4, 3, 5, 2]
    """

    indices = list(range(len(arr)))
    indices.sort(key=lambda i: arr[i])
    return [i + 1 for i, _ in sorted(enumerate(indices), key=lambda x: x[1])]

