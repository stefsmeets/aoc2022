import re
from collections import deque
from pathlib import Path

import numpy as np


MOVE_PAT = re.compile(r'\d+|[A-Z]')


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


def part1(s: str):
    board_lines, route_line = s.split('\n\n')

    board = parse_board(board_lines)
    route = parse_route(route_line)

    #          right    down    left       up
    facings = ((0, 1), (1, 0), (0, -1), (-1, 0))
    directions = deque(facings)

    max_r, max_c = board.shape

    pos = 0, list(board[0]).index(1)

    def find_new_pos(pos, d, max_n):
        r, c = best_pos = pos
        dr, dc = d
        n = 1

        while n <= max_n:
            tr = (r + dr * n) % max_r
            tc = (c + dc * n) % max_c

            match board[tr, tc]:
                case 2:
                    break
                case 1:
                    best_pos = tr, tc
                case 0:
                    max_n += 1

            n += 1

        return best_pos

    for instruction in route:
        match instruction:
            case 'move', n:
                d = directions[0]
                pos = find_new_pos(pos, d, n)
            case 'turn', 'L':
                directions.rotate()
            case 'turn', 'R':
                directions.rotate(-1)

    r, c = pos

    return 1000 * (r + 1) + 4 * (c + 1) + facings.index(directions[0])


def part2(s: str):
    board_lines, route_line = s.split('\n\n')

    board = parse_board(board_lines)
    route = parse_route(route_line)

    # test case
    if board.shape == (12, 16):
        ln = 4
        origins = {
            'top': (0 * ln, 2 * ln),

            'back': (1 * ln, 0 * ln),
            'left': (1 * ln, 1 * ln),
            'front': (1 * ln, 2 * ln),

            'bot': (2 * ln, 2 * ln),
            'right': (2 * ln, 3 * ln),
        }
    else:
        ln = 50
        origins = {
            'top': (0 * ln, 1 * ln),
            'right': (0 * ln, 2 * ln),

            'front': (1 * ln, 1 * ln),

            'left': (2 * ln, 0 * ln),
            'bot': (2 * ln, 1 * ln),

            'back': (3 * ln, 0 * ln),
        }

    def get_side(pos):
        r, c = pos
        for side, (ro, co) in origins.items():
            if ro <= r < ro + ln and co <= c < co + ln:
                return side
        raise ValueError(f'Cannot place {r,c}')

    right = (0, 1)
    down = (1, 0)
    left = (0, -1)
    up = (-1, 0)

    facings = (right, down, left, up)

    directions = deque(facings)

    max_r, max_c = board.shape

    pos = 0, list(board[0]).index(1)

    side = 'top'

    portals = {
        ('top', up): ('back', right),
        ('top', down): ('front', down),
        ('top', left): ('left', right),
        ('top', right): ('right', right),

        ('bot', up): ('front', up),
        ('bot', down): ('back', left),
        ('bot', left): ('left', left),
        ('bot', right): ('right', left),

        ('left', up): ('front', right),
        ('left', down): ('back', down),
        ('left', left): ('top', right),
        ('left', right): ('bot', right),

        ('right', up): ('back', up),
        ('right', down): ('front', left),
        ('right', left): ('top', left),
        ('right', right): ('bot', left),

        ('front', up): ('top', up),
        ('front', down): ('bot', down),
        ('front', left): ('left', down),
        ('front', right): ('right', up),

        ('back', up): ('left', up),
        ('back', down): ('right', down),
        ('back', left): ('top', down),
        ('back', right): ('bot', up),
    }

    def teleport(pos, d, side):
        new_side, new_d = portals[side, d]

        r, c = pos

        dr, dc = d
        ndr, ndc = new_d

        ro, co = origins[side]
        nro, nco = origins[new_side]

        # convert to origin
        rr = r - ro - dr
        cc = c - co - dc

        if d == new_d:
            new_r = nro + rr
            new_c = nco + cc + 1
        elif abs(dr) and (dr == -ndr):
            new_r = nro + rr - 1
            new_c = nco + ln - cc - 1
        elif abs(dc) and (dc == -ndc):
            new_c = nco + cc - 1
            new_r = nro + ln - rr - 1
        elif dc == -1 and ndr == 1:
            new_r = nro + cc - 1
            new_c = nco + rr
        elif dr == -1 and ndc == 1:
            new_r = nro + cc
            new_c = nco + rr
        elif dr == 1 and ndc == -1:
            new_r = nro + cc
            new_c = nco + rr + 1
        elif dc == 1 and ndr == -1:
            new_r = nro + cc + 1
            new_c = nco + rr
        else:
            new_r = nro + ln - cc - 1
            new_c = nco + ln - rr - 1

        new_pos = new_r, new_c

        return new_pos, new_d, new_side

    def find_new_pos(pos, d, side, *, max_n):
        r, c = pos

        accepted = (pos, d, side)

        dr, dc = d
        n = 1

        while n <= max_n:
            tr = (r + dr * n)
            tc = (c + dc * n)

            try:
                side = get_side((tr, tc))
            except ValueError:
                pass

            if tr in (-1, max_r) or tc in (-1, max_c):
                (r, c), (dr, dc), side = teleport((tr, tc), d, side)

            if board[tr, tc] == 0:  # wrap
                (r, c), (dr, dc), side = teleport((tr, tc), d, side)
                max_n = max_n - n + 1
                n = 0

            elif board[tr, tc] == 1:  # open
                accepted = ((tr, tc), (dr, dc), side)

            elif board[tr, tc] == 2:  # rock
                break

            print(pos)

            n += 1

        return accepted

    for i, instruction in enumerate(route):
        match instruction:
            case 'move', n:
                d = directions[0]
                (pos, new_d, side) = find_new_pos(pos, d, side, max_n=n)
            case 'turn', 'L':
                directions.rotate()
            case 'turn', 'R':
                directions.rotate(-1)

    r, c = pos

    return 1000 * (r + 1) + 4 * (c + 1) + facings.index(directions[0])


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()
