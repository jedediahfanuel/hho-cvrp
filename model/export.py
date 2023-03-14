import csv
import platform
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from controller.benchmarks import gap
from model.collection import Collection
from model.solution import Solution

if platform.system() == "Linux":  # Linux: "Linux", Mac: "Darwin", Windows: "Windows"
    import matplotlib

    matplotlib.use('Agg')  # Force matplotlib to not use any Xwindows backend.


class Export:
    def __init__(self, avg, detail, conv, box, scatter, route, config, iterations):
        self.avg = avg
        self.boxplot = box
        self.configuration = config
        self.convergence = conv
        self.details = detail
        self.route = route
        self.scatter = scatter

        # CSV header for convergence
        self.cnvg_header = ["Iter" + str(it + 1) for it in range(0, iterations)]
        self.flag = False
        self.flag_detail = False

    def write_avg(self, filename, collection: Collection, solution: Solution, num_of_runs: int):
        with open(filename, "a", newline="\n") as out:
            writer = csv.writer(out, delimiter=",")
            if not self.flag:
                # just one time to write the header of the CSV file
                header = np.concatenate(
                    [["Optimizer", "Instance", "BKS", "BS", "Gap", "ExecutionTime"], self.cnvg_header]
                )
                writer.writerow(header)
                self.flag = True

            avg_execution_time = float("%0.2f" % (sum(collection.execution_time) / num_of_runs))
            avg_bs = float("%0.2f" % (sum(collection.best_solution) / num_of_runs))
            avg_gap = float("%0.4f" % (sum(collection.gap_solution) / num_of_runs))
            avg_convergence = np.around(
                np.mean(collection.convergence, axis=0, dtype=np.float64), decimals=2
            ).tolist()
            a = np.concatenate(
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

    @staticmethod
    def write_configuration(filename, num, pop, iterate, names):
        """
        Create a file that log current test parameter configuration

        Parameters
        ----------
        filename : str
            filename
        num : int
            number of run
        pop : int
            population size
        iterate : int
            number of iterations
        names

        Returns
        -------
        N/A
        """

        with open(filename, "a", newline="\n") as out:
            out.write(str(f'Num of run : {num}\n'))
            out.write(str(f'Population : {pop}\n'))
            out.write(str(f'Iterations : {iterate}\n'))
            out.write(str(f'Instances  : {names}\n'))
        out.close()

    def write_detail(self, filename, collection: Collection, s: Solution, k: int):
        with open(filename, "a", newline="\n") as out:
            writer = csv.writer(out, delimiter=",")
            if not self.flag_detail:
                # just one time to write the header of the CSV file
                header = np.concatenate(
                    [["Optimizer", "Instance", "BKS", "BS", "Gap", "ExecutionTime"], self.cnvg_header]
                )
                writer.writerow(header)
                self.flag_detail = True

            collection.execution_time[k] = s.execution_time
            collection.best_solution[k] = s.best
            collection.gap_solution[k] = gap(s.bks, s.best)
            a = np.concatenate(
                [
                    [
                        s.optimizer,
                        s.name,
                        s.bks,
                        s.best,
                        collection.gap_solution[k],
                        s.execution_time
                    ],
                    s.convergence
                ]
            )
            writer.writerow(a)
        out.close()

    @staticmethod
    def write_route(results_directory, solution: Solution, k: int):
        """
        Create a file that contains the final routes of current run

        Parameters
        ----------
        solution : Solution
            solution class (check solution.py)
        results_directory : str
            directory path the file will be saved
        k : int
            number of current run

        Returns
        -------
        N/A
        """

        fn = solution.name + "-" + solution.optimizer + "-" + str(k) + ".sol"
        with open(results_directory + fn, "a", newline="\n") as out:
            for i, route in enumerate(solution.routes):
                out.write(str(f"Route #{i + 1}: "))

                for city in route:
                    if city == 0:
                        continue

                    whitespace = "\n" if city == route[-2] else " "

                    out.write(str(f"{city}{whitespace}"))

            out.write(str(f"Cost {solution.best}"))
        out.close()

    @staticmethod
    def write_boxplot(results_directory, optimizer, instances, iterations):
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

    @staticmethod
    def write_convergence(results_directory, optimizer, instances, iterations):
        """
        Create a convergence of fitness value of each algorithm

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
        file_results_data = pd.read_csv(results_directory + "../experiment_avg.csv")

        for j in range(0, len(instances)):
            instance_name = instances[j]

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
                row = row.iloc[:, 6 + start_iteration:]
                plt.plot(all_generations, row.values.tolist()[0], label=optimizer_name)
            plt.xlabel("Iterations")
            plt.ylabel("Fitness")
            plt.legend(loc="upper right", bbox_to_anchor=(1.2, 1.02))
            plt.grid()
            fig_name = results_directory + "/convergence-" + instance_name + ".png"
            plt.savefig(fig_name, bbox_inches="tight")
            plt.clf()

    @staticmethod
    def write_scatter(s: Solution, results_directory, k: int):
        """
        Create a picture & PDF that plot customers location and routes lines

        Parameters
        ----------
        s : Solution
            solution class (check solution.py)
        results_directory : str
            directory path the file will be saved
        k : int
            number of current run

        Returns
        -------
        N/A
        """

        plt.ioff()
        fn = "scatter-" + s.name + "-" + str(k) + "-" + str(s.best)
        plot_cities(s, pathsave=results_directory, filename=fn, size=10, show_id=False)


def get_space(coordinates):
    x_min, x_max = np.min(coordinates[:, 0:]), np.max(coordinates[:, 0:])
    y_min, y_max = np.min(coordinates[:, 1:]), np.max(coordinates[:, 1:])
    text_space_x = (x_min + x_max) / 75
    text_space_y = (y_min + y_max) / 75
    space_x = np.mean(coordinates[:, 0:]) / 5
    space_y = np.mean(coordinates[:, 1:]) / 5
    return x_min, x_max, y_min, y_max, text_space_x, text_space_y, space_x, space_y


def plot_cities(s: Solution, filename: str, pathsave: str, exts=(".png", ".pdf"), size=100, show_id=True):
    coordinates = np.array(s.coordinates)

    # add text annotation
    x_min, x_max, y_min, y_max, text_space_x, text_space_y, space_x, space_y = get_space(coordinates)

    if show_id:
        for city in range(0, s.dim):
            plt.text(coordinates[city][0] - text_space_x, coordinates[city][1] - text_space_y,
                     f"{city}", size='xx-small', color='black', weight='normal')

    for i, r in enumerate(s.routes):
        point_x = np.array([coordinates[x, 0].T for x in r])
        point_y = np.array([coordinates[y, 1].T for y in r])
        line_x = np.array([coordinates[x, 0] for x in r])
        line_y = np.array([coordinates[y, 1] for y in r])

        # draw customer & routes
        plt.scatter(point_x[:-1], point_y[:-1], s=size)
        plt.plot(line_x, line_y, '-', label=str(f'route {i + 1}'), lw=0.5)

        plt.text(x_min - 2 * space_x, y_min - 2 * space_y, f"Total distance: {s.best}",
                 fontdict={'size': 8, 'color': 'red'})

    plt.xlim((x_min - space_x, x_max + space_x))
    plt.ylim((y_min - space_y, y_max + space_y))
    plt.title(s.name + " " + str(s.best))
    plt.legend(fontsize='xx-small', bbox_to_anchor=(1, 0.5))

    Path(pathsave).mkdir(parents=True, exist_ok=True)

    for idx, ext in enumerate(exts):
        plt.savefig(f"{pathsave}/{filename}{ext}", bbox_inches='tight')

    plt.close()
