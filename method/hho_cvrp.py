import time
import random
import math
import numpy as np

import method.mutate as mutate
from method.crossover import pmx
from method.encode import random_key
from method.local_search import cvrp_inverse
from method.local_search import cvrp_insertion
from method.local_search import two_opt_inverse

from model.solution import Solution
from controller.benchmarks import concat_depot
from controller.benchmarks import normal_cvrp
from controller.benchmarks import split_customer


class HarrisHawksOptimization:
    def __init__(
            self,
            objf,
            iteration: int,
            population: int,
            bks,
            data
    ):
        self.objf = objf
        self.iteration = iteration
        self.population = population

        self.bks = bks
        self.lb = 1
        self.ub = data.n_customers
        self.capacity = data.capacity
        self.dimension = data.n_customers
        self.distance = data.distances
        self.demands = data.demands
        self.coordinates = data.coordinates  # ?
        self.problem_name = data.name  # ?

        self.hawks = np.zeros(self.dimension)
        self.rabbit_location = np.zeros(self.dimension)
        self.best_route = None
        self.test_route = []

        self.rabbit_energy = float("inf")
        self.hawks_fitness = [float("inf") for _ in range(self.population)]

    def initiate_population(self):
        self.hawks = np.array(
            [
                x * (self.ub - self.lb) + self.lb
                for x in np.random.uniform(0, 1, (self.population, self.dimension))
            ]
        )

    def run(self):
        """
        This function is Harris Hawks Optimization for CVRP.

        Returns
        -------
        s : Solution
            a local defined solution class (check solution.py)
        """

        # lb, ub, dim, distances = 1, data.n_customers, data.n_customers, data.distances
        # max_capacity, demands = data.capacity, data.demands
        # best_route, bks = None, sol.cost

        # initialize the location and Energy of the rabbit

        # change this to -inf for maximization problems
        # rabbit_energy = float("inf")
        # fs = [float("inf") for _ in range(search_agent_no)]

        # if not isinstance(lb, list):
        #     lb = [lb for _ in range(dim)]
        #     ub = [ub for _ in range(dim)]
        # lb = np.array(lb)
        # ub = np.array(ub)

        # Initialize the locations of Harris' hawks
        self.initiate_population()

        # Initialize convergence
        convergence_curve = np.zeros(self.iteration)

        ############################
        s = Solution()

        print('HHO is now tackling "' + self.objf.__name__ + '" ' + self.problem_name)

        timer_start = time.time()
        s.start_time = time.strftime("%Y-%m-%d-%H-%M-%S")
        ############################

        t = 0  # Loop counter

        for i in range(0, self.population):

            # fitness of locations
            self.hawks[i, :] = random_key(self.hawks[i, :])
            fitness = self.objf(self.hawks[i, :].astype(int), self.distance, self.capacity, self.demands)
            self.hawks_fitness[i] = fitness

            # Update the location of Rabbit
            if fitness < self.rabbit_energy:  # Change this to > for maximization problem
                self.rabbit_energy = fitness
                self.rabbit_location = self.hawks[i, :].copy()

        # Main loop
        while t < self.iteration:
            e1 = 2 * (1 - (t / self.iteration))  # factor to show the decreasing energy of rabbit

            # Update the location of Harris' hawks
            for i in range(0, self.population):

                e0 = 2 * random.random() - 1  # -1 < e0 < 1
                escaping_energy = e1 * (
                    e0
                )  # escaping energy of rabbit Eq. (3) in the paper

                # -------- Exploration phase Eq. (1) in paper -------------------

                if abs(escaping_energy) >= 1:
                    # Harris' hawks perch randomly based on 2 strategy:
                    q = random.random()
                    rand_hawk_index = math.floor(self.population * random.random())
                    x_rand = self.hawks[rand_hawk_index, :]
                    if q >= 0.5:
                        # perch based on other family members
                        self.hawks[i, :] = x_rand - random.random() * abs(
                            x_rand - 2 * random.random() * self.hawks[i, :]
                        )
                        self.hawks[i, :] = mutate.swap(random_key(self.hawks[i, :]))

                    elif q < 0.5:
                        # perch on a random tall tree (random site inside group's home range)
                        self.hawks[i, :] = (self.rabbit_location - self.hawks.mean(0)) - random.random() * (
                                (self.ub - self.lb) * random.random() + self.lb
                        )
                        self.hawks[i, :] = mutate.inverse(random_key(self.hawks[i, :]))

                # -------- Exploitation phase -------------------
                elif abs(escaping_energy) < 1:
                    # Attacking the rabbit using 4 strategies regarding the behavior of the rabbit

                    # phase 1: ----- surprise pounce (seven kills) ----------
                    # surprise pounce (seven kills): multiple, short rapid dives by different hawks

                    r = random.random()  # probability of each event

                    if (
                            r >= 0.5 > abs(escaping_energy)
                    ):  # Hard besiege Eq. (6) in paper
                        self.hawks[i, :] = self.rabbit_location - escaping_energy * abs(
                            self.rabbit_location - self.hawks[i, :]
                        )
                        self.hawks[i, :] = mutate.swap(random_key(self.hawks[i, :]))

                    if (
                            r >= 0.5 and abs(escaping_energy) >= 0.5
                    ):  # Soft besiege Eq. (4) in paper
                        jump_strength = 2 * (
                                1 - random.random()
                        )  # random jump strength of the rabbit
                        self.hawks[i, :] = (self.rabbit_location - self.hawks[i, :]) - escaping_energy * abs(
                            jump_strength * self.rabbit_location - self.hawks[i, :]
                        )
                        self.hawks[i, :] = mutate.swap(random_key(self.hawks[i, :]))

                    # phase 2: --------performing team rapid dives (leapfrog movements)----------

                    if (
                            r < 0.5 <= abs(escaping_energy)
                    ):  # Soft besiege Eq. (10) in paper
                        # rabbit try to escape by many zigzag deceptive motions
                        jump_strength = 2 * (1 - random.random())
                        x1 = self.rabbit_location - escaping_energy * abs(
                            jump_strength * self.rabbit_location - self.hawks[i, :]
                        )
                        x1 = mutate.swap(random_key(x1))
                        x1, x2 = pmx(
                            random_key(self.rabbit_location),
                            x1
                        )

                        xo1 = self.objf(x1, self.distance, self.capacity, self.demands)
                        xo2 = self.objf(x2, self.distance, self.capacity, self.demands)

                        yobjf = xo1 if xo1 < xo2 else xo2
                        y = x1 if xo1 < xo2 else x2

                        if yobjf < self.hawks_fitness[i]:  # improved move?
                            self.hawks[i, :] = np.array(y).copy()
                        else:  # hawks perform levy-based short rapid dives around the rabbit
                            x2 = (
                                    self.rabbit_location
                                    - escaping_energy
                                    * abs(jump_strength * self.rabbit_location - self.hawks[i, :])
                                    + np.multiply(np.random.randn(self.dimension), self.levy())
                            )
                            x2 = mutate.insertion(random_key(x2))
                            x2 = two_opt_inverse(concat_depot(x2), self.distance)[1:-1]

                            if self.objf(x2, self.distance, self.capacity, self.demands) < self.hawks_fitness[i]:
                                self.hawks[i, :] = x2.copy()
                    if (
                            r < 0.5 and abs(escaping_energy) < 0.5
                    ):  # Hard besiege Eq. (11) in paper
                        jump_strength = 2 * (1 - random.random())
                        x1 = self.rabbit_location - escaping_energy * abs(
                            jump_strength * self.rabbit_location - self.hawks.mean(0)
                        )
                        x1 = mutate.inverse(random_key(x1))

                        if self.objf(x1, self.distance, self.capacity, self.demands) < self.hawks_fitness[i]:
                            self.hawks[i, :] = x1.copy()
                        else:  # Perform levy-based short rapid dives around the rabbit
                            x2 = (
                                    self.rabbit_location
                                    - escaping_energy
                                    * abs(jump_strength * self.rabbit_location - self.hawks.mean(0))
                                    + np.multiply(np.random.randn(self.dimension), self.levy())
                            )
                            x2 = mutate.insertion(random_key(x2))

                            if self.objf(x2, self.distance, self.capacity, self.demands) < self.hawks_fitness[i]:
                                self.hawks[i, :] = x2.copy()

            for i in range(0, self.population):

                # fitness of locations
                if t == self.iteration - 1:
                    # Finishing Phase
                    self.test_route = split_customer(random_key(self.hawks[i, :]), self.capacity, self.demands)
                    self.test_route = cvrp_inverse(self.test_route, self.distance)
                    self.test_route = cvrp_insertion(self.test_route, self.distance)

                fitness = self.objf(self.hawks[i, :].astype(int), self.distance, self.capacity, self.demands
                                    ) if t < self.iteration - 1 else normal_cvrp(self.test_route, self.distance)
                self.hawks_fitness[i] = fitness

                # Update the location of Rabbit
                if fitness < self.rabbit_energy:  # Change this to > for maximization problem
                    self.rabbit_energy = fitness
                    self.rabbit_location = self.hawks[i, :].copy()

                    if t == self.iteration - 1:
                        self.best_route = self.test_route

            convergence_curve[t] = self.rabbit_energy
            if t % 1 == 0:
                print(
                    "At iteration " + str(t) + " the best fitness is " + str(self.rabbit_energy)
                )
            t = t + 1

            # stop iteration if bks is reached, fill convergence with bks
            if self.rabbit_energy <= self.bks:
                convergence_curve = [self.rabbit_energy if conv == 0 else conv for conv in convergence_curve]
                break

        timer_end = time.time()
        s.end_time = time.strftime("%Y-%m-%d-%H-%M-%S")
        s.execution_time = timer_end - timer_start
        s.convergence = convergence_curve
        s.optimizer = "HHO"
        s.objfname = self.objf.__name__
        s.bks = self.bks
        s.best = self.rabbit_energy
        s.best_individual = self.rabbit_location
        s.name = self.problem_name
        s.routes = self.best_route if self.best_route is not None else split_customer(
            self.rabbit_location.astype(int), self.capacity, self.demands)
        s.dim = self.dimension
        s.coordinates = self.coordinates

        return s

    def levy(self):
        """
        This function is a Lévy flight function.
    
        :return: value of Lévy flight
        """
        beta = 1.5
        sigma = (
                        math.gamma(1 + beta) * math.sin(math.pi * beta / 2)
                        / (math.gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))
                ) ** (1 / beta)
        u = 0.01 * np.random.randn(self.dimension) * sigma
        v = np.random.randn(self.dimension)
        zz = np.power(np.absolute(v), (1 / beta))
        step = np.divide(u, zz)
        return step
