from collections import defaultdict
from pathlib import Path


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


def setup(s):
    lines = s.splitlines()

    header = []
    for i, line in enumerate(lines):
        if not line:
            break
        header.append(line)

    stacks = get_stacks(header)

    instructions = lines[i + 1:]

    return stacks, instructions


def crate_mover(s: str, version: int = 9000):
    stacks, instructions = setup(s)

    for instruction in instructions:
        _, num, _, src, _, dst = instruction.split()
        num = int(num)

        crates = [stacks[src].pop() for step in range(num)]
        if version == 9001:
            crates = list(reversed(crates))

        stacks[dst].extend(crates)

    return ''.join(stack.pop() for stack in stacks.values())


def part1(s: str):
    return crate_mover(s, version=9000)


def part2(s: str):
    return crate_mover(s, version=9001)


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
