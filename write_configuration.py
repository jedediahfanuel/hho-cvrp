def run(fn, num, pop, iterate, names):
    """
    Create a file that log current test parameter configuration

    Parameters
    ----------
    fn : str
        filename
    num : int
        number of run
    pop : int
        population size
    iterate : int
        number of iterations
    names

    Returns
    -------
    N/A
    """

    with open(fn, "a", newline="\n") as out:
        out.write(str(f'Num of run : {num}\n'))
        out.write(str(f'Population : {pop}\n'))
        out.write(str(f'Iterations : {iterate}\n'))
        out.write(str(f'Instances  : {names}\n'))
    out.close()
