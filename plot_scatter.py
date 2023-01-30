import platform
import datetime
from pathlib import Path
from solution import Solution

import numpy as np
import matplotlib.pyplot as plt

t = datetime.datetime.now().strftime(" %d %b %Y %X")

if platform.system() == "Linux":  # Linux: "Linux", Mac: "Darwin", Windows: "Windows"
    import matplotlib

    matplotlib.use('Agg')  # Force matplotlib to not use any Xwindows backend.


def run(s: Solution, results_directory):
    plt.ioff()
    fn = "scatter-" + s.name + "-" + s.optimizer + t
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
    plt.scatter(coordinates[:, 0].T, coordinates[:, 1].T, s=size, c='k')

    # add text annotation
    x_min, x_max, y_min, y_max, text_space_x, text_space_y, space_x, space_y = get_space(coordinates)

    if show_id:
        for city in range(0, s.dim):
            plt.text(coordinates[city][0] - text_space_x, coordinates[city][1] - text_space_y,
                     f"{city}", size='xx-small', color='white', weight='normal')

    plt.xlim((x_min - space_x, x_max + space_x))
    plt.ylim((y_min - space_y, y_max + space_y))
    plt.title(s.name + " " + s.best)

    Path(pathsave).mkdir(parents=True, exist_ok=True)

    for idx, ext in enumerate(exts):
        plt.savefig(f"{pathsave}/{filename}{ext}", bbox_inches='tight')

    if platform.system() != "Linux":
        plt.show()
    plt.close()


def plot_solutions(self, dict_solutions, filename: str, pathsave: str, exts=(".png", ".pdf"),
                   size=100, show_id=True):
    x_min, x_max, y_min, y_max, text_space_x, text_space_y, space_x, space_y = self.__get_space__()

    for idx_pos, solution in enumerate(dict_solutions.values()):
        obj_value = solution[1]
        city_coord = self.city_positions[solution[0]]
        line_x = city_coord[:, 0]
        line_y = city_coord[:, 1]
        plt.scatter(self.city_positions[:, 0].T, self.city_positions[:, 1].T, s=size, c='k')

        # add text annotation
        if show_id:
            for city in range(0, self.n_cities):
                plt.text(self.city_positions[city][0] + text_space_x, self.city_positions[city][1] - text_space_y,
                         f"{city}", size='medium', color='black', weight='semibold')

        plt.plot(line_x.T, line_y.T, 'r-')
        plt.text(x_min - 2 * space_x, y_min - 2 * space_y, f"Total distance: {obj_value:.2f}",
                 fontdict={'size': 12, 'color': 'red'})
        plt.xlim((x_min - space_x, x_max + space_x))
        plt.ylim((y_min - space_y, y_max + space_y))
        plt.title(f"Solution: {idx_pos + 1}, GBest: {solution[1]}")

        Path(pathsave).mkdir(parents=True, exist_ok=True)

        for idx, ext in enumerate(exts):
            plt.savefig(f"{pathsave}/{filename}-id{idx_pos + 1}{ext}", bbox_inches='tight')
        if platform.system() != "Linux":
            plt.show()
        plt.close()
