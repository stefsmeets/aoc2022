import argparse
from dataclasses import dataclass
from itertools import takewhile
from math import prod
from pathlib import Path

from helpers import timeit


DATA = Path(__file__).with_name('data.txt')


@dataclass
class Monkey:
    num: int
    items: list[int]
    func: callable
    test_div: int
    true: int
    false: int
    inspections: int = 0

    @classmethod
    def from_input(cls, lines: list[str]):
        *_, left, op, right = lines[2].rsplit(maxsplit=3)

        agg = {'*': prod, '+': sum}[op]

        match (left, right):
            case ('old', 'old'):
                func = lambda x: agg((x, x))
            case ('old', val):
                func = lambda x: agg((x, int(val)))

        return cls(
            num=int(lines[0].strip(':').rsplit()[-1]),
            items=[int(val) for val in lines[1].rsplit(':')[-1].split(',')],
            func=func,
            test_div=int(lines[3].split()[-1]),
            true=int(lines[4].rsplit()[-1]),
            false=int(lines[5].rsplit()[-1]),
        )


def solve(s: str, div: int, rounds: int):
    lines = iter(s.splitlines())

    monkeys = []

    while monkey_input := list(takewhile(lambda line: line, lines)):
        monkeys.append(Monkey.from_input(monkey_input))

    mod = prod(monkey.test_div for monkey in monkeys)

    for rnd in range(rounds):

        for monkey in monkeys:
            monkey.inspections += len(monkey.items)

            for old in monkey.items:
                new = monkey.func(old) // div

                # Avoid numbers getting too large
                new %= mod

                test = new % monkey.test_div == 0

                throw_to = monkey.true if test else monkey.false

                monkeys[throw_to].items.append(new)

            monkey.items.clear()

    inspections = sorted((
        monkey.inspections for monkey in monkeys),
        reverse=True,
    )

    return prod(inspections[0: 2])


@timeit
def part1(s: str):
    # > part1 took: 0.012 s, result: 55216
    return solve(s, div=3, rounds=20)


@timeit
def part2(s: str):
    # > part2 took: 5.467 s, result: 12848882750
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
