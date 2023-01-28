import numpy
import cvrplib


def get_function_details(a):
    # Download instances
    instance = cvrplib.download(a)

    # [name, lb, ub, dim]
    param = {
        # dimensi = banyaknya customer
        "cvrp": ["cvrp", instance],
    }
    return param.get("cvrp", "nothing")


# fungsi objektif dari cvrp
# dimana menghitung jarak total dari seluruh rute
def cvrp(routes, distances):
    # inget ini masih 1 rute
    # kedepannya sih pecah dulu jadi beberapa rute
    # baru kirim ke concat_depot
    routes = concat_depot(routes)
    total = 0
    # for r in routes:
    #     for i in range(len(r) - 1):
    #         total += distances[r[i]][r[i + 1]]
    for i in range(len(routes) - 1):
        total += distances[routes[i]][routes[i + 1]]
    return total


def concat_depot(s):
    return numpy.concatenate((
        numpy.zeros(1, dtype=int), s, numpy.zeros(1, dtype=int)
    ))
