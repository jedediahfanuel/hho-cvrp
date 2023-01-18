from optimizer import run

# Select optimizers
optimizer = ["HHO"]

# Select benchmark function
objectivefunc = ["F3", "F4"]

# Select number of repetitions for each experiment.
# To obtain meaningful statistical results, usually 30 independent runs are executed for each algorithm.
NumOfRuns = 3

# Select general parameters for all optimizers (population size, number of iterations) ....
params = {"PopulationSize": 30, "Iterations": 50}

# Choose whether to Export the results in different formats
export_flags = {
    "Export_avg": True,
    "Export_details": True,
    "Export_convergence": True,
    "Export_boxplot": True,
}

run(optimizer, objectivefunc, NumOfRuns, params, export_flags)
