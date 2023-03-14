import time
from pathlib import Path


class Parameter:
    results_directory = "out/" + time.strftime("%Y-%m-%d-%H-%M-%S") + "/"
    optimizers = ["HHO"]

    def __init__(self, n_runs, population, iteration, instances, results_directory=None, optimizers=None):
        self.n_runs = n_runs
        self.population = population
        self.iteration = iteration
        self.instances = instances

        if optimizers is not None:
            self.optimizers = optimizers

        if results_directory is not None:
            self.results_directory = results_directory

        Path(self.results_directory).mkdir(parents=True, exist_ok=True)
