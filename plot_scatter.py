import platform
from pathlib import Path
from solution import Solution

import numpy as np
import matplotlib.pyplot as plt

if platform.system() == "Linux":  # Linux: "Linux", Mac: "Darwin", Windows: "Windows"
    import matplotlib

    matplotlib.use('Agg')  # Force matplotlib to not use any Xwindows backend.


def run(s: Solution, results_directory, k: int):
    plt.ioff()
    fn = "scatter-" + s.name + "-" + str(k) + "-" + str(s.best)
    plot_cities(s, pathsave=results_directory, filename=fn)


def get_space(coordinates):
    x_min, x_max = np.min(coordinates[:, 0:]), np.max(coordinates[:, 0:])
    y_min, y_max = np.min(coordinates[:, 1:]), np.max(coordinates[:, 1:])
    text_space_x = (x_min + x_max) / 75
    text_space_y = (y_min + y_max) / 75
    space_x = np.mean(coordinates[:, 0:]) / 5
    space_y = np.mean(coordinates[:, 1:]) / 5
    return x_min, x_max, y_min, y_max, text_space_x, text_space_y, space_x, space_y


def plot_cities(s: Solution, filename: str, pathsave: str, exts=(".png", ".pdf"), size=100, show_id=True):
    coordinates = np.array(s.coordinates)

    # add text annotation
    x_min, x_max, y_min, y_max, text_space_x, text_space_y, space_x, space_y = get_space(coordinates)

    if show_id:
        for city in range(0, s.dim):
            plt.text(coordinates[city][0] - text_space_x, coordinates[city][1] - text_space_y,
                     f"{city}", size='xx-small', color='black', weight='normal')

    for i, r in enumerate(s.routes):
        point_x = np.array([coordinates[x, 0].T for x in r])
        point_y = np.array([coordinates[y, 1].T for y in r])
        line_x = np.array([coordinates[x, 0] for x in r])
        line_y = np.array([coordinates[y, 1] for y in r])

        # draw cities
        plt.scatter(point_x, point_y, s=size)

        # draw lines
        plt.plot(line_x, line_y, '-', label=str(f'route {i + 1}'), lw=0.5)
        plt.text(x_min - 2 * space_x, y_min - 2 * space_y, f"Total distance: {s.best}",
                 fontdict={'size': 8, 'color': 'red'})

    plt.xlim((x_min - space_x, x_max + space_x))
    plt.ylim((y_min - space_y, y_max + space_y))
    plt.title(s.name + " " + str(s.best))
    plt.legend(fontsize='xx-small', bbox_to_anchor = (1, 0.5))

    Path(pathsave).mkdir(parents=True, exist_ok=True)

    for idx, ext in enumerate(exts):
        plt.savefig(f"{pathsave}/{filename}{ext}", bbox_inches='tight')

    if platform.system() != "Linux":
        plt.show()
    plt.close()
