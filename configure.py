from model.export import Export
from optimizer import run


def conf(num, pop, iterate, names):
    """
    Parameter configuration

    Parameters
    ----------
    num : int
        number of run
    pop : int
        population size
    iterate : int
        number of iteration
    names : list of str
        list of instance name to be tested

    Returns
    -------
    N/A
    """

    # Select optimizers
    optimizer = ["HHO"]

    # Select benchmark function
    instances = names

    # Select number of repetitions for each experiment.
    # To obtain meaningful statistical results, usually 30 independent runs are executed for each algorithm.
    num_of_runs = num

    # Select general parameters for all optimizers (population size, number of iterations) ....
    params = {
        "population_size": pop,
        "iterations": iterate
    }

    # Choose whether to Export the results in different formats
    export_flags = Export(True, True, True, True, True, True, True)

    run(optimizer, instances, num_of_runs, params, export_flags)
