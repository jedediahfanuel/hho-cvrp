import csv
import numpy
import benchmarks

from model.collection import Collection
from model.solution import Solution


class Export:
    def __init__(self, avg, detail, conv, box, scatter, route, config):
        self.avg = avg
        self.boxplot = box
        self.configuration = config
        self.convergence = conv
        self.details = detail
        self.route = route
        self.scatter = scatter

    @staticmethod
    def write_avg(filename, flag, collection: Collection, solution: Solution, num_of_runs: int, cnvg_header):
        with open(filename, "a", newline="\n") as out:
            writer = csv.writer(out, delimiter=",")
            if not flag:
                # just one time to write the header of the CSV file
                header = numpy.concatenate(
                    [["Optimizer", "Instance", "BKS", "BS", "Gap", "ExecutionTime"], cnvg_header]
                )
                writer.writerow(header)

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

    @staticmethod
    def write_detail(filename, flag_detail, collection: Collection, s: Solution, cnvg_header, k: int):
        with open(filename, "a", newline="\n") as out:
            writer = csv.writer(out, delimiter=",")
            if not flag_detail:
                # just one time to write the header of the CSV file
                header = numpy.concatenate(
                    [["Optimizer", "Instance", "BKS", "BS", "Gap", "ExecutionTime"], cnvg_header]
                )
                writer.writerow(header)

            collection.execution_time[k] = s.execution_time
            collection.best_solution[k] = s.best
            collection.gap_solution[k] = benchmarks.gap(s.bks, s.best)
            a = numpy.concatenate(
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
