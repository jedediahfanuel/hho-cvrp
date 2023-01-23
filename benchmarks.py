from typing import Dict, Any, List

import numpy
import math
import cvrplib


def getFunctionDetails(a):
    # Download instances
    instance = cvrplib.download(a)

    # [name, lb, ub, problem]
    param = {
        "cvrp": ["cvrp", 0, 1, instance],
    }
    return param.get("cvrp", "nothing")


# fungsi objektif dari cvrp
# dimana menghitung jarak total dari seluruh rute
def cvrp(routes, distances):
    total = 0
    for r in routes:
        for i in range(len(r) - 1):
            total += distances[r[i]][r[i + 1]]
    return total
