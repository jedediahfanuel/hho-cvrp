import random


def n_vehicle(name):
    return int(name[name.rfind("k") + 1:])


def add_depot(s):
    for i in range(len(s)):
        s[i] = [0] + s[i] + [0]
    return s


def initial_solution(n_customers, n_vehicles, capacity, demands):
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
    return add_depot(routes)


#TODO: masih nge bug kah? infinity loop? Tapi mungkin karena si input nya yg ngaco
def binary_to_permutation(s):
    trip = [0]
    current_customer = 0  # mulai dari depot
    while len(trip) <= len(s[0]):
        for i, val in enumerate(s[current_customer]):
            if val:
                trip.append(i)
                current_customer = i
                break
        if current_customer == 0:  # berakhir di depot
            break
    return trip


def get_route(binary_solution):
    routes = []
    for route in binary_solution:
        routes.append(binary_to_permutation(route))
    return routes


def permutation_to_binary(permutation, dim):
    x = [[0 for _ in range(dim)] for _ in range(dim)]
    current_customer = permutation[0]
    for next_customer in permutation[1:]:
        x[current_customer][next_customer] = 1
        current_customer = next_customer
    return x


def get_binary(permutation_solution, dim):
    routes = []
    for route in permutation_solution:
        routes.append(permutation_to_binary(route, dim))
    return routes
