import argparse
import os
from pathlib import Path

import numpy as np

from helpers import timeit


DATA = Path(__file__).with_name('data.txt')


def solve(s, *, markersize):
    line = s.splitlines()[0]

    for start in range(len(line)):
        stop = start + markersize
        marker = set(line[start: stop])
        if len(marker) == markersize:
            break

    return stop


@timeit
def part1(s: str):
    return solve(s, markersize=4)


@timeit
def part2(s: str):
    return solve(s, markersize=14)


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
