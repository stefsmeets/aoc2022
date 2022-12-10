import argparse
from pathlib import Path

from helpers import timeit


DATA = Path(__file__).with_name('data.txt')


@timeit
def part1(s: str):
    lines = s.splitlines()

    register = {'X': 1}
    cycle = 1
    signal_strength = {}

    def update_signal(cycle):
        if cycle % 20 == 0:
            val = register['X']
            signal_strength[cycle] = val * cycle

    for line in lines:
        match line.split():
            case ('addx', val):
                val = int(val)
                cycle += 1
                update_signal(cycle)
                cycle += 1
                register['X'] += val
                update_signal(cycle)
            case ('noop', ):
                cycle += 1
                update_signal(cycle)
            case _:
                print(f'Unknown instruction: {line}')

    return sum(signal_strength[val] for val in (20, 60, 100, 140, 180, 220))


@timeit
def part2(s: str):
    lines = s.splitlines()

    register = {'X': 1}
    cycle = 0
    signal = {}

    def update_signal(cycle):
        val = register['X']

        col = cycle % 40

        draw = (val - 1 <= col <= val + 1)
        signal[cycle] = draw

    for line in lines:
        match line.split():
            case ('addx', val):
                val = int(val)
                cycle += 1
                update_signal(cycle)
                cycle += 1
                register['X'] += val
                update_signal(cycle)
            case ('noop', ):
                cycle += 1
                update_signal(cycle)
            case _:
                print(f'Unknown instruction: {line}')

    answer = '\n\n'
    for i in range(6):
        row = list(signal.values())[i * 40:(i + 1) * 40]
        answer += ''.join([' #'[draw] for draw in row])
        answer += '\n'

    return answer


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--parts', nargs='+', type=int,
        choices=(1, 2), default=(1, 2))
    parser.add_argument('data', nargs='?', default=DATA)
    args = parser.parse_args()

    data = Path(args.data).read_text()

    for i in args.parts:
        func = (..., part1, part2)[i]
        func(data)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
