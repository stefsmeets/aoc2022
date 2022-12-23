import re
from pathlib import Path

import numpy as np


MOVE_PAT = re.compile(r'\d+|[A-Z]')

RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP = (-1, 0)
LENGTH = 50


def parse_board(lines):
    rows = []
    lines = lines.split('\n')

    max_length = max(len(line) for line in lines)

    for line in lines:
        row = [' .#'.index(c) for c in line]
        row.extend([0 for _ in range(max_length - len(row))])
        rows.append(row)

    return np.array(rows)


def parse_route(line):
    line = line.strip()

    route = []

    for step in MOVE_PAT.findall(line):
        try:
            step = int(step)
            route.append(('move', int(step)))
        except ValueError:
            route.append(('turn', step))

    return route


def solve(s: str, *, portals):
    *board_lines, _, route_line = s.split()

    full_board = parse_board(board_lines)
    route = parse_route(route_line)

    origins = {
        'top': (0 * LENGTH, 1 * LENGTH),
        'right': (0 * LENGTH, 2 * LENGTH),

        'front': (1 * LENGTH, 1 * LENGTH),

        'left': (2 * LENGTH, 0 * LENGTH),
        'bot': (2 * LENGTH, 1 * LENGTH),

        'back': (3 * LENGTH, 0 * LENGTH),
    }

    subboards = {key: full_board[ro:ro + LENGTH, co:co + LENGTH] for key, (ro, co) in origins.items()}

    facings = (RIGHT, DOWN, LEFT, UP)

    def rotate_right(facing):
        i = facings.index(facing)
        return facings[(i + 1) % 4]

    def rotate_left(facing):
        i = facings.index(facing)
        return facings[(i - 1) % 4]

    def teleport(pos, facing, side):
        new_side, new_facing, f = portals[side, facing]
        new_pos = f(*pos)

        return new_pos, new_facing, new_side

    def find_new_pos(pos, facing, side, *, max_n):
        accepted = (pos, facing, side)
        board = subboards[side]

        for n in range(max_n):
            dr, dc = facing
            r, c = pos
            new_side = side

            tr = r + dr
            tc = c + dc

            if tr in (-1, LENGTH) or tc in (-1, LENGTH):
                (tr, tc), (dr, dc), new_side = teleport((r, c), (dr, dc), side)
                board = subboards[new_side]

            if board[tr, tc] == 1:  # open
                pos = (tr, tc)
                facing = (dr, dc)
                side = new_side

                accepted = (pos, facing, side)

            elif board[tr, tc] == 2:  # rock
                break

            elif board[tr, tc] == 0:
                raise ValueError('This should no longer happen')

        return accepted

    side = 'top'
    pos = 0, 0
    facing = facings[0]

    for i, instruction in enumerate(route):
        match instruction:
            case 'move', n:
                (pos, facing, side) = find_new_pos(pos, facing, side, max_n=n)
            case 'turn', 'L':
                facing = rotate_left(facing)
            case 'turn', 'R':
                facing = rotate_right(facing)

    ro, rc = origins[side]
    r, c = pos

    return 1000 * (ro + r + 1) + 4 * (rc + c + 1) + facings.index(facing)


def part1(s: str):
    going_down = lambda r, c: (0, c)
    going_up = lambda r, c: (LENGTH - 1, c)
    going_left = lambda r, c: (r, LENGTH -1)
    going_right = lambda r, c: (r, 0)

    portals = {
        ('top', UP): ('bot', UP, going_up),
        ('top', DOWN): ('front', DOWN, going_down),
        ('top', LEFT): ('right', LEFT, going_left),
        ('top', RIGHT): ('right', RIGHT, going_right),
        ('bot', UP): ('front', UP, going_up),
        ('bot', DOWN): ('top', DOWN, going_down),
        ('bot', LEFT): ('left', LEFT, going_left),
        ('bot', RIGHT): ('left', RIGHT, going_right),
        ('left', UP): ('back', UP, going_up),
        ('left', DOWN): ('back', DOWN, going_down),
        ('left', LEFT): ('bot', LEFT, going_left),
        ('left', RIGHT): ('bot', RIGHT, going_right),
        ('right', UP): ('right', UP, going_up),
        ('right', DOWN): ('right', DOWN, going_down),
        ('right', LEFT): ('top', LEFT, going_left),
        ('right', RIGHT): ('top', RIGHT, going_right),
        ('front', UP): ('top', UP, going_up),
        ('front', DOWN): ('bot', DOWN, going_down),
        ('front', LEFT): ('front', LEFT, going_left),
        ('front', RIGHT): ('front', RIGHT, going_right),
        ('back', UP): ('left', UP, going_up),
        ('back', DOWN): ('left', DOWN, going_down),
        ('back', LEFT): ('back', LEFT, going_left),
        ('back', RIGHT): ('back', RIGHT, going_right),
    }
    return solve(s, portals=portals)


def part2(s: str):
    portals = {
        ('top', UP): ('back', RIGHT, lambda r, c: (c, 0)),
        ('top', DOWN): ('front', DOWN, lambda r, c: (0, c)),
        ('top', LEFT): ('left', RIGHT, lambda r, c: (LENGTH - 1 - r, c)),
        ('top', RIGHT): ('right', RIGHT, lambda r, c: (r, 0)),
        ('bot', UP): ('front', UP, lambda r, c: (LENGTH - 1, c)),
        ('bot', DOWN): ('back', LEFT, lambda r, c: (c, LENGTH - 1)),
        ('bot', LEFT): ('left', LEFT, lambda r, c: (r, LENGTH - 1)),
        ('bot', RIGHT): ('right', LEFT, lambda r, c: (LENGTH - 1 - r, c)),
        ('left', UP): ('front', RIGHT, lambda r, c: (c, 0)),
        ('left', DOWN): ('back', DOWN, lambda r, c: (0, c)),
        ('left', LEFT): ('top', RIGHT, lambda r, c: (LENGTH - 1 - r, c)),
        ('left', RIGHT): ('bot', RIGHT, lambda r, c: (r, 0)),
        ('right', UP): ('back', UP, lambda r, c: (LENGTH - 1, c)),
        ('right', DOWN): ('front', LEFT, lambda r, c: (c, LENGTH - 1)),
        ('right', LEFT): ('top', LEFT, lambda r, c: (r, LENGTH - 1)),
        ('right', RIGHT): ('bot', LEFT, lambda r, c: (LENGTH - 1 - r, c)),
        ('front', UP): ('top', UP, lambda r, c: (LENGTH - 1, c)),
        ('front', DOWN): ('bot', DOWN, lambda r, c: (0, c)),
        ('front', LEFT): ('left', DOWN, lambda r, c: (0, r)),
        ('front', RIGHT): ('right', UP, lambda r, c: (LENGTH - 1, r)),
        ('back', UP): ('left', UP, lambda r, c: (LENGTH - 1, c)),
        ('back', DOWN): ('right', DOWN, lambda r, c: (0, c)),
        ('back', LEFT): ('top', DOWN, lambda r, c: (0, r)),
        ('back', RIGHT): ('bot', UP, lambda r, c: (LENGTH - 1, r)),
    }
    return solve(s, portals=portals)


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
