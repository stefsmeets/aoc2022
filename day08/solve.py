import argparse
from pathlib import Path

import numpy as np

from helpers import timeit


DATA = Path(__file__).with_name('data.txt')


@timeit
def part1(s: str):
    forest = np.array([[int(val) for val in line] for line in s.splitlines()])

    visible = np.zeros_like(forest)

    imax, jmax = forest.shape

    for (i, j), h in np.ndenumerate(forest):
        visible[i, j] = any((
            np.all(forest[0:i, j] < h),
            np.all(forest[i + 1:imax, j] < h),
            np.all(forest[i, 0:j] < h),
            np.all(forest[i, j + 1:jmax] < h),









        ))

    return visible.sum()


def score(r, h):
    score = 0
    for x in r:
        score += 1
        if x >= h:
            break

    return score


@timeit
def part2(s: str):
    forest = np.array([[int(val) for val in line] for line in s.splitlines()])

    scenic_scores = np.zeros_like(forest)
    imax, jmax = forest.shape

    for (i, j), h in np.ndenumerate(forest):
        scenic_scores[i, j] = np.prod([
            score(forest[0:i, j][::-1], h),
            score(forest[i + 1:imax, j], h),
            score(forest[i, 0:j][::-1], h),
            score(forest[i, j + 1:jmax], h),
        ])

    return scenic_scores.max()


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
