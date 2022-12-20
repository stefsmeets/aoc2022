from collections import deque
from pathlib import Path


def parse(s):
    lines = s.splitlines()

    q = deque()

    for line in lines:
        match line.split():
            case ('addx', val):
                q.append(('noop', None))
                q.append(('addx', int(val)))
            case ('noop',):
                q.append(('noop', None))

    return q


def reshape(lst, *, h, w):
    assert h * w == len(lst)

    rows = []
    for i in range(h):
        rows.append(lst[i * w:(i + 1) * w])

    return rows


def part1(s: str):
    q = parse(s)

    X = 1
    cycle = 1
    signal_strength = []

    def update_signal(cycle):
        if cycle in (20, 60, 100, 140, 180, 220):
            signal_strength.append(cycle * X)

    while q:
        op, arg = q.popleft()

        update_signal(cycle)

        cycle += 1

        if op == 'addx':
            X += arg

    return sum(signal_strength)


def part2(s: str):
    q = parse(s)

    X = 1
    cycle = 1
    signal = []

    def update_signal(cycle):
        pixel = (cycle - 1) % 40
        draw = abs(pixel - X) <= 1
        signal.append(draw)

    while q:
        op, arg = q.popleft()

        update_signal(cycle)

        cycle += 1

        if op == 'addx':
            X += arg

    answer = '\n\n'
    for row in reshape(signal, h=6, w=40):
        answer += ''.join([' #'[draw] for draw in row])
        answer += '\n'

    return answer


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
