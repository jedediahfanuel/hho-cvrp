# from pprint import pprint
#
# import cvrplib
#
# # Download instances
# instance = cvrplib.download('A-n32-k5')
# instance, solution = cvrplib.download('A-n32-k5', solution=True)
#
# pprint(instance)
# pprint(solution)
#
# import random
# import time
#
# random.seed(int(time.time()))
#
# n = 31
# print(random.sample(range(n), n))
# print(random.sample(range(n), n))

# initialize the location and Energy of the rabbit
import numpy

dim = 9
lb = 0
ub = 1
s = 5

Rabbit_Location = numpy.zeros(dim)
Rabbit_Energy = float("inf")  # change this to -inf for maximization problems

if not isinstance(lb, list):
    lb = [lb for _ in range(dim)]
    ub = [ub for _ in range(dim)]

lb = numpy.asarray(lb)
ub = numpy.asarray(ub)

# Initialize the locations of Harris' hawks
X = numpy.asarray([x * (ub - lb) + lb for x in numpy.random.uniform(0, 1, (s, dim))])

print(X)
