from pathlib import Path

import numpy as np
import scipy.ndimage as ndi


def sides(x, y, z):
    return {(x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
            (x, y, z + 1),
            (x, y, z - 1)}


def exposed_faces(cubes):
    n_exposed = 0

    for x, y, z in cubes:
        n_exposed += len(sides(x, y, z) - cubes)

    return n_exposed


def part1(s: str):
    cubes = {tuple(int(val) for val in line.split(',')) for line in s.splitlines()}
    return exposed_faces(cubes)


def part2(s: str):
    cubes = np.array([[int(val) for val in line.split(',')] for line in s.splitlines()])

    space = np.zeros(cubes.max(axis=0) + 1)

    i, j, k = cubes.T
    space[i, j, k] = 1

    space = ndi.binary_fill_holes(space)

    cubes = set(zip(*np.where(space)))

    return exposed_faces(cubes)


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt')

    print(part1(DATA))
    print(part2(DATA))
