import argparse
from pathlib import Path

import numpy as np
import scipy.ndimage as ndi

from helpers import timeit


DATA = Path(__file__).with_name('data.txt')


def sides(x,y,z):
    return {(x+1,y,z),
     (x-1,y,z),
     (x,y+1,z),
     (x,y-1,z),
     (x,y,z+1),
     (x,y,z-1)}


def exposed_faces(cubes):
    n_exposed = 0

    for x,y,z in cubes:
        n_exposed += len(sides(x,y,z) - cubes)

    return n_exposed


@timeit
def part1(s: str):
    cubes = {tuple(int(val) for val in line.split(',')) for line in s.splitlines()}
    return exposed_faces(cubes)


@timeit
def part2(s: str):
    cubes = np.array([[int(val) for val in line.split(',')] for line in s.splitlines()])

    space = np.zeros(cubes.max(axis=0) + 1)

    i, j, k = cubes.T
    space[i, j, k] = 1

    space = ndi.binary_fill_holes(space)

    cubes = set(zip(*np.where(space)))

    return exposed_faces(cubes)


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
