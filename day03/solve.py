import argparse
from pathlib import Path

from helpers import timeit


DATA = Path(__file__).with_name('data.txt').read_text()


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
        common = set(a) & set(b)
        assert len(common) == 1
        item = tuple(common)[0]

        index = 96 if item.islower() else 38

        value = ord(item) - index

        result += value

    return result


@timeit
def part2(s: str):
    lines = s.splitlines()

    result = 0

    for group in group_by_three(lines):
        a, b, c = (set(line) for line in group)
        common = set(a) & set(b) & set(c)
        assert len(common) == 1
        item = tuple(common)[0]

        index = 96 if item.islower() else 38

        value = ord(item) - index

        result += value

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
