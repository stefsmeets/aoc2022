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
        ('top', up): ('bot', down),
        ('top', down): ('front', down),
        ('top', left): ('left', right),
        ('top', right): ('right', left),

        ('bot', up): ('front', up),
        ('bot', down): ('back', up),
        ('bot', left): ('right', up),
        ('bot', right): ('right', right),

        ('left', up): ('top', right),
        ('left', down): ('bot', right),
        ('left', left): ('back', left),
        ('left', right): ('front', right),

        ('right', up): ('front', left),
        ('right', down): ('back', right),
        ('right', left): ('bot', left),
        ('right', right): ('top', left),

        ('front', up): ('top', up),
        ('front', down): ('bot', down),
        ('front', left): ('left', left),
        ('front', right): ('right', down),

        ('back', up): ('top', down),
        ('back', down): ('bot', up),
        ('back', left): ('right', up),
        ('back', right): ('left', right),
    }

    def teleport(pos, d, side):
        new_side, new_d = portals[side, d]

        r, c = pos

        dr, dc = d
        ndr, ndc = new_d

        ro, co = origins[side]
        nro, nco = origins[new_side]

        # convert to origin
        rr = r - ro
        cc = c - co - dc

        if d == new_d:
            pass
        elif abs(dr) and (dr == -ndr):
            rr -= 1
            cc = ln - cc - 1
        elif abs(dc) and (dc == -ndc):
            cc -= 1
            rr = ln - rr - 1
        else:
            c_tmp = cc
            r_tmp = rr
            rr = ln - c_tmp - 1
            cc = ln - r_tmp - 1

        new_pos = (nro + rr, nco + cc)

        if new_pos == (8, 2):
            breakpoint()

        return new_pos, new_d, new_side

    def find_new_pos(pos, d, side, *, max_n):
        print()
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

            print(n, max_n, side, (tr, tc), (dr, dc))

            if tr in (-1, max_r):
                print('max r reached')

                (r, c), (dr, dc), side = teleport((tr, tc), d, side)
                max_n -= n
                n = 0

            elif tc in (-1, max_c):
                print('max c reached')

                (r, c), (dr, dc), side = teleport((tr, tc), d, side)
                max_n -= n
                n = 0

            elif board[tr, tc] == 0:  # wrap
                (r, c), (dr, dc), side = teleport((tr, tc), d, side)
                print(f'teleported to {(r, c)} at {side=} facing: {(dr, dc)}')
                max_n -= n
                n = 0

            elif board[tr, tc] == 1:  # open
                print('accepted')
                accepted = ((tr, tc), (dr, dc), side)

            elif board[tr, tc] == 2:  # rock
                print('rock')
                break

            n += 1

        return accepted

    for instruction in route:
        match instruction:
            case 'move', n:
                d = directions[0]

                (pos, new_d, side) = find_new_pos(pos, d, side, max_n=n)

                print('facing', new_d)

                while directions[0] != new_d:
                    directions.rotate()

                print('new position:', pos, 'at', side, 'facing', directions[0], new_d)
            case 'turn', 'L':
                directions.rotate()
                print('\nrotating L', directions[0])
            case 'turn', 'R':
                directions.rotate(-1)
                print('\nrotating R', directions[0])

    r, c = pos

    return 1000 * (r + 1) + 4 * (c + 1) + facings.index(directions[0])


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
