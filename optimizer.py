import csv
import time
import warnings
from pathlib import Path

import numpy

import benchmarks
from optimizers.hho_cvrp import hho
from model.collection import Collection
from model.export import Export
import plot_boxplot as box_plot
import plot_convergence as conv_plot
import plot_scatter as scatter_plot
import write_configuration
import write_details
import write_routes

warnings.simplefilter(action="ignore")


def selector(algo, func_details, pop_size, n_iter):
    """

    Parameters
    ----------
    algo : list of str
        list of algorithm used to solve the problem
    func_details : list
        Contain name of objective function, instance, and solution
    pop_size : int
        population size for each algorithm
    n_iter : int
        number of iteration for each algorithm

    Returns
    -------
    x : Solution Class
        Solution class that include much information about optimizer process result
    """

    function_name = func_details[0]
    instance = func_details[1]
    solution = func_details[2]

    if algo == "HHO":
        x = hho(getattr(benchmarks, function_name), instance, solution, pop_size, n_iter)
    else:
        return None
    return x


def run(optimizer, instances, num_of_runs, params: dict[str, int], export: Export):
    """
    It serves as the main interface of the framework for running the experiments.

    Parameters
    ----------
    optimizer : list
        The list of optimizers names
    instances : list
        The list of benchmark instances
    num_of_runs : int
        The number of independent runs
    params  : set
        The set of parameters which are:
        1. Size of population (population_size)
        2. The number of iterations (iterations)
    export : Export
        The set of Boolean flags which are:
        1. export.avg (Exporting the results in a file)
        2. export.boxplot (Exporting the box plots)
        3. export.configuration: (Exporting the configuration of current test)
        4. export.convergence (Exporting the convergence plots)
        5. export.details (Exporting the detailed results in files)
        6. export.route (Exporting the routes for each iteration)
        7. export.scatter (Exporting the scatter plots)

    Returns
    -----------
    N/A
    """

    # Select general parameters for all optimizers (population size, number of iterations) ....
    population_size = params["population_size"]
    iterations = params["iterations"]

    flag = False

    # CSV Header for the convergence
    cnvg_header = []

    results_directory = "out/" + time.strftime("%Y-%m-%d-%H-%M-%S") + "/"
    Path(results_directory).mkdir(parents=True, exist_ok=True)

    for it in range(0, iterations):
        cnvg_header.append("Iter" + str(it + 1))

    for i in range(0, len(optimizer)):
        for j in range(0, len(instances)):
            collection = Collection(num_of_runs)
            for k in range(0, num_of_runs):
                func_details = benchmarks.get_function_details(instances[j])
                solution = selector(optimizer[i], func_details, population_size, iterations)
                collection.convergence[k] = solution.convergence

                if export.details:
                    export_to_file = results_directory + "experiment_details.csv"
                    write_details.run(export_to_file, collection, solution, cnvg_header, k)

                if export.route:
                    rd = results_directory + "routes-" + solution.optimizer + "/" + solution.name + "/"
                    Path(rd).mkdir(parents=True, exist_ok=True)
                    write_routes.run(solution, rd, k)

                if export.scatter:
                    close = "/" if solution.coordinates is not None else "/None"
                    rd = results_directory + "scatter-plot-" + solution.optimizer + "/" + solution.name + close
                    Path(rd).mkdir(parents=True, exist_ok=True)

                    scatter_plot.run(solution, rd, k) if solution.coordinates is not None else ()

            if export.avg:
                export_to_file = results_directory + "experiment_avg.csv"

                with open(export_to_file, "a", newline="\n") as out:
                    writer = csv.writer(out, delimiter=",")
                    if not flag:
                        # just one time to write the header of the CSV file
                        header = numpy.concatenate(
                            [["Optimizer", "Instance", "BKS", "BS", "Gap", "ExecutionTime"], cnvg_header]
                        )
                        writer.writerow(header)
                        flag = True

                    avg_execution_time = float("%0.2f" % (sum(collection.execution_time) / num_of_runs))
                    avg_bs = float("%0.2f" % (sum(collection.best_solution) / num_of_runs))
                    avg_gap = float("%0.4f" % (sum(collection.gap_solution) / num_of_runs))
                    avg_convergence = numpy.around(
                        numpy.mean(collection.convergence, axis=0, dtype=numpy.float64), decimals=2
                    ).tolist()
                    a = numpy.concatenate(
                        [
                            [
                                solution.optimizer,
                                solution.name,
                                solution.bks,
                                avg_bs,
                                avg_gap,
                                avg_execution_time
                            ],
                            avg_convergence
                        ]
                    )
                    writer.writerow(a)
                out.close()

    if export.convergence:
        rd = results_directory + "convergence-plot/"
        Path(rd).mkdir(parents=True, exist_ok=True)
        conv_plot.run(rd, optimizer, instances, iterations)

    if export.boxplot:
        rd = results_directory + "box-plot/"
        Path(rd).mkdir(parents=True, exist_ok=True)
        box_plot.run(rd, optimizer, instances, iterations)

    if export.configuration:
        export_to_file = results_directory + "configuration.txt"
        write_configuration.run(export_to_file, num_of_runs, population_size, iterations, instances)

    if not flag:  # Failed to run at least one experiment
        print(
            "No Optimizer or Cost function is selected. Check lists of available optimizers and cost functions"
        )

    print("Execution completed")
