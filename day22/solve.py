from pathlib import Path
import re
import numpy as np

from collections import deque

MOVE_PAT = re.compile('\d+|[A-Z]')


def parse_board(lines):
    rows = []
    lines = lines.split('\n')

    max_length = max(len(line) for line in lines)

    for line in lines:
        row = [' .#'.index(c) for c in line]
        row.extend([0 for _ in range(max_length-len(row))])
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
    directions = deque((facings))

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

    r,c = pos

    return 1000*(r+1) + 4*(c+1) + facings.index(directions[0])


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
