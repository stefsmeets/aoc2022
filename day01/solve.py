import argparse
from pathlib import Path

from helpers import timeit


DATA = Path(__file__).with_name('data.txt')


def calc_elves(lines):
    elves = []
    tot = 0

    for calories in lines:
        if not calories:
            elves.append(tot)
            tot = 0
        else:
            tot += int(calories)

    return elves


@timeit
def part1(s: str):
    lines = s.splitlines()
    elves = calc_elves(lines)
    return max(elves)


@timeit
def part2(s: str):
    lines = s.splitlines()
    elves = calc_elves(lines)
    elves = sorted(elves, reverse=True)

    return elves[0] + elves[1] + elves[2]


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
