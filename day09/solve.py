import argparse
from collections import defaultdict
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path

from helpers import timeit


DATA = Path(__file__).with_name('data.txt')


def parse_line(line):
    inp = line.split()
    return inp[0], int(inp[1])


@dataclass
class Knot:
    x: int = 0
    y: int = 0


def solve(s, n_knots):
    lines = (parse_line(line) for line in s.splitlines())

    knots = [Knot() for _ in range(n_knots)]
    tail_pos = defaultdict(int)

    moves = {
        'U': (0, 1),
        'D': (0, -1),
        'L': (-1, 0),
        'R': (1, 0),
    }

    for direction, n_steps in lines:
        dx, dy = moves[direction]

        for step in range(n_steps):
            knots[0].x += dx
            knots[0].y += dy

            for (H, T) in pairwise(knots):
                if abs(H.x - T.x) > 1 or abs(H.y - T.y) > 1:

                    if H.x != T.x:
                        T.x += (-1, 1)[H.x > T.x]

                    if H.y != T.y:
                        T.y += (-1, 1)[H.y > T.y]

            tail_pos[T.x, T.y] = 1

    return sum(tail_pos.values())


@timeit
def part1(s: str):
    return solve(s, n_knots=2)


@timeit
def part2(s: str):
    return solve(s, n_knots=10)


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
