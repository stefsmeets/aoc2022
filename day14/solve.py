import argparse
from itertools import pairwise
from pathlib import Path

from helpers import timeit


DATA = Path(__file__).with_name('data.txt')


def parse_traces(lines):
    for line in lines:
        for start, stop in pairwise(line.split(' -> ')):
            start_x, start_y = (int(val) for val in start.split(','))
            stop_x, stop_y = (int(val) for val in stop.split(','))

            yield sorted((start_x, stop_x)), sorted((start_y, stop_y))


def scan_cave(s):
    traces = parse_traces(s.splitlines())

    cave = set()

    for (x1, x2), (y1, y2) in traces:
        cave |= {complex(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)}

    return cave


def solve(s, part1=False):
    cave = scan_cave(s)
    hole = 500
    abyss = max(pos.imag for pos in cave) + 1

    grain = complex(hole)
    n_grains = 0

    while hole not in cave:
        for new_pos in (grain + 1j, grain - 1 + 1j, grain + 1 + 1j):
            if new_pos.imag == abyss:
                if part1:
                    return n_grains
                pass  # part2
            elif new_pos not in cave:
                grain = new_pos
                break
        else:
            cave.add(grain)
            n_grains += 1
            grain = complex(hole)

    return n_grains


@timeit
def part1(s: str):
    return solve(s, part1=True)


@timeit
def part2(s: str):
    return solve(s)


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
