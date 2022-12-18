from itertools import pairwise
from pathlib import Path


def parse_traces(lines):
    for line in lines:
        for start, stop in pairwise(line.split(' -> ')):
            start_x, start_y = (int(val) for val in start.split(','))
            stop_x, stop_y = (int(val) for val in stop.split(','))

            yield sorted((start_x, stop_x)), sorted((start_y, stop_y))


def scan_cave(s):
    traces = parse_traces(s.splitlines())

    cave = set()

    for (x1, x2), (y1, y2) in traces:
        cave |= {complex(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)}

    return cave


def solve(s, part1=False):
    cave = scan_cave(s)

    hole = 500
    abyss = max(pos.imag for pos in cave) + 1

    n_grains = 0
    grain = hole

    while hole not in cave:
        for new_pos in (grain + 1j, grain - 1 + 1j, grain + 1 + 1j):
            if part1 and (new_pos.imag == abyss):
                return n_grains
            elif new_pos.imag == abyss + 1:
                pass
            elif new_pos not in cave:
                grain = new_pos
                break
        else:
            cave.add(grain)
            n_grains += 1
            grain = hole

    return n_grains


def part1(s: str):
    return solve(s, part1=True)


def part2(s: str):
    return solve(s)


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt')

    print(part1(DATA))
    print(part2(DATA))
