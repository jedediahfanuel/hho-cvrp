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

print(sol)

# Add depot as the first and last in route
for i in range(len(sol)):
    sol[i] = [0] + sol[i] + [0]

print(sol)
print()

# def objective(routes):
#     total = 0
#     for r in routes:
#         total_2 = 0
#         for i in range(len(r) - 1):
#             total += distance(
#                 c_list[r[i]]['location'][0], c_list[r[i]]['location'][1],
#                 c_list[r[i + 1]]['location'][0], c_list[r[i + 1]]['location'][1]
#             )
#             # print(c_list[r[i]]['demand'])
#             total_2 += c_list[r[i]]['demand']
#         print(r)
#         print(total_2)
#
#     return total

# print(objective(sol))
# c_list = [
#     {'demand': 0, 'location': (82, 76)},
#
#     {'demand': 19, 'location': (96, 44)},
#     {'demand': 21, 'location': (50, 5)},
#     {'demand': 6, 'location': (49, 8)},
#     {'demand': 19, 'location': (13, 7)},
#     {'demand': 7, 'location': (29, 89)},
#
#     {'demand': 12, 'location': (58, 30)},
#     {'demand': 16, 'location': (84, 39)},
#     {'demand': 6, 'location': (14, 24)},
#     {'demand': 16, 'location': (2, 39)},
#     {'demand': 8, 'location': (3, 82)},
#
#     {'demand': 14, 'location': (5, 10)},
#     {'demand': 21, 'location': (98, 52)},
#     {'demand': 16, 'location': (84, 25)},
#     {'demand': 3, 'location': (61, 59)},
#     {'demand': 22, 'location': (1, 65)},
#     {'demand': 18, 'location': (88, 51)},
#
#     {'demand': 19, 'location': (91, 2)},
#     {'demand': 1, 'location': (19, 32)},
#     {'demand': 24, 'location': (93, 3)},
#     {'demand': 8, 'location': (50, 93)},
#     {'demand': 12, 'location': (98, 14)},
#
#     {'demand': 4, 'location': (5, 42)},
#     {'demand': 8, 'location': (42, 9)},
#     {'demand': 24, 'location': (61, 62)},
#     {'demand': 24, 'location': (9, 97)},
#     {'demand': 2, 'location': (80, 55)},
#
#     {'demand': 20, 'location': (57, 69)},
#     {'demand': 15, 'location': (23, 15)},
#     {'demand': 2, 'location': (20, 70)},
#     {'demand': 14, 'location': (85, 60)},
#     {'demand': 9, 'location': (98, 5)}
# ]

# def distance(x1, y1, x2, y2):
#     return round(math.hypot((x2 - x1), (y2 - y1)))