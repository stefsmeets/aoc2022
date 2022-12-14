import argparse
import string
from pathlib import Path

from helpers import timeit


DATA = Path(__file__).with_name('data.txt')

LETTERS = '_' + string.ascii_lowercase + string.ascii_uppercase


def split_in_two(lst):
    n = int(len(lst) / 2)

    a = lst[:n]
    b = lst[n:]
    assert len(a) == len(b), (a, b)

    return a, b


def group_by_three(lst) -> list[tuple[str]]:
    args = [iter(lst)] * 3
    return list(zip(*args, strict=True))


@timeit
def part1(s: str):
    lines = s.splitlines()

    result = 0

    for line in lines:
        a, b = split_in_two(line)
        letter = (set(a) & set(b)).pop()
        result += LETTERS.index(letter)

    return result


@timeit
def part2(s: str):
    lines = s.splitlines()

    result = 0

    for a, b, c in group_by_three(lines):
        letter = (set(a) & set(b) & set(c)).pop()
        result += LETTERS.index(letter)

    return result


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
