import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def run(results_directory, optimizer, instances, iterations):
    """
    Create a boxplot of fitness value of each algorithm

    Parameters
    ----------
    results_directory : str
        directory path the file will be saved
    optimizer :
        list of optimizers
    instances : CVRPLIB CVRP Class
        instance of problem
    iterations :
        number of iterations

    Returns
    -------
    N/A
    """

    plt.ioff()

    file_results_details_data = pd.read_csv(results_directory + "../experiment_details.csv")
    for j in range(0, len(instances)):

        # Box Plot
        data = []

        for i in range(len(optimizer)):
            instance_name = instances[j]
            optimizer_name = optimizer[i]

            detailed_data = file_results_details_data[
                (file_results_details_data["Optimizer"] == optimizer_name)
                & (file_results_details_data["Instance"] == instance_name)
                ]
            detailed_data = detailed_data["Iter" + str(iterations)]
            detailed_data = np.array(detailed_data).T.tolist()
            data.append(detailed_data)

        # , notch=True
        box = plt.boxplot(data, patch_artist=True, labels=optimizer)

        colors = [
            "#5c9eb7", "#f77199", "#cf81d2", "#4a5e6a",
            "#f45b18", "#ffbd35", "#6ba5a1", "#fcd1a1",
            "#c3ffc1", "#68549d", "#1c8c44", "#a44c40",
            "#404636",
        ]
        for patch, color in zip(box["boxes"], colors):
            patch.set_facecolor(color)

        plt.legend(
            handles=box["boxes"],
            labels=optimizer,
            loc="upper right",
            bbox_to_anchor=(1.2, 1.02),
        )
        fig_name = results_directory + "/boxplot-" + instance_name + ".png"
        plt.savefig(fig_name, bbox_inches="tight")
        plt.clf()
