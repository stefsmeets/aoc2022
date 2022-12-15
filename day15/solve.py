import argparse
import re
from itertools import pairwise
from pathlib import Path

from helpers import timeit

DATA = Path(__file__).with_name('data.txt')

INTEGER_PAT = re.compile('-?[0-9]+')


def parse_line(line):
    sx, sy, bx, by = (int(val) for val in re.findall(INTEGER_PAT, line))
    return (sx, sy), (bx, by), abs(sx - bx) + abs(sy - by)


def solve(s, rows, part1=False):
    lines = s.splitlines()

    scanners, beacons, distances = zip(*(parse_line(line) for line in lines))

    for row in rows:
        ranges = []

        for (sx, sy), dist in zip(scanners, distances):
            proj_dist = sy - row

            if proj_dist > dist:
                continue

            ranges.append(((sx + abs(proj_dist) - dist),
                           (sx - abs(proj_dist) + dist + 1)),
                          )

        if part1:
            beacons_on_row = len({bx for (bx, by) in beacons if by == row})
            r1, r2 = zip(*ranges)
            return max(r2) - min(r1) - beacons_on_row

        ranges = sorted(ranges)
        max_col = 0

        for (start1, stop1), (start2, stop2) in pairwise(ranges):
            if start2 > max_col and start2 > stop1:
                return (stop1 * 4_000_000 + row)
            else:
                max_col = max(stop1, max_col)


@timeit
def part1(s):
    # 5125700
    return solve(s, [2000000], part1=True)


@timeit
def part2(s):
    # 11379390658764
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
