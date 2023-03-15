import math
import random
import numpy as np

import method.extra.mutate as mutate
from method.extra.crossover import pmx
from method.extra.encode import random_key
from method.extra.local_search import two_opt_inverse
from method.extra.local_search import two_opt_cvrp_inverse
from method.extra.local_search import two_opt_cvrp_insertion

from model.solution import Solution
from controller.benchmarks import concat_depot
from controller.benchmarks import normal_cvrp
from controller.benchmarks import split_customer


class HHOCVRP:
    """Harris Hawks Optimization class modified for Capacitated Vehicle Routing Problem"""

    t = 0

    def __init__(
            self,
            objf,
            iteration: int,
            population: int,
            data
    ):
        self.objf = objf
        self.iteration = iteration
        self.population = population
        self.escaping_energy = 0

        self.lb = 1
        self.ub = data.n_customers
        self.capacity = data.capacity
        self.dimension = data.n_customers
        self.distance = data.distances
        self.demands = data.demands

        self.hawks = np.zeros(self.dimension)
        self.rabbit_location = np.zeros(self.dimension)
        self.best_route = None
        self.test_route = []

        self.rabbit_energy = float("inf")
        self.hawks_fitness = [float("inf") for _ in range(self.population)]

    def initiate_population(self):
        """
        This function create a randomized array with size of population x dimension

        Returns
        -------
        N/
        """

        self.hawks = np.array(
            [
                x * (self.ub - self.lb) + self.lb
                for x in np.random.uniform(0, 1, (self.population, self.dimension))
            ]
        )

    def check_solution(self, solution: Solution):
        """
        This function stop iteration process if current best solution has
        reached the best known solution, then the convergence curve will be filled
        with bks

        Returns
        -------
        N/A
        """

        if self.rabbit_energy <= solution.bks:
            solution.convergence = [
                self.rabbit_energy if conv == 0 else conv for conv in solution.convergence
            ]
            self.t = self.iteration

    def determine_rabbit(self):
        """
        This function is setter for the rabbit at the start of hho-cvrp

        Returns
        -------
        N/A
        """

        for i in range(0, self.population):

            # Update the location of Hawks
            self.hawks[i, :] = random_key(self.hawks[i, :])
            self.hawks_fitness[i] = self.objf(self.hawks[i, :].astype(int), self.distance, self.capacity, self.demands)

            # Update the location of Rabbit
            if self.hawks_fitness[i] < self.rabbit_energy:  # Change this to > for maximization problem
                self.rabbit_energy = self.hawks_fitness[i]
                self.rabbit_location = self.hawks[i, :].copy()

    def update_location(self, t: int):
        """
        Update the location of Hawks and Rabbit

        Parameters
        ----------
        t : int
            current iteration number

        Returns
        -------
        N/A
        """

        for i in range(0, self.population):
            # -------- Finishing phase at last iteration ----
            if self.t == self.iteration - 1:
                self.finishing_phase(i)

            self.hawks_fitness[i] = self.objf(
                self.hawks[i, :].astype(int), self.distance, self.capacity, self.demands
            ) if t < self.iteration - 1 else normal_cvrp(self.test_route, self.distance)

            # Update the location of Rabbit
            if self.hawks_fitness[i] < self.rabbit_energy:  # Change this to > for maximization problem
                self.rabbit_energy = self.hawks_fitness[i]
                self.rabbit_location = self.hawks[i, :].copy()

                if t == self.iteration - 1:
                    self.best_route = self.test_route

    def update_escaping_energy(self):
        """
        Escaping energy of rabbit

        Returns
        -------
        N/A
        """

        self.escaping_energy = 2 * (2 * random.random() - 1) * (1 - (self.t / self.iteration))

    def run(self, solution: Solution):
        """
        This function is Harris Hawks Optimization for CVRP.

        Returns
        -------
        N/A
        """

        # Initialize convergence
        solution.convergence = np.zeros(self.iteration)

        print('HHO is now tackling "' + self.objf.__name__ + '" ' + solution.name)

        self.initiate_population()

        solution.start_timer()

        self.determine_rabbit()

        # Main loop
        while self.t < self.iteration:
            for i in range(0, self.population):
                self.update_escaping_energy()

                # -------- Exploration phase --------------------
                if abs(self.escaping_energy) >= 1:
                    self.exploration(i)

                # -------- Exploitation phase -------------------
                elif abs(self.escaping_energy) < 1:
                    self.exploitation(i)

            self.update_location(self.t)

            solution.convergence[self.t] = self.rabbit_energy
            if self.t % 1 == 0:
                print("At iteration " + str(self.t) + " the best fitness is " + str(self.rabbit_energy))
            self.t += 1

            self.check_solution(solution)

        solution.stop_timer()
        solution.objfname = self.objf.__name__
        solution.best = self.rabbit_energy
        solution.best_individual = self.rabbit_location
        solution.routes = self.best_route if self.best_route is not None else split_customer(
            self.rabbit_location.astype(int), self.capacity, self.demands)

    def exploration(self, i: int):
        """
        Perching strategy divided into 2 strategies based on q

        Parameters
        ----------
        i : int
            index of current hawk

        Returns
        -------
        N/A
        """

        q = random.random()
        rand_hawk_index = math.floor(self.population * random.random())
        rand_hawk = self.hawks[rand_hawk_index, :]

        if q >= 0.5:
            self.perching_based_on_random_location(i, rand_hawk)
        elif q < 0.5:
            self.perching_based_on_the_position_of_other_hawks(i)

    def exploitation(self, i: int):
        """
        Attacking the rabbit using 4 strategies regarding the behavior of the rabbit

        Parameters
        ----------
        i : int
            index of current hawk

        Returns
        -------
        N/A
        """

        r = random.random()  # probability of each event

        # phase 1: ----- surprise pounce (seven kills) ----------
        # surprise pounce (seven kills): multiple, short rapid dives by different hawks
        if r >= 0.5 and abs(self.escaping_energy) >= 0.5:
            self.soft_besiege(i)
        if r >= 0.5 > abs(self.escaping_energy):
            self.hard_besiege(i)

        # phase 2: --------performing team rapid dives (leapfrog movements)----------
        if r < 0.5 <= abs(self.escaping_energy):
            self.soft_besiege_with_progressive_rapid_dives(i)
        if r < 0.5 and abs(self.escaping_energy) < 0.5:
            self.hard_besiege_with_progressive_rapid_dives(i)

    def perching_based_on_random_location(self, i, rand_hawk):
        """
        Perching based on random location

        Parameters
        ----------
        i : int
            current index of hawks
        rand_hawk :
            a randomly selected hawk
        """

        self.hawks[i, :] = rand_hawk - random.random() * abs(
            rand_hawk - 2 * random.random() * self.hawks[i, :]
        )
        self.hawks[i, :] = mutate.swap(random_key(self.hawks[i, :]))

    def perching_based_on_the_position_of_other_hawks(self, i):
        """
        Perching based on the position of other hawks

        Parameters
        ----------
        i : int
            current index of hawks
        """

        self.hawks[i, :] = (self.rabbit_location - self.hawks.mean(0)) - random.random() * (
                (self.ub - self.lb) * random.random() + self.lb
        )
        self.hawks[i, :] = mutate.inverse(random_key(self.hawks[i, :]))

    def soft_besiege(self, i):
        """
        Soft besiege

        Parameters
        ----------
        i : int
            current index of hawks
        """

        jump_strength = 2 * (1 - random.random())
        self.hawks[i, :] = (self.rabbit_location - self.hawks[i, :]) - self.escaping_energy * abs(
            jump_strength * self.rabbit_location - self.hawks[i, :]
        )
        self.hawks[i, :] = mutate.swap(random_key(self.hawks[i, :]))

    def hard_besiege(self, i: int):
        """
        Hard besiege

        Parameters
        ----------
        i : int
            current index of hawks
        """

        self.hawks[i, :] = self.rabbit_location - self.escaping_energy * abs(
            self.rabbit_location - self.hawks[i, :]
        )
        self.hawks[i, :] = mutate.swap(random_key(self.hawks[i, :]))

    def soft_besiege_with_progressive_rapid_dives(self, i: int):
        """
        Soft besiege with progressive rapid dives

        Parameters
        ----------
        i : int
            current index of hawks
        """

        jump_strength = 2 * (1 - random.random())
        x1 = self.rabbit_location - self.escaping_energy * abs(
            jump_strength * self.rabbit_location - self.hawks[i, :]
        )
        x1 = mutate.swap(random_key(x1))
        x1, x2 = pmx(random_key(self.rabbit_location), x1)

        xo1 = self.objf(x1, self.distance, self.capacity, self.demands)
        xo2 = self.objf(x2, self.distance, self.capacity, self.demands)

        yobjf = xo1 if xo1 < xo2 else xo2
        y = x1 if xo1 < xo2 else x2

        if yobjf < self.hawks_fitness[i]:  # improved move?
            self.hawks[i, :] = np.array(y).copy()
        else:
            x2 = (
                    self.rabbit_location
                    - self.escaping_energy
                    * abs(jump_strength * self.rabbit_location - self.hawks[i, :])
                    + np.multiply(np.random.randn(self.dimension), self.levy())
            )
            x2 = mutate.insertion(random_key(x2))
            x2 = two_opt_inverse(concat_depot(x2), self.distance)[1:-1]

            if self.objf(x2, self.distance, self.capacity, self.demands) < self.hawks_fitness[i]:
                self.hawks[i, :] = x2.copy()

    def hard_besiege_with_progressive_rapid_dives(self, i):
        """
        Hard besiege with progressive rapid dives

        Parameters
        ----------
        i : int
            current index of hawks
        """

        jump_strength = 2 * (1 - random.random())
        x1 = self.rabbit_location - self.escaping_energy * abs(
            jump_strength * self.rabbit_location - self.hawks.mean(0)
        )
        x1 = mutate.inverse(random_key(x1))

        if self.objf(x1, self.distance, self.capacity, self.demands) < self.hawks_fitness[i]:
            self.hawks[i, :] = x1.copy()
        else:
            x2 = (
                    self.rabbit_location
                    - self.escaping_energy
                    * abs(jump_strength * self.rabbit_location - self.hawks.mean(0))
                    + np.multiply(np.random.randn(self.dimension), self.levy())
            )
            x2 = mutate.insertion(random_key(x2))

            if self.objf(x2, self.distance, self.capacity, self.demands) < self.hawks_fitness[i]:
                self.hawks[i, :] = x2.copy()

    def finishing_phase(self, i: int):
        """
        Finishing phase

        Parameters
        ----------
        i : int
            current index of hawks
        """

        self.test_route = split_customer(random_key(self.hawks[i, :]), self.capacity, self.demands)
        self.test_route = two_opt_cvrp_inverse(self.test_route, self.distance)
        self.test_route = two_opt_cvrp_insertion(self.test_route, self.distance)

    def levy(self):
        """
        This function is a Lévy flight function.

        Returns
        -------
        step :
            value of Lévy flight
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

    def extend_bound(self):
        """
        This function extend lower bound and upper bound into a list

        Returns
        -------
        N/A
        """

        if not isinstance(self.lb, list):
            self.lb = [self.lb for _ in range(self.dimension)]
            self.ub = [self.ub for _ in range(self.dimension)]
        self.lb = np.array(self.lb)
        self.ub = np.array(self.ub)
