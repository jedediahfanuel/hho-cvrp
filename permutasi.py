import math
import random
import cvrplib

# Download instances
instance, solution = cvrplib.download('A-n32-k5', solution=True)


# print(instance.name)
# print(instance.dimension)
# print(instance.n_customers)
# print(instance.depot)
# print(instance.customers)
# print(instance.capacity)
# print(instance.distances)
# print(instance.demands)
# print(instance.service_times)
# print(instance.coordinates)


def n_vehicle(name):
    return int(name[name.rfind("k") + 1:])


def generate_solution(n_customers, n_vehicles, capacity, demands):
    """
    Generates a permutation solution
    with multiple vehicles
    and checks its constraints.
    """

    permutation = random.sample(range(1, n_customers + 1), n_customers)
    loads = [0] * n_vehicles
    routes = [[] for _ in range(n_vehicles)]
    vehicle = 0

    for i in permutation:
        if loads[vehicle] + demands[i] <= capacity:
            routes[vehicle].append(i)
            loads[vehicle] += demands[i]
        else:
            vehicle = (vehicle + 1) % n_vehicles
            if loads[vehicle] + demands[i] <= capacity:
                routes[vehicle].append(i)
                loads[vehicle] += demands[i]
    return routes


sol = generate_solution(
    instance.n_customers,
    n_vehicle(instance.name),
    instance.capacity,
    instance.demands
)


# Add depot as the first and last in route
def add_depot(s):
    for i in range(len(s)):
        s[i] = [0] + s[i] + [0]
    return s


def objective(routes, distances):
    total = 0
    for r in routes:
        for i in range(len(r) - 1):
            total += distances[r[i]][r[i + 1]]
    return total


print(objective(add_depot(solution.routes), instance.distances))

# def distance(x1, y1, x2, y2):
#     return round(math.hypot((x2 - x1), (y2 - y1)))
