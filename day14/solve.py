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

    cave = {}

    for (x1, x2), (y1, y2) in traces:

        if x1 == x2:
            for y in range(y1, y2 + 1):
                cave[x1, y] = '#'

        if y1 == y2:
            for x in range(x1, x2 + 1):
                cave[x, y1] = '#'

    return cave


def solve(s, part2=False):
    cave = scan_cave(s)
    hole = (500, 0)
    abyss = max(y for x, y in cave.keys()) + 1

    def test_part1():
        return grain_y < abyss

    def test_part2():
        return hole not in cave

    test = test_part2 if part2 else test_part1

    grain_x, grain_y = hole

    while test():
        for x, y in (
                    (grain_x, grain_y + 1),
                    (grain_x - 1, grain_y + 1),
                    (grain_x + 1, grain_y + 1),
        ):
            if part2 and (y == abyss + 1):
                pass
            elif (x, y) not in cave:
                grain_x, grain_y = x, y
                break
        else:
            cave[grain_x, grain_y] = '.'
            grain_x, grain_y = hole

    return sum(v == '.' for v in cave.values())


@timeit
def part1(s: str):
    return solve(s)


@timeit
def part2(s: str):
    return solve(s, part2=True)


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
