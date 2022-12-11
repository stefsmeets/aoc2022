import argparse
from collections import deque
from itertools import takewhile
from math import prod
from pathlib import Path

from helpers import timeit


DATA = Path(__file__).with_name('data.txt')


def parse_monkey(lines):
    return {
        'num': int(lines[0].strip(':').rsplit()[-1]),
        'items': deque([
            int(val) for val in lines[1].rsplit(':')[-1].split(',')]),
        'op': lines[2].rsplit('= ')[-1],
        'test_div': int(lines[3].split()[-1]),
        'true': int(lines[4].rsplit()[-1]),
        'false': int(lines[5].rsplit()[-1]),
        'inspections': 0,
    }


def solve(s: str, div: int, rounds: int):
    lines = iter(s.splitlines())

    monkeys = []

    while monkey := list(takewhile(lambda line: line, lines)):
        monkeys.append(parse_monkey(monkey))

    mod = prod(monkey['test_div'] for monkey in monkeys)

    for rnd in range(rounds):

        for monkey in monkeys:
            monkey['inspections'] += len(monkey['items'])

            while monkey['items']:
                old = monkey['items'].popleft()

                new = eval(monkey['op']) // div

                # Avoid numbers getting too large
                new %= mod

                test = new % monkey['test_div'] == 0

                throw_to = monkey['true'] if test else monkey['false']

                monkeys[throw_to]['items'].append(new)

    inspections = sorted((
        monkey['inspections'] for monkey in monkeys),
        reverse=True,
    )

    return prod(inspections[0: 2])


@timeit
def part1(s: str):
    return solve(s, div=3, rounds=20)


@timeit
def part2(s: str):
    return solve(s, div=1, rounds=10_000)


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
