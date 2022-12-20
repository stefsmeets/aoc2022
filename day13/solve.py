import json
from functools import cmp_to_key
from pathlib import Path


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


def part1(s: str):
    packets = [json.loads(line) for line in s.splitlines() if line]

    indices = []

    for i, (left, right) in enumerate(group_by_two(packets)):
        if cmp_packets(left, right) == 1:
            indices.append(i + 1)

    return sum(indices)


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


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
