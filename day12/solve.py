import argparse
from pathlib import Path

import networkx as nx
import numpy as np

from helpers import timeit


DATA = Path(__file__).with_name('data.txt')


def get_paths(grid, *, end):
    imax, jmax = np.array(grid.shape)

    G = nx.grid_2d_graph(imax, jmax, create_using=nx.DiGraph)
    G.remove_edges_from([(i, j) for i, j in G.edges if grid[j] - grid[i] > 1])

    return nx.shortest_path_length(G, target=end)


def setup(s: str):
    grid = np.array([[ord(c) for c in line] for line in s.splitlines()])
    start = tuple(*np.argwhere(grid == ord('S')))
    end = tuple(*np.argwhere(grid == ord('E')))

    grid[start] = ord('a')
    grid[end] = ord('z')

    return grid, end


@timeit
def part1(s: str):
    grid, end = setup(s)
    start = (0, 0)
    paths = get_paths(grid, end=end)
    return paths[start]


@timeit
def part2(s: str):
    grid, end = setup(s)
    starts = (tuple(start) for start in np.argwhere(grid == ord('a')))
    paths = get_paths(grid, end=end)
    return min(paths.get(start, np.inf) for start in starts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--parts', nargs='+', type=int,
        choices=(1, 2), default=(1, 2))
    parser.add_argument('data', nargs='?', default=DATA)
    args = parser.parse_args()

    data = Path(args.data).read_text()

    for i in args.parts:
        func = (..., part1, part2)[i]
        func(data)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
