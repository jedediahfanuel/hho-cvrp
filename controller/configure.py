from controller import backbone
from model.export import Export
from model.parameter import Parameter


def conf(num, pop, iterate, names, exports, city_size, city_id, progress, result_directory="", optimizer=None):
    """
    Parameter configuration for test

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
    exports : list of bool
        list of which export will be proceeded
    city_size : int
        the size of scatter-plot dots
    city_id : bool
        show city id in scatter-plot
    progress : function
        a progress bar update function
    result_directory : str
        path of root directory for result files
    optimizer : list of str
        list of optimizer name to be tested
    """

    # Collection of params
    params = Parameter(num, pop, iterate, names, city_size, city_id, result_directory, optimizer)

    # Choose whether to Export the results in different formats
    export_flags = Export(
        True,        # average
        exports[0],  # boxplot
        exports[1],  # configuration
        exports[2],  # convergence
        True,        # details
        exports[3],  # routes
        exports[4],  # scatter-plot
        iterate)

    backbone.run(params, export_flags, progress)
