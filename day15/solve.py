import argparse
import re
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path

from helpers import timeit

DATA = Path(__file__).with_name('data.txt')

INTEGER_PAT = re.compile('-?[0-9]+')


@dataclass
class Point:
    x: int
    y: int


def parse_line(line):
    x1, y1, x2, y2 = (int(val) for val in re.findall(INTEGER_PAT, line))
    return Point(x1, y1), Point(x2, y2)


def manh_dist(s, b):
    return abs(s.x - b.x) + abs(s.y - b.y)


def solve(s, rows, part1=False):
    lines = s.splitlines()

    for row in rows:
        ranges = []

        scanners, beacons = zip(*(parse_line(line) for line in lines))

        for s, b in zip(scanners, beacons):
            dist = manh_dist(s, b)

            proj = Point(s.x, row)

            if (proj_dist := manh_dist(s, proj)) > dist:
                continue

            delta = abs(dist - proj_dist)
            ranges.append((proj.x - delta, proj.x + delta + 1))

        if part1:
            beacons_on_row = len({b.x for b in beacons if b.y == row})
            mn = min(r[0] for r in ranges)
            mx = max(r[1] for r in ranges)
            return mx - mn - beacons_on_row

        ranges = sorted(ranges)
        max_col = 0

        for (start1, stop1), (start2, stop2) in pairwise(ranges):
            if start2 > max_col and start2 > stop1:
                return (stop1 * 4_000_000 + row)
            else:
                max_col = max(stop1, max_col)


@timeit
def part1(s):
    return solve(s, [2000000], part1=True)


@timeit
def part2(s):
    # return solve(s, range(2658764, 2658764 + 1))
    return solve(s, range(4000000))


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
