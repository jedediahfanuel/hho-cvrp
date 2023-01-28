import random
import numpy
import math
from solution import Solution
import time
import generate


def HHO(objf, lb, ub, instance, SearchAgents_no, Max_iter):
    dim = (
        generate.n_vehicle(instance.name),
        instance.dimension,
        instance.dimension
    )

    # initialize the location and Energy of the rabbit
    Rabbit_Location = numpy.zeros(dim)
    Rabbit_Energy = float("inf")  # change this to -inf for maximization problems

    if not isinstance(lb, list):
        lb = numpy.full(dim[1:], lb)
        ub = numpy.full(dim[1:], ub)

    # Initialize the locations of Harris hawks || 4D Array
    X = numpy.asarray([ generate.get_binary(
        generate.initial_solution(
            instance.n_customers,
            generate.n_vehicle(instance.name),
            instance.capacity,
            instance.demands
        ), instance.dimension
    ) for _ in range(SearchAgents_no)])

    # Initialize convergence
    convergence_curve = numpy.zeros(Max_iter)

    ############################
    s = Solution()

    print('HHO is now tackling  "' + objf.__name__ + '" ' + instance.name)

    timerStart = time.time()
    s.start_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    ############################

    t = 0  # Loop counter

    # Main loop
    while t < Max_iter:
        for i in range(0, SearchAgents_no):

            # Check boundaries

            X[i, :] = numpy.clip(X[i, :], lb, ub)

            # fitness of locations
            fitness = objf(generate.get_route(X[i, :]), instance.distances)

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
                    X1 = numpy.clip(X1, lb, ub)

                    if objf(generate.get_route(X1), instance.distances) < fitness:  # improved move?
                        X[i, :] = X1.copy()
                    else:  # hawks perform levy-based short rapid dives around the rabbit
                        X2 = (
                                Rabbit_Location
                                - Escaping_Energy
                                * abs(Jump_strength * Rabbit_Location - X[i, :])
                                + numpy.multiply(numpy.random.randn(*dim), Levy(dim))
                        )
                        X2 = numpy.clip(X2, lb, ub)
                        if objf(generate.get_route(X2), instance.distances) < fitness:
                            X[i, :] = X2.copy()
                if (
                        r < 0.5 and abs(Escaping_Energy) < 0.5
                ):  # Hard besiege Eq. (11) in paper
                    Jump_strength = 2 * (1 - random.random())
                    X1 = Rabbit_Location - Escaping_Energy * abs(
                        Jump_strength * Rabbit_Location - X.mean(0)
                    )
                    X1 = numpy.clip(X1, lb, ub)

                    if objf(generate.get_route(X1), instance.distances) < fitness:  # improved move?
                        X[i, :] = X1.copy()
                    else:  # Perform levy-based short rapid dives around the rabbit
                        X2 = (
                                Rabbit_Location
                                - Escaping_Energy
                                * abs(Jump_strength * Rabbit_Location - X.mean(0))
                                + numpy.multiply(numpy.random.randn(*dim), Levy(dim))
                        )
                        X2 = numpy.clip(X2, lb, ub)
                        if objf(generate.get_route(X2), instance.distances) < fitness:
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
    s.end_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    s.execution_time = timerEnd - timerStart
    s.convergence = convergence_curve
    s.optimizer = "HHO"
    s.objfname = objf.__name__
    s.best = Rabbit_Energy
    s.best_individual = Rabbit_Location

    return s


def Levy(dim):
    beta = 1.5
    sigma = (
                    math.gamma(1 + beta)
                    * math.sin(math.pi * beta / 2)
                    / (math.gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))
            ) ** (1 / beta)
    u = 0.01 * numpy.random.randn(*dim) * sigma
    v = numpy.random.randn(*dim)
    zz = numpy.power(numpy.absolute(v), (1 / beta))
    step = numpy.divide(u, zz)
    return step
