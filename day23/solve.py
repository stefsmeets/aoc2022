from collections import Counter
from collections import deque
from itertools import count
from pathlib import Path


vectors = {
    'N': (-1, 0),
    'S': (1, 0),
    'W': (0, -1),
    'E': (0, 1),
    'NE': (-1, 1),
    'NW': (-1, -1),
    'SE': (1, 1),
    'SW': (1, -1),
}


def parse_field(s):
    field = set()

    for r, line in enumerate(s.splitlines()):
        for c, tile in enumerate(line):
            if tile == '#':
                field.add((r, c))

    return field


def all_empty(field, pos):
    r, c = pos
    for dr, dc in vectors.values():
        if (r + dr, c + dc) in field:
            return False
    return True


def move_allowed(field, pos, directions):
    r, c = pos
    for dr, dc in (vectors[d] for d in directions):
        nr, nc = r + dr, c + dc
        if (nr, nc) in field:
            return False

    return nr, nc


def move_n(field, pos):
    if new := move_allowed(field, pos, ('NE', 'NW', 'N')):
        return new


def move_s(field, pos):
    if new := move_allowed(field, pos, ('SE', 'SW', 'S')):
        return new


def move_w(field, pos):
    if new := move_allowed(field, pos, ('NW', 'SW', 'W')):
        return new


def move_e(field, pos):
    if new := move_allowed(field, pos, ('NE', 'SE', 'E')):
        return new


def solve(s: str, rounds):
    field = parse_field(s)

    moves = deque((move_n, move_s, move_w, move_e))

    for rnd in rounds:
        proposals = []

        for pos in field:
            if not all_empty(field, pos):
                for func in moves:
                    if new_pos := func(field, pos):
                        break
                else:
                    new_pos = pos
            else:
                new_pos = pos

            proposals.append(new_pos)

        c = Counter(proposals)

        new_field = set()

        for current, proposed in zip(field, proposals):
            new = proposed if c[proposed] == 1 else current
            new_field.add(new)

        if field == new_field:
            return rnd

        field = new_field

        moves.rotate(-1)

    rmin = min(r for r, c in field)
    cmin = min(c for r, c in field)
    rmax = max(r for r, c in field)
    cmax = max(c for r, c in field)

    area = (rmax - rmin + 1) * (cmax - cmin + 1)

    return area - len(field)


def part1(s: str):
    return solve(s, rounds=range(10))


def part2(s: str):
    return solve(s, rounds=count(1))


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
