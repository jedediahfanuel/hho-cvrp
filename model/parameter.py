import time
from pathlib import Path


class Parameter:
    results_directory = "hho_cvrp_result/" + time.strftime("%Y-%m-%d-%H-%M-%S") + "/"
    optimizers = ["HHOCVRP"]

    def __init__(self, n_runs, population, iteration, instances, city_size, city_id, results_directory="", optimizers=None):
        self.n_runs = n_runs
        self.population = population
        self.iteration = iteration
        self.instances = instances
        self.city_size = city_size,
        self.city_id = city_id

        if optimizers is not None:
            self.optimizers = optimizers

        if results_directory != "":
            self.results_directory = results_directory + "/hho_cvrp_result/" + time.strftime("%Y-%m-%d-%H-%M-%S") + "/"
        else:
            self.results_directory = "hho_cvrp_result/" + time.strftime("%Y-%m-%d-%H-%M-%S") + "/"

        Path(self.results_directory).mkdir(parents=True, exist_ok=True)
