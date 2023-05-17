import numpy
import vrplib


def get_function_details(name):
    """
    Return the name of objective function, instance, and solution

    Parameters
    ----------
    name : str
        instance name (ex: A-n32-k5)

    Returns
    -------
    x : list
        as described before
    """

    # Download instances
    vrplib.download_instance(name, "./instances/"+name+".vrp")
    vrplib.download_solution(name, "./instances/"+name+".sol")

    instance = vrplib.read_instance("./instances/"+name+".vrp")
    solution = vrplib.read_solution("./instances/"+name+".sol")

    return ["cvrp", instance, solution]


def cvrp(solution, distances, capacity, demands):
    """
    CVRP objective function sum all distance of routes.
    This function take tsp single_route, convert it into cvrp single_route,
    then calculate its total distance (fitness value)

    Parameters
    ----------
    solution : list
        1D list of tsp single_route representation
    distances : list
        matrix of distances
    capacity : number
        maximum capacity of truck (homogeneous)
    demands : list
        matrox of demands

    Returns
    -------
    total : number
        the fitness value of cvrp (total distance)
    """

    routes = split_customer(solution, capacity, demands)

    return normal_cvrp(routes, distances)


def normal_cvrp(solution, distances):
    """
    This function is CVRP objective function with
    CVRP single_route representation as input single_route

    Parameters
    ----------
    solution : list
        list of routes (CVRP single_route representation)
    distances : list
        matrix of distances

    Returns
    -------
    total : number
        the fitness value of cvrp (total distance)
    """

    total = 0
    for r in solution:
        for i in range(len(r) - 1):
            total += distances[r[i]][r[i + 1]]

    return total


def split_customer(solution, capacity, demands):
    """
    This function split tsp single_route into cvrp single_route

    Parameters
    ----------
    solution : list
        1D list of tsp single_route representation
    capacity : number
        maximum capacity of truck (homogeneous)
    demands : list
        matrix of demands

    Returns
    -------
    routes : multidimensional list
        Lists of route, where regular customers are sorted from left -> right
    """

    routes, load, v = [[0]], 0, 0

    for i in solution:
        if demands[i] + load <= capacity:
            routes[v].append(i)
            load += demands[i]
        else:
            routes[v].append(0)  # close the route
            routes.append([0, i])  # open new route
            load = demands[i]
            v += 1

    routes[v].append(0)  # close the last route
    return routes


def concat_depot(route):
    """
    Add depot (index zero) in-front and in-end of route, like sandwich

    Parameters
    ----------
    route : list
        name single route that represent customers order

    Returns
    -------
    new_route : list
        the same route with extra depot (depot -> route -> depot)
    """

    return numpy.concatenate((
        numpy.zeros(1, dtype=int), route, numpy.zeros(1, dtype=int)
    ))
