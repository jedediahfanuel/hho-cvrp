import benchmarks
import cvrplib
from itertools import chain

data, sol = cvrplib.download("A-n32-k5", solution=True)

print(benchmarks.cvrp(list(chain.from_iterable(sol.routes)), data.distances, data.capacity, data.demands))
