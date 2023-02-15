def random_key(arr):
    """
    Return a list of indices that correspond to the sorted elements in the input list.

    The function takes a 1-dimensional list or array of real numbers as input and returns a list of indices that
    correspond to the sorted elements. The returned list of indices can be used to access the sorted elements in the
    input list.

    :param arr: A 1-dimensional list or array of real numbers.
    :return: A list of indices that correspond to the sorted elements in the input list.

    Examples
    --------
    >>> ary = [0.1, 0.5, 0.3, 0.7, 0.2]
    >>> print(random_key(ary))
    [1, 5, 3, 2, 4]

    """
    return [i + 1 for i, _ in sorted(enumerate(arr), key=lambda x: x[1])]


def random_key_original(arr):
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
    >>> print(random_key(ary))
    [1, 4, 3, 5, 2]

    """
    indices = list(range(len(arr)))
    indices.sort(key=lambda i: arr[i])
    return [i + 1 for i, _ in sorted(enumerate(indices), key=lambda x: x[1])]

