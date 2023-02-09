import random


def pmx(ind1, ind2):
    """Executes a partially matched crossover (PMX) on the input individuals.
    The two individuals are modified in place. This crossover expects
    :term:`sequence` individuals of indices, the result for any other type of
    individuals is unpredictable.

    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :returns: A tuple of two individuals.

    Moreover, this crossover generates two children by matching
    pairs of values in a certain range of the two parents and swapping the values
    of those indexes. For more details see [Goldberg1985]_.
    """

    size = min(len(ind1), len(ind2))
    p1, p2 = [0] * (size + 1), [0] * (size + 1)

    # Initialize the position of each index in the individuals
    for i in range(size):
        p1[ind1[i]] = i
        p2[ind2[i]] = i

    # Choose crossover points
    point1 = random.randint(0, size)
    point2 = random.randint(0, size - 1)

    if point2 >= point1:
        point2 += 1
    else:  # Swap the two cx points
        point1, point2 = point2, point1

    # Apply crossover between cx points
    for i in range(point1, point2):
        # Keep track of the selected values
        temp1 = ind1[i]
        temp2 = ind2[i]

        # Swap the matched value
        ind1[i], ind1[p1[temp2]] = temp2, temp1
        ind2[i], ind2[p2[temp1]] = temp1, temp2

        # Position bookkeeping
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

    return ind1, ind2
