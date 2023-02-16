import random
import copy
import numpy as np


def pmx_on(parent1, parent2):
    # randomly select two crossover points
    cp = sorted(np.random.randint(len(parent1), size=2))

    # create two empty offspring solutions
    offspring1, offspring2 = [-1] * len(parent1), [-1] * len(parent1)

    # copy the subsequence between the crossover points from the first parent to the offspring
    offspring1[cp[0]:cp[1] + 1] = parent2[cp[0]:cp[1] + 1]
    offspring2[cp[0]:cp[1] + 1] = parent1[cp[0]:cp[1] + 1]
    mid1 = parent2[cp[0]:cp[1] + 1]
    mid2 = parent1[cp[0]:cp[1] + 1]

    for i in range(len(parent1)):
        if i < cp[0] or i > cp[1]:
            offspring1[i] = parent1[i]
            search = True
            idx = copy.deepcopy(offspring1[i])
            while search:
                try:
                    idx = copy.deepcopy(mid1.index(idx))
                    idx = copy.deepcopy(mid2[idx])
                except ValueError:
                    search = False
                    offspring1[i] = idx

            offspring2[i] = parent2[i]
            search = True
            idx = copy.deepcopy(offspring2[i])
            while search:
                try:
                    idx = copy.deepcopy(mid2.index(idx))
                    idx = copy.deepcopy(mid1[idx])
                except ValueError:
                    search = False
                    offspring2[i] = idx

    return offspring1, offspring2


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
