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

        if tr < 0 or tr >= field.shape[0]:
            continue
        if tc < 0 or tc >= field.shape[1]:
            continue

        if not field[tr, tc]:
            yield tr, tc


def its_gusty_here(gusts):
    left, right, up, down = gusts

    right = np.roll(right, 1, axis=1)
    left = np.roll(left, -1, axis=1)
    down = np.roll(down, 1, axis=0)
    up = np.roll(up, -1, axis=0)

    return left, right, up, down


def find_shortest_path(gusts, start, stop):
    safe = {start}

    for rnd in count(1):
        gusts = its_gusty_here(gusts)
        gust_map = sum(gusts)

        new_safe = {start}

        for pos in safe:
            new_safe |= set(is_safe(gust_map, pos))

        safe = new_safe

        if stop in safe:
            break

    gusts = its_gusty_here(gusts)

    return rnd + 1, gusts


def part1(s: str):
    gusts = parse_field(s)

    max_r, max_c = gusts[0].shape

    start = -1, 0
    stop = (max_r - 1, max_c - 1)

    rnd, gusts = find_shortest_path(gusts, start, stop)

    return rnd


def part2(s: str):
    gusts = parse_field(s)

    max_r, max_c = gusts[0].shape

    rounds = []

    for start, stop in (
        ((-1, 0), (max_r - 1, max_c - 1)),
        ((max_r, max_c - 1), (0, 0)),
        ((-1, 0), (max_r - 1, max_c - 1)),
    ):
        rnd, gusts = find_shortest_path(gusts, start, stop)
        rounds.append(rnd)

    return sum(rounds)


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
