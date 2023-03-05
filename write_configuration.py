def run(fn, num, pop, iterate, names):
    with open(fn, "a", newline="\n") as out:
        out.write(str(f'Num of run : {num}\n'))
        out.write(str(f'Population : {pop}\n'))
        out.write(str(f'Iterations : {iterate}\n'))
        out.write(str(f'Instances  : {names}\n'))
    out.close()
