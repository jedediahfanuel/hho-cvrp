import numpy
import cvrplib


def getFunctionDetails(a):
    # Download instances
    instance = cvrplib.download(a)

    # [name, lb, ub, dim]
    param = {
        # dimensi = banyaknya customer
        "cvrp": ["cvrp", 1, instance.dimension - 0.01, instance.n_customers],
    }
    return param.get("cvrp", "nothing")


# fungsi objektif dari cvrp
# dimana menghitung jarak total dari seluruh rute
def cvrp(routes, distances):
    # inget ini masih 1 rute
    # kedepannya sih pecah dulu jadi beberapa rute
    # baru kirim ke concat_depot
    routes = concat_depot(generate_stable_solution(routes))
    total = 0
    for r in routes:
        for i in range(len(r) - 1):
            total += distances[r[i]][r[i + 1]]
    return total


def concat_depot(s):
    return numpy.concatenate((
        numpy.zeros(1, dtype=int), s, numpy.zeros(1, dtype=int)
    ))


def generate_stable_solution(solution, lb=None, ub=None):
    # print(f"Raw: {solution}")
    # Bring them back to boundary
    # sudah dilakuin sebelum masuk fungsi objektif
    # solution = numpy.clip(solution, lb, ub)

    solution_set = set(list(range(0, len(solution))))
    solution_done = numpy.array([-1, ] * len(solution))
    solution_int = solution.astype(int)
    city_unique, city_counts = numpy.unique(solution_int, return_counts=True)

    # Way 1: Stable, not random
    for idx, city in enumerate(solution_int):
        if solution_done[idx] != -1:
            continue
        if city in city_unique:
            solution_done[idx] = city
            city_unique = numpy.where(city_unique == city, -1, city_unique)
        else:
            list_cities_left = list(solution_set - set(city_unique) - set(solution_done))
            # print(list_cities_left)
            solution_done[idx] = list_cities_left[0]
    # print(f"What: {solution_done}")
    return solution_done


def generate_unstable_solution(solution, lb=None, ub=None):
    # print(solution)
    solution_bound = numpy.clip(solution, lb, ub)
    solution_set = set(range(int(lb[0]), round(ub[0])))
    solution_done = numpy.array([-1, ] * len(solution_bound))
    solution_int = solution_bound.astype(int)
    # print(solution_int)
    city_unique, city_counts = numpy.unique(solution_int, return_counts=True)

    # Way 2: Random, not stable
    # count_dict = dict(zip(*numpy.unique(solution_int, return_counts=True)))
    count_dict = dict(zip(city_unique, city_counts))
    for idx, city in enumerate(solution_int):
        if solution_done[idx] != -1:
            continue
        if city in city_unique:
            if city in (solution_set - set(solution_done)):
                if count_dict[city] == 1:
                    solution_done[idx] = city
                else:
                    idx_list_city = numpy.where(solution_int == city)[0]
                    idx_city_keep = numpy.random.choice(idx_list_city)
                    solution_done[idx_city_keep] = city
                    if idx_city_keep != idx:
                        solution_done[idx] = numpy.random.choice(
                            list(solution_set - set(solution_done) - set(city_unique)))
            else:
                solution_done[idx] = numpy.random.choice(list(solution_set - set(solution_done) - set(city_unique)))
        else:
            solution_done[idx] = numpy.random.choice(list(solution_set - set(solution_done) - set(city_unique)))
    # print(solution_done)
    return solution_done
