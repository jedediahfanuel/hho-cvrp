import csv
import platform
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from controller.benchmarks import gap
from model.collection import Collection
from model.parameter import Parameter
from model.solution import Solution

if platform.system() == "Linux":  # Linux: "Linux", Mac: "Darwin", Windows: "Windows"
    import matplotlib

    matplotlib.use('Agg')  # Force matplotlib to not use any Xwindows backend.


class Export:
    def __init__(self, avg, box, config, conv, detail, route, scatter, iteration):
        self.avg = avg
        self.boxplot = box
        self.configuration = config
        self.convergence = conv
        self.details = detail
        self.route = route
        self.scatter = scatter

        # CSV header for convergence
        self.cnvg_header = ["Iter" + str(it + 1) for it in range(0, iteration)]
        self.flag = False
        self.flag_detail = False

    def write_avg(self, collection: Collection, solution: Solution, params: Parameter):
        """
        Write experiment_avg.csv for averaged detail for each instance and optimizer

        Parameters
        ----------
        collection : Collection
            class of collection (check collection.py)
        solution : Solution
            class of solution (check solution.py)
        params : Parameter
            collection of configurable user parameter

        Returns
        -------

        """
        filename = params.results_directory + "experiment_avg.csv"

        with open(filename, "a", newline="\n") as out:
            writer = csv.writer(out, delimiter=",")
            if not self.flag:
                # just one time to write the header of the CSV file
                header = np.concatenate(
                    [["Optimizer", "Instance", "BKS", "BS", "Gap", "ExecutionTime"], self.cnvg_header]
                )
                writer.writerow(header)
                self.flag = True

            avg_execution_time = float("%0.2f" % (sum(collection.execution_time) / params.n_runs))
            avg_bs = float("%0.2f" % (sum(collection.best_solution) / params.n_runs))
            avg_gap = float("%0.4f" % (sum(collection.gap_solution) / params.n_runs))
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
    def write_configuration(params: Parameter):
        """
        Create a file that log current test parameter configuration

        Parameters
        ----------
        params : Parameter
            collection of configurable user parameter

        Returns
        -------
        N/A
        """

        filename = params.results_directory + "configuration.txt"

        with open(filename, "a", newline="\n") as out:
            out.write(str(f'Num of run : {params.n_runs}\n'))
            out.write(str(f'Population : {params.population}\n'))
            out.write(str(f'Iterations : {params.iteration}\n'))
            out.write(str(f'Instances  : {params.instances}\n'))
        out.close()

    def write_detail(self, collection: Collection, solution: Solution, params: Parameter, k: int):
        """
        Write experiment_detail.csv for averaged detail for each instance, optimizer, and iteration

        Parameters
        ----------
        collection : Collection
            class of collection (check collection.py)
        solution : Solution
            class of solution (check solution.py)
        params : Parameter
            collection of configurable user parameter
        k : int
            number of current run

        Returns
        -------

        """
        filename = params.results_directory + "experiment_details.csv"

        with open(filename, "a", newline="\n") as out:
            writer = csv.writer(out, delimiter=",")
            if not self.flag_detail:
                # just one time to write the header of the CSV file
                header = np.concatenate(
                    [["Optimizer", "Instance", "BKS", "BS", "Gap", "ExecutionTime"], self.cnvg_header]
                )
                writer.writerow(header)
                self.flag_detail = True

            collection.execution_time[k] = solution.execution_time
            collection.best_solution[k] = solution.best
            collection.gap_solution[k] = gap(solution.bks, solution.best)
            a = np.concatenate(
                [
                    [
                        solution.optimizer,
                        solution.name,
                        solution.bks,
                        solution.best,
                        collection.gap_solution[k],
                        solution.execution_time
                    ],
                    solution.convergence
                ]
            )
            writer.writerow(a)
        out.close()

    @staticmethod
    def write_route(solution: Solution, params: Parameter, k: int):
        """
        Create a file that contains the final routes of current run

        Parameters
        ----------
        solution : Solution
            class of solution (check solution.py)
        params : Parameter
            collection of configurable user parameter
        k : int
            number of current run

        Returns
        -------
        N/A
        """

        rd = params.results_directory + "routes-" + solution.optimizer + "/" + solution.name + "/"
        Path(rd).mkdir(parents=True, exist_ok=True)
        filename = rd + solution.name + "-" + solution.optimizer + "-" + str(k) + ".sol"

        with open(filename, "a", newline="\n") as out:
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
    def write_boxplot(params: Parameter):
        """
        Create a boxplot of fitness value of each algorithm
    
        Parameters
        ----------
        params : Parameter
            collection of configurable user parameter
    
        Returns
        -------
        N/A
        """

        plt.ioff()

        rd = params.results_directory + "box-plot/"
        Path(rd).mkdir(parents=True, exist_ok=True)
        file_results_details_data = pd.read_csv(rd + "../experiment_details.csv")

        for instance_name in params.instances:

            # Box Plot
            data = []

            for optimizer_name in params.optimizers:
                detailed_data = file_results_details_data[
                    (file_results_details_data["Optimizer"] == optimizer_name)
                    & (file_results_details_data["Instance"] == instance_name)
                    ]
                detailed_data = detailed_data["Iter" + str(params.iteration)]
                detailed_data = np.array(detailed_data).T.tolist()
                data.append(detailed_data)

            # , notch=True
            box = plt.boxplot(data, patch_artist=True, labels=params.optimizers)

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
                labels=params.optimizers,
                loc="upper right",
                bbox_to_anchor=(1.2, 1.02),
            )
            fig_name = rd + "/boxplot-" + instance_name + ".png"
            plt.savefig(fig_name, bbox_inches="tight")
            plt.clf()

    @staticmethod
    def write_convergence(params: Parameter):
        """
        Create a convergence of fitness value of each algorithm

        Parameters
        ----------
        params : Parameter
            collection of configurable user parameter

        Returns
        -------
        N/A
        """

        plt.ioff()

        rd = params.results_directory + "convergence-plot/"
        Path(rd).mkdir(parents=True, exist_ok=True)
        file_results_data = pd.read_csv(rd + "../experiment_avg.csv")

        for instance_name in params.instances:
            start_iteration = 0
            if "SSA" in params.optimizers:
                start_iteration = 1
            all_generations = [x + 1 for x in range(start_iteration, params.iteration)]

            for i, optimizer_name in enumerate(params.optimizers):
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
            fig_name = rd + "/convergence-" + instance_name + ".png"
            plt.savefig(fig_name, bbox_inches="tight")
            plt.clf()

    @staticmethod
    def write_scatter(solution: Solution, params: Parameter, k: int):
        """
        Create a picture & PDF that plot customers location and routes lines

        Parameters
        ----------
        solution : Solution
            class of solution (check solution.py)
        params : Parameter
            collection of configurable user parameter
        k : int
            number of current run

        Returns
        -------
        N/A
        """

        close = "/" if solution.coordinates is not None else "/None"
        rd = params.results_directory + "scatter-plot-" + solution.optimizer + "/" + solution.name + close
        Path(rd).mkdir(parents=True, exist_ok=True)

        plt.ioff()
        filename = "scatter-" + solution.name + "-" + str(k) + "-" + str(solution.best)
        plot_cities(solution, pathsave=rd, filename=filename, size=params.city_size, show_id=params.city_id)


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
