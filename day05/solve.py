import argparse
from collections import defaultdict
from pathlib import Path

from helpers import timeit


DATA = Path(__file__).with_name('data.txt').read_text()


def get_stacks(setup):
    NO_CRATE = ' '

    stacks = defaultdict(list)

    positions = [(i, pos) for i, pos in enumerate(setup[-1]) if pos != ' ']

    for line in reversed(setup[:-1]):
        for i, pos in positions:
            crate = line[i]
            if crate == NO_CRATE:
                continue

            stacks[pos].append(crate)

    return stacks


def setup(lines):
    header = []
    for i, line in enumerate(lines):
        if not line:
            break
        header.append(line)

    stacks = get_stacks(header)

    instructions = lines[i + 1:]

    return stacks, instructions


@timeit
def part1(s: str):
    lines = s.splitlines()
    stacks, instructions = setup(lines)

    for instruction in instructions:
        _, num, _, src, _, dst = instruction.split()
        num = int(num)

        for step in range(num):
            crate = stacks[src].pop()
            stacks[dst].append(crate)

    return ''.join(stack.pop() for stack in stacks.values())


@timeit
def part2(s: str):
    lines = s.splitlines()
    stacks, instructions = setup(lines)

    for instruction in instructions:
        _, num, _, src, _, dst = instruction.split()
        num = int(num)

        crates = list(reversed([stacks[src].pop() for step in range(num)]))
        stacks[dst].extend(crates)

    return ''.join(stack.pop() for stack in stacks.values())


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
