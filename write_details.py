import csv
import numpy
import benchmarks

from optimizer import Collection
from solution import Solution


def run(fn, collection: Collection, s: Solution, cnvg_header, k: int):
    with open(fn, "a", newline="\n") as out:
        writer = csv.writer(out, delimiter=",")
        if k == 0:
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
