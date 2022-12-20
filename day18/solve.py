from pathlib import Path

import numpy as np
import scipy.ndimage as ndi


def solve(s: str, part2=False):
    cubes = np.loadtxt(s.splitlines(), delimiter=',', dtype=int)
    space = np.zeros(cubes.max(axis=0) + 1, bool)

    space[*cubes.T] = True

    if part2:
        space = ndi.binary_fill_holes(space)

    return sum(np.sum(np.diff(space, 1, i, False, False)) for i in (0, 1, 2))


def part1(s: str):
    return solve(s)


def part2(s: str):
    return solve(s, part2=True)


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
