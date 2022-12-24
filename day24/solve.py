from itertools import count
from pathlib import Path

import numpy as np


def parse_field(s):
    _, *lines, _ = s.splitlines()

    shape = (len(lines), len(lines[0]) - 2)

    left = np.zeros(shape, bool)
    right = np.zeros(shape, bool)
    up = np.zeros(shape, bool)
    down = np.zeros(shape, bool)

    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            match char:
                case '>':
                    right[r, c - 1] = True
                case '<':
                    left[r, c - 1] = True
                case '^':
                    up[r, c - 1] = True
                case 'v':
                    down[r, c - 1] = True

    return left, right, up, down


def is_safe(field, pos):
    r, c = pos

    for dr, dc in (
        (-1, 0),
        (0, -1),
        (0, 0),
        (0, 1),
        (1, 0),
    ):
        tr = r + dr
        tc = c + dc

        if tr < 0 or tr == field.shape[0]:
            continue
        if tc < 0 or tc == field.shape[1]:
            continue

        if not field[tr, tc]:
            yield tr, tc


def part1(s: str):
    left, right, up, down = parse_field(s)

    shape = left.shape

    start = -1, 0
    stop = (shape[0] - 1, shape[1] - 1)

    safe = {start}

    for rnd in count(1):
        right = np.roll(right, 1, axis=1)
        left = np.roll(left, -1, axis=1)
        down = np.roll(down, 1, axis=0)
        up = np.roll(up, -1, axis=0)

        field = sum((right, left, down, up))

        new_safe = {start}
        for pos in safe:
            new_safe |= set(is_safe(field, pos))

        safe = new_safe

        if stop in safe:
            break

    return rnd + 1


def part2(s: str):
    lines = s.splitlines()

    for line in lines:
        pass

    # breakpoint()

    return 0


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
