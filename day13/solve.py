import argparse
import json
from functools import cmp_to_key
from pathlib import Path

from helpers import timeit


DATA = Path(__file__).with_name('data.txt')


def cmp_packets(left, right):
    match (left, right):
        case int(left), int(right):
            if left < right:
                return 1
            elif left > right:
                return -1
            else:
                return 0
        case int(), list():
            return cmp_packets([left], right)
        case list(), int():
            return cmp_packets(left, [right])
        case list(), list():
            for l, r in zip(left, right):
                ret = cmp_packets(l, r)
                if ret != 0:
                    return ret
            if len(right) > len(left):
                return 1
            elif len(right) < len(left):
                return -1
            else:
                return 0


def group_by_two(lst) -> list[tuple[str]]:
    args = [iter(lst)] * 2
    return list(zip(*args, strict=True))


@timeit
def part1(s: str):
    packets = [json.loads(line) for line in s.splitlines() if line]

    indices = []

    for i, (left, right) in enumerate(group_by_two(packets)):
        if cmp_packets(left, right) == 1:
            indices.append(i + 1)

    return sum(indices)


@timeit
def part2(s: str):
    packets = [json.loads(line) for line in s.splitlines() if line]

    div1 = [[2]]
    div2 = [[6]]

    packets.append(div1)
    packets.append(div2)

    sorted_packets = sorted(packets, key=cmp_to_key(cmp_packets), reverse=True)

    i1 = sorted_packets.index(div1) + 1
    i2 = sorted_packets.index(div2) + 1

    return i1 * i2


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
