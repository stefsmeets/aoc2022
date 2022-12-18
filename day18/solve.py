from pathlib import Path

import numpy as np
import scipy.ndimage as ndi


def solve(s: str, part2=False):
    cubes = np.array([[int(val) for val in line.split(',')] for line in s.splitlines()])
    space = np.zeros(cubes.max(axis=0) + 1)

    space[*cubes.T] = 1

    if part2:
        space = ndi.binary_fill_holes(space)

    n_exposed = 0

    for axis in (0, 1, 2):
        n_exposed += np.sum(np.abs(np.diff(space, 1, axis, 0, 0)))

    return int(n_exposed)


def part1(s: str):
    return solve(s)


def part2(s: str):
    return solve(s, part2=True)


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt')

    print(part1(DATA))
    print(part2(DATA))
