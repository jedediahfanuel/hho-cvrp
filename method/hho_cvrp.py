import time
import random
import math

import method.mutate as mutate
from method.crossover import pmx
from method.encode import random_key
from method.local import two_opt_inverse
from method.local import two_opt_insertion

from model.solution import Solution
from controller.benchmarks import concat_depot
from controller.benchmarks import normal_cvrp
from controller.benchmarks import split_customer

import numpy


def hho(objf, data, sol, search_agent_no, max_iter):
    """
    This function is Harris Hawks Optimization for CVRP.

    Parameters
    ----------
    objf : function
        an objective function (check benchmarks.py)
    data : CVRP Class
        an instance class downloaded from cvrplib
    sol : Solution Class
        a solution class downloaded from cvrplib
    search_agent_no : int
        equivalent as population size (number of hawks)
    max_iter : int
        equivalent as number of iterations (maximum iteration before it stopped)

    Returns
    -------
    s : Solution
        a local defined solution class (check solution.py)
    """

    lb, ub, dim, distances = 1, data.n_customers, data.n_customers, data.distances
    max_capacity, demands = data.capacity, data.demands
    best_route, bks = None, sol.cost

    # initialize the location and Energy of the rabbit
    rabbit_location = numpy.zeros(dim)

    # change this to -inf for maximization problems
    rabbit_energy = float("inf")
    fs = [float("inf") for _ in range(search_agent_no)]

    if not isinstance(lb, list):
        lb = [lb for _ in range(dim)]
        ub = [ub for _ in range(dim)]
    lb = numpy.array(lb)
    ub = numpy.array(ub)

    # Initialize the locations of Harris' hawks
    x_hawks = numpy.array(
        [x * (ub - lb) + lb for x in numpy.random.uniform(0, 1, (search_agent_no, dim))]
    )

    # Initialize convergence
    convergence_curve = numpy.zeros(max_iter)

    ############################
    s = Solution()

    print('HHO is now tackling "' + objf.__name__ + '" ' + data.name)

    timer_start = time.time()
    s.start_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    ############################

    t = 0  # Loop counter

    for i in range(0, search_agent_no):

        # fitness of locations
        x_hawks[i, :] = random_key(x_hawks[i, :])
        fitness = objf(x_hawks[i, :].astype(int), distances, max_capacity, demands)
        fs[i] = fitness

        # Update the location of Rabbit
        if fitness < rabbit_energy:  # Change this to > for maximization problem
            rabbit_energy = fitness
            rabbit_location = x_hawks[i, :].copy()

    # Main loop
    while t < max_iter:
        e1 = 2 * (1 - (t / max_iter))  # factor to show the decreasing energy of rabbit

        # Update the location of Harris' hawks
        for i in range(0, search_agent_no):

            e0 = 2 * random.random() - 1  # -1 < e0 < 1
            escaping_energy = e1 * (
                e0
            )  # escaping energy of rabbit Eq. (3) in the paper

            # -------- Exploration phase Eq. (1) in paper -------------------

            if abs(escaping_energy) >= 1:
                # Harris' hawks perch randomly based on 2 strategy:
                q = random.random()
                rand_hawk_index = math.floor(search_agent_no * random.random())
                x_rand = x_hawks[rand_hawk_index, :]
                if q >= 0.5:
                    # perch based on other family members
                    x_hawks[i, :] = x_rand - random.random() * abs(
                        x_rand - 2 * random.random() * x_hawks[i, :]
                    )
                    x_hawks[i, :] = mutate.swap(random_key(x_hawks[i, :]))

                elif q < 0.5:
                    # perch on a random tall tree (random site inside group's home range)
                    x_hawks[i, :] = (rabbit_location - x_hawks.mean(0)) - random.random() * (
                            (ub - lb) * random.random() + lb
                    )
                    x_hawks[i, :] = mutate.inverse(random_key(x_hawks[i, :]))

            # -------- Exploitation phase -------------------
            elif abs(escaping_energy) < 1:
                # Attacking the rabbit using 4 strategies regarding the behavior of the rabbit

                # phase 1: ----- surprise pounce (seven kills) ----------
                # surprise pounce (seven kills): multiple, short rapid dives by different hawks

                r = random.random()  # probability of each event

                if (
                        r >= 0.5 > abs(escaping_energy)
                ):  # Hard besiege Eq. (6) in paper
                    x_hawks[i, :] = rabbit_location - escaping_energy * abs(
                        rabbit_location - x_hawks[i, :]
                    )
                    x_hawks[i, :] = mutate.swap(random_key(x_hawks[i, :]))

                if (
                        r >= 0.5 and abs(escaping_energy) >= 0.5
                ):  # Soft besiege Eq. (4) in paper
                    jump_strength = 2 * (
                            1 - random.random()
                    )  # random jump strength of the rabbit
                    x_hawks[i, :] = (rabbit_location - x_hawks[i, :]) - escaping_energy * abs(
                        jump_strength * rabbit_location - x_hawks[i, :]
                    )
                    x_hawks[i, :] = mutate.swap(random_key(x_hawks[i, :]))

                # phase 2: --------performing team rapid dives (leapfrog movements)----------

                if (
                        r < 0.5 <= abs(escaping_energy)
                ):  # Soft besiege Eq. (10) in paper
                    # rabbit try to escape by many zigzag deceptive motions
                    jump_strength = 2 * (1 - random.random())
                    x1 = rabbit_location - escaping_energy * abs(
                        jump_strength * rabbit_location - x_hawks[i, :]
                    )
                    x1 = mutate.swap(random_key(x1))
                    x1, x2 = pmx(
                        random_key(rabbit_location),
                        x1
                    )

                    xo1 = objf(x1, distances, max_capacity, demands)
                    xo2 = objf(x2, distances, max_capacity, demands)

                    yobjf = xo1 if xo1 < xo2 else xo2
                    y = x1 if xo1 < xo2 else x2

                    if yobjf < fs[i]:  # improved move?
                        x_hawks[i, :] = numpy.array(y).copy()
                    else:  # hawks perform levy-based short rapid dives around the rabbit
                        x2 = (
                                rabbit_location
                                - escaping_energy
                                * abs(jump_strength * rabbit_location - x_hawks[i, :])
                                + numpy.multiply(numpy.random.randn(dim), levy(dim))
                        )
                        x2 = mutate.insertion(random_key(x2))
                        x2 = two_opt_inverse(concat_depot(x2), distances)[1:-1]

                        if objf(x2, distances, max_capacity, demands) < fs[i]:
                            x_hawks[i, :] = x2.copy()
                if (
                        r < 0.5 and abs(escaping_energy) < 0.5
                ):  # Hard besiege Eq. (11) in paper
                    jump_strength = 2 * (1 - random.random())
                    x1 = rabbit_location - escaping_energy * abs(
                        jump_strength * rabbit_location - x_hawks.mean(0)
                    )
                    x1 = mutate.inverse(random_key(x1))

                    if objf(x1, distances, max_capacity, demands) < fs[i]:  # improved move?
                        x_hawks[i, :] = x1.copy()
                    else:  # Perform levy-based short rapid dives around the rabbit
                        x2 = (
                                rabbit_location
                                - escaping_energy
                                * abs(jump_strength * rabbit_location - x_hawks.mean(0))
                                + numpy.multiply(numpy.random.randn(dim), levy(dim))
                        )
                        x2 = mutate.insertion(random_key(x2))

                        if objf(x2, distances, max_capacity, demands) < fs[i]:
                            x_hawks[i, :] = x2.copy()

        for i in range(0, search_agent_no):

            # fitness of locations
            if t == max_iter - 1:
                # Finishing Phase
                test_route = split_customer(random_key(x_hawks[i, :]), max_capacity, demands)
                test_route = cvrp_inverse(test_route, distances)
                test_route = cvrp_insertion(test_route, distances)

            fitness = objf(x_hawks[i, :].astype(int), distances, max_capacity, demands
                           ) if t < max_iter - 1 else normal_cvrp(test_route, distances)
            fs[i] = fitness

            # Update the location of Rabbit
            if fitness < rabbit_energy:  # Change this to > for maximization problem
                rabbit_energy = fitness
                rabbit_location = x_hawks[i, :].copy()

                if t == max_iter - 1:
                    best_route = test_route

        convergence_curve[t] = rabbit_energy
        if t % 1 == 0:
            print(
                "At iteration " + str(t) + " the best fitness is " + str(rabbit_energy)
            )
        t = t + 1

        # stop iteration if bks is reached, fill convergence with bks
        if rabbit_energy <= bks:
            convergence_curve = [rabbit_energy if conv == 0 else conv for conv in convergence_curve]
            break

    timer_end = time.time()
    s.end_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    s.execution_time = timer_end - timer_start
    s.convergence = convergence_curve
    s.optimizer = "HHO"
    s.objfname = objf.__name__
    s.bks = bks
    s.best = rabbit_energy
    s.best_individual = rabbit_location
    s.name = data.name
    s.routes = best_route if best_route is not None else split_customer(
        rabbit_location.astype(int), max_capacity, demands)
    s.dim = data.dimension
    s.coordinates = data.coordinates

    return s


def levy(dim):
    """
    This function is a Lévy flight function.

    :param dim: integer of problem dimension
    :return: value of Lévy flight
    """
    beta = 1.5
    sigma = (
                    math.gamma(1 + beta) * math.sin(math.pi * beta / 2)
                    / (math.gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))
            ) ** (1 / beta)
    u = 0.01 * numpy.random.randn(dim) * sigma
    v = numpy.random.randn(dim)
    zz = numpy.power(numpy.absolute(v), (1 / beta))
    step = numpy.divide(u, zz)
    return step


def cvrp_insertion(routes, distances):
    """
    This function accepts a list of routes in which
    each route will be processed using insertion 2-opt

    Parameters
    ----------
    routes : cvrp solution representation
        list of routes
    distances : list
        matrix of distance

    Returns
    -------
    x : cvrp solution representation
        list of routes after insertion 2-opt
    """

    return [two_opt_insertion(r, distances) for r in routes]


def cvrp_inverse(routes, distances):
    """
    This function accepts a list of routes in which
    each route will be processed using inverse 2-opt

    Parameters
    ----------
    routes : cvrp solution representation
        list of routes
    distances : list
        matrix of distance

    Returns
    -------
    x : cvrp solution representation
        list of routes after inverse 2-opt
    """

    return [two_opt_inverse(r, distances) for r in routes]
