import numpy
import cvrplib


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
    instance, solution = cvrplib.download(name, solution=True)

    return ["cvrp", instance, solution]


def cvrp(solution, distances, max_capacity, demands):
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
    max_capacity : number
        maximum capacity of truck (homogeneous)
    demands : list
        matrox of demands

    Returns
    -------
    total : number
        the fitness value of cvrp (total distance)
    """

    routes = split_customer(solution, max_capacity, demands)

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


def split_customer(solution, max_capacity, demands):
    """
    This function split tsp single_route into cvrp single_route

    Parameters
    ----------
    solution : list
        1D list of tsp single_route representation
    max_capacity : number
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
        if demands[i] + load <= max_capacity:
            routes[v].append(i)
            load += demands[i]
        else:
            routes[v].append(0)  # close the route
            routes.append([0, i])  # open new route
            load = demands[i]
            v += 1

    routes[v].append(0)  # close the last route
    return routes


def concat_depot(single_route):
    """
    Add depot (index zero) in-front and in-end of route, like sandwich

    Parameters
    ----------
    single_route : list
        name single route that represent customers order

    Returns
    -------
    new_route : list
        the same route with extra depot (depot -> route -> depot)
    """

    return numpy.concatenate((
        numpy.zeros(1, dtype=int), single_route, numpy.zeros(1, dtype=int)
    ))


def gap(bks, bs):
    """
    Calculate gap of two route in percentage. If the result is positive number,
    that means bks has name better value, and vice versa

    Parameters
    ----------
    bks : number
        best solution known
    bs : number
        best solution

    Returns
    -------
    gap : number
        the gap of bks and bs (in percentage)
    """

    return (bs - bks) * 100 / bks
