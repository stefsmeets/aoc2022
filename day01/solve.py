import argparse
from pathlib import Path

from helpers import timeit


DATA = Path(__file__).with_name('data.txt')


def calc_calories(s):
    return (sum(int(val) for val in group.splitlines()) for group in s.split('\n\n'))


@timeit
def part1(s: str):
    calories = calc_calories(s)
    return max(calories)


@timeit
def part2(s: str):
    calories = calc_calories(s)
    return sum(sorted(calories)[-3:])


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
