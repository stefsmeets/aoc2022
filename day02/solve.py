import argparse
import os
from pathlib import Path

import numpy as np

from helpers import timeit


DATA = Path(__file__).with_name('data.txt')


@timeit
def part1(s: str):
    lines = s.splitlines()

    total_score = 0

    points = {'X': 1, 'Y': 2, 'Z': 3}

    for line in lines:
        left, right = line.split()
        round_score = points[right]
        match left, right:
            # losses
            case ('A', 'Z') | ('B', 'X') | ('C', 'Y'):
                round_score += 0
            # draws
            case ('A', 'X') | ('B', 'Y') | ('C', 'Z'):
                round_score += 3
            # wins
            case ('A', 'Y') | ('B', 'Z') | ('C', 'X'):
                round_score += 6

        total_score += round_score

    return total_score


@timeit
def part2(s: str):
    lines = s.splitlines()

    total_score = 0

    points = {'X': 0, 'Y': 3, 'Z': 6}

    for line in lines:
        left, right = line.split()
        round_score = points[right]
        match left, right:
            case ('A', 'Y') | ('B', 'X') | ('C', 'Z'):
                round_score += 1
            case ('A', 'Z') | ('B', 'Y') | ('C', 'X'):
                round_score += 2
            case ('A', 'X') | ('B', 'Z') | ('C', 'Y'):
                round_score += 3

        total_score += round_score

    return total_score


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
