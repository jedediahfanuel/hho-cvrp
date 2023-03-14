import warnings

import controller.benchmarks as benchmarks
from method.hho_cvrp import hho
from model.collection import Collection
from model.export import Export
from model.parameter import Parameter

warnings.simplefilter(action="ignore")


def selector(algo, func_details, params):
    """

    Parameters
    ----------
    algo : list of str
        list of algorithm used to solve the problem
    func_details : list
        Contain name of objective function, instance, and solution
    params : Parameter
        Collection of configurable user parameter

    Returns
    -------
    x : Solution Class
        Solution class that include much information about optimizer process result
    """

    function_name = func_details[0]
    instance = func_details[1]
    solution = func_details[2]

    if algo == "HHO":
        solution = hho(getattr(benchmarks, function_name), instance, solution, params.population, params.iteration)
    else:
        return None
    return solution


def run(params: Parameter, export: Export):
    """
    It serves as the main interface of the framework for running the experiments.

    Parameters
    ----------
    params : Parameter
        collection of configurable user parameter
    export : Export
        the set of Boolean flags which are:
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

    for i, optimizer_name in enumerate(params.optimizers):
        for instance_name in params.instances:
            collection = Collection(params.n_runs)
            for k in range(params.n_runs):
                func_details = benchmarks.get_function_details(instance_name)
                solution = selector(optimizer_name, func_details, params)
                collection.convergence[k] = solution.convergence

                if export.details:
                    export.write_detail(collection, solution, params, k)

                if export.route:
                    export.write_route(solution, params, k)

                if export.scatter:
                    export.write_scatter(solution, params, k) if solution.coordinates is not None else ()

            if export.avg:
                export.write_avg(collection, solution, params)

    if export.convergence:
        export.write_convergence(params)

    if export.boxplot:
        export.write_boxplot(params)

    if export.configuration:
        export.write_configuration(params)

    print("Execution completed")
