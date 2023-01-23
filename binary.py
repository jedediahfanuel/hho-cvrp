sol = [
    [  # 1st route
        [0, 1, 0, 0, 0],  # depot
        [0, 0, 0, 0, 1],  # customer 1
        [0, 0, 0, 1, 0],  # customer 2
        [1, 0, 0, 0, 0],  # customer 3
        [0, 0, 1, 0, 0],  # customer 4
    ],
    [  # 2nd route
        [0, 0, 0, 0, 1],  # depot
        [0, 0, 0, 1, 0],  # customer 1
        [1, 0, 0, 0, 0],  # customer 2
        [0, 0, 1, 0, 0],  # customer 3
        [0, 1, 0, 0, 0],  # customer 4
    ]
]


def binary_to_permutation(s):
    trip = [0]
    current_customer = 0  # mulai dari depot
    while True:
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


def permutation_to_binary(permutation):
    x = [[0 for j in range(5)] for i in range(5)]
    current_customer = permutation[0]
    for next_customer in permutation[1:]:
        x[current_customer][next_customer] = 1
        current_customer = next_customer
    return x


def get_binary(permutation_solution):
    routes = []
    for route in permutation_solution:
        routes.append(permutation_to_binary(route))
    return routes


print(get_route(sol))
print(get_binary(get_route(sol)))

# def generate_random_solution_x_kij(customers, demand, capacity, num_vehicles):
#     x = [[[0 for j in range(num_customers)] for i in range(num_customers)] for k in range(num_vehicles)]
#     remaining_demand = demand.copy()
#     remaining_capacity = [capacity for _ in range(num_vehicles)]
#     for k in range(num_vehicles):
#         current_customer = 0
#         while remaining_demand:
#             feasible_customers = [c for c in customers if
#                                   remaining_demand[c] > 0 and remaining_demand[c] <= remaining_capacity[
#                                       k] and c != current_customer]
#             if feasible_customers:
#                 next_customer = random.choice(feasible_customers)
#                 x[k][current_customer][next_customer] = 1
#                 remaining_demand[next_customer] = 0
#                 remaining_capacity[k] -= demand[next_customer]
#                 current_customer = next_customer
#             else:
#                 x[k][current_customer][0] = 1
#                 current_customer = 0
#     return x


import random
