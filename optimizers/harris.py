import random
import numpy
import math
from solution import solution
import time


def HHO(objf, instance, SearchAgents_no, Max_iter):
    lb, ub, dim, distances = 1, instance.dimension - 0.01, instance.n_customers, instance.distances

    # initialize the location and Energy of the rabbit
    Rabbit_Location = numpy.zeros(dim)
    Rabbit_Energy = float("inf")  # change this to -inf for maximization problems

    if not isinstance(lb, list):
        lb = [lb for _ in range(dim)]
        ub = [ub for _ in range(dim)]
    lb = numpy.asarray(lb)
    ub = numpy.asarray(ub)

    # Initialize the locations of Harris' hawks
    X = numpy.asarray(
        [x * (ub - lb) + lb for x in numpy.random.uniform(0, 1, (SearchAgents_no, dim))]
    )

    # Initialize convergence
    convergence_curve = numpy.zeros(Max_iter)

    ############################
    s = solution()

    print('HHO is now tackling  "' + objf.__name__ + '"')

    timerStart = time.time()
    s.startTime = time.strftime("%Y-%m-%d-%H-%M-%S")
    ############################

    t = 0  # Loop counter

    # Main loop
    while t < Max_iter:
        for i in range(0, SearchAgents_no):

            # Check boundaries

            X[i, :] = numpy.clip(X[i, :], lb, ub)

            # fitness of locations
            fitness = objf(generate_unstable_solution(X[i, :], lb, ub), distances)

            # Update the location of Rabbit
            if fitness < Rabbit_Energy:  # Change this to > for maximization problem
                Rabbit_Energy = fitness
                Rabbit_Location = X[i, :].copy()

        E1 = 2 * (1 - (t / Max_iter))  # factor to show the decreasing energy of rabbit

        # Update the location of Harris' hawks
        for i in range(0, SearchAgents_no):

            E0 = 2 * random.random() - 1  # -1<E0<1
            Escaping_Energy = E1 * (
                E0
            )  # escaping energy of rabbit Eq. (3) in the paper

            # -------- Exploration phase Eq. (1) in paper -------------------

            if abs(Escaping_Energy) >= 1:
                # Harris' hawks perch randomly based on 2 strategy:
                q = random.random()
                rand_Hawk_index = math.floor(SearchAgents_no * random.random())
                X_rand = X[rand_Hawk_index, :]
                if q < 0.5:
                    # perch on a random tall tree (random site inside group's home range)
                    X[i, :] = X_rand - random.random() * abs(
                        X_rand - 2 * random.random() * X[i, :]
                    )

                elif q >= 0.5:
                    # perch based on other family members
                    X[i, :] = (Rabbit_Location - X.mean(0)) - random.random() * (
                            (ub - lb) * random.random() + lb
                    )

            # -------- Exploitation phase -------------------
            elif abs(Escaping_Energy) < 1:
                # Attacking the rabbit using 4 strategies regarding the behavior of the rabbit

                # phase 1: ----- surprise pounce (seven kills) ----------
                # surprise pounce (seven kills): multiple, short rapid dives by different hawks

                r = random.random()  # probability of each event

                if (
                        r >= 0.5 and abs(Escaping_Energy) < 0.5
                ):  # Hard besiege Eq. (6) in paper
                    X[i, :] = (Rabbit_Location) - Escaping_Energy * abs(
                        Rabbit_Location - X[i, :]
                    )

                if (
                        r >= 0.5 and abs(Escaping_Energy) >= 0.5
                ):  # Soft besiege Eq. (4) in paper
                    Jump_strength = 2 * (
                            1 - random.random()
                    )  # random jump strength of the rabbit
                    X[i, :] = (Rabbit_Location - X[i, :]) - Escaping_Energy * abs(
                        Jump_strength * Rabbit_Location - X[i, :]
                    )

                # phase 2: --------performing team rapid dives (leapfrog movements)----------

                if (
                        r < 0.5 and abs(Escaping_Energy) >= 0.5
                ):  # Soft besiege Eq. (10) in paper
                    # rabbit try to escape by many zigzag deceptive motions
                    Jump_strength = 2 * (1 - random.random())
                    X1 = Rabbit_Location - Escaping_Energy * abs(
                        Jump_strength * Rabbit_Location - X[i, :]
                    )
                    # X1 = numpy.clip(X1, lb, ub)

                    if objf(generate_unstable_solution(X1, lb, ub), distances) < fitness:  # improved move?
                        X[i, :] = X1.copy()
                    else:  # hawks perform levy-based short rapid dives around the rabbit
                        X2 = (
                                Rabbit_Location
                                - Escaping_Energy
                                * abs(Jump_strength * Rabbit_Location - X[i, :])
                                + numpy.multiply(numpy.random.randn(dim), Levy(dim))
                        )
                        # X2 = numpy.clip(X2, lb, ub)
                        if objf(generate_unstable_solution(X2, lb, ub), distances) < fitness:
                            X[i, :] = X2.copy()
                if (
                        r < 0.5 and abs(Escaping_Energy) < 0.5
                ):  # Hard besiege Eq. (11) in paper
                    Jump_strength = 2 * (1 - random.random())
                    X1 = Rabbit_Location - Escaping_Energy * abs(
                        Jump_strength * Rabbit_Location - X.mean(0)
                    )
                    # X1 = numpy.clip(X1, lb, ub)

                    if objf(generate_unstable_solution(X1, lb, ub), distances) < fitness:  # improved move?
                        X[i, :] = X1.copy()
                    else:  # Perform levy-based short rapid dives around the rabbit
                        X2 = (
                                Rabbit_Location
                                - Escaping_Energy
                                * abs(Jump_strength * Rabbit_Location - X.mean(0))
                                + numpy.multiply(numpy.random.randn(dim), Levy(dim))
                        )
                        # X2 = numpy.clip(X2, lb, ub)
                        if objf(generate_unstable_solution(X2, lb, ub), distances) < fitness:
                            X[i, :] = X2.copy()

        convergence_curve[t] = Rabbit_Energy
        if t % 1 == 0:
            print(
                [
                    "At iteration "
                    + str(t)
                    + " the best fitness is "
                    + str(Rabbit_Energy)
                ]
            )
        t = t + 1

    timerEnd = time.time()
    s.endTime = time.strftime("%Y-%m-%d-%H-%M-%S")
    s.executionTime = timerEnd - timerStart
    s.convergence = convergence_curve
    s.optimizer = "HHO"
    s.objfname = objf.__name__
    s.best = Rabbit_Energy
    s.bestIndividual = Rabbit_Location

    return s


def Levy(dim):
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


def generate_stable_solution(s, lb=None, ub=None):
    # Bring them back to boundary
    s = numpy.clip(s, lb, ub)

    solution_set = set(list(range(lb[0], len(s))))
    solution_done = numpy.array([-1, ] * len(s))
    solution_int = s.astype(int)
    city_unique, city_counts = numpy.unique(solution_int, return_counts=True)

    # Way 1: Stable, not random
    for idx, city in enumerate(solution_int):
        if solution_done[idx] != -1:
            continue
        if city in city_unique:
            solution_done[idx] = city
            city_unique = numpy.where(city_unique == city, -1, city_unique)
        else:
            list_cities_left = list(solution_set - set(city_unique) - set(solution_done))
            # print(list_cities_left)
            solution_done[idx] = list_cities_left[0]
    # print(f"What: {solution_done}")
    return solution_done


def generate_unstable_solution(s, lb=None, ub=None):
    # print(solution)
    solution_bound = numpy.clip(s, lb, ub)
    solution_set = set(range(int(lb[0]), round(ub[0])))
    solution_done = numpy.array([-1, ] * len(solution_bound))
    solution_int = solution_bound.astype(int)
    # print(solution_int)
    city_unique, city_counts = numpy.unique(solution_int, return_counts=True)

    # Way 2: Random, not stable
    # count_dict = dict(zip(*numpy.unique(solution_int, return_counts=True)))
    count_dict = dict(zip(city_unique, city_counts))
    for idx, city in enumerate(solution_int):
        if solution_done[idx] != -1:
            continue
        if city in city_unique:
            if city in (solution_set - set(solution_done)):
                if count_dict[city] == 1:
                    solution_done[idx] = city
                else:
                    idx_list_city = numpy.where(solution_int == city)[0]
                    idx_city_keep = numpy.random.choice(idx_list_city)
                    solution_done[idx_city_keep] = city
                    if idx_city_keep != idx:
                        solution_done[idx] = numpy.random.choice(
                            list(solution_set - set(solution_done) - set(city_unique)))
            else:
                solution_done[idx] = numpy.random.choice(list(solution_set - set(solution_done) - set(city_unique)))
        else:
            solution_done[idx] = numpy.random.choice(list(solution_set - set(solution_done) - set(city_unique)))
    # print(solution_done)
    return solution_done
