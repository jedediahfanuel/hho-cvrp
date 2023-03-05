from solution import Solution


def run(s: Solution, results_directory, k: int):
    fn = s.name + "-" + s.optimizer + "-" + str(k) + ".sol"
    with open(results_directory + fn, "a", newline="\n") as out:
        for i, route in enumerate(s.routes):
            out.write(str(f"Route #{i + 1}: "))

            for city in route:
                if city == 0:
                    continue

                whitespace = "\n" if city == route[-2] else " "

                out.write(str(f"{city}{whitespace}"))

        out.write(str(f"Cost {s.best}"))
    out.close()
