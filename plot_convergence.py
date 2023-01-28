import matplotlib.pyplot as plt
import pandas as pd


def run(results_directory, optimizer, objectivefunc, iterations):
    plt.ioff()
    file_results_data = pd.read_csv(results_directory + "/experiment.csv")

    for j in range(0, len(objectivefunc)):
        instance_name = objectivefunc[j] # ini harusnya cvrp tapi ganti dulu ke na

        start_iteration = 0
        if "SSA" in optimizer:
            start_iteration = 1
        all_generations = [x + 1 for x in range(start_iteration, iterations)]

        for i in range(len(optimizer)):
            optimizer_name = optimizer[i]

            row = file_results_data[
                (file_results_data["Optimizer"] == optimizer_name)
                & (file_results_data["Instance"] == instance_name)
                ]
            row = row.iloc[:, 3 + start_iteration:]
            plt.plot(all_generations, row.values.tolist()[0], label=optimizer_name)
        plt.xlabel("Iterations")
        plt.ylabel("Fitness")
        plt.legend(loc="upper right", bbox_to_anchor=(1.2, 1.02))
        plt.grid()
        fig_name = results_directory + "/convergence-" + instance_name + ".png"
        plt.savefig(fig_name, bbox_inches="tight")
        plt.clf()

