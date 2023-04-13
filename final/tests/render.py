#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
import matplotlib.pyplot as plt


parser = ArgumentParser()
parser.add_argument("n_values_dirpath")
parser.add_argument("single_dirpath")
parser.add_argument("multi_dirpath")
parser.add_argument("plot_filepath")
args = parser.parse_args()

n_values_dirpath = args.n_values_dirpath
single_dirpath = args.single_dirpath
multi_dirpath = args.multi_dirpath
plot_filepath = args.plot_filepath


allowed_x_values = [int(filepath.stem) for filepath in Path(n_values_dirpath).iterdir()]


def parse_results_folder(dirpath: Path):
    x_values = []
    y_values = []
    for filepath in dirpath.iterdir():
        x_value = int(filepath.stem)
        if x_value not in allowed_x_values:
            continue
        x_values.append(x_value)
        with filepath.open() as f:
            val = f.read().strip()
            y_values.append(int(val) if val.isnumeric() else None)
    return (x_values, y_values)


def main():
    single_results = parse_results_folder(Path(single_dirpath))
    multi_names, multi_results = zip(
        *sorted(
            [
                (dirpath.stem, parse_results_folder(dirpath))
                for dirpath in Path("./tests/results/multi").iterdir()
            ],
            key=lambda t: int(t[0]),
        )
    )

    ax = plt.gca()

    ax.set_xscale("log")
    ax.xaxis.set_ticks(single_results[0])

    plt.plot(*single_results)

    for xs, ys in multi_results:
        plt.plot(xs, ys)

    plt.legend(labels=("1*", *multi_names))

    plt.savefig(plot_filepath)


if __name__ == "__main__":
    main()
