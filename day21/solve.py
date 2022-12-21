from operator import add, mul, sub, truediv
from pathlib import Path


def parse(s: str):
    lines = s.splitlines()

    known = {}
    to_solve = {}

    ops = {'+': add, '-': sub, '*': mul, '/': truediv}

    for line in lines:
        match line.split():
            case (name, x, op, y):
                name = name[:-1]
                to_solve[name] = (ops[op], x, y)
            case (name, x):
                name = name[:-1]
                known[name] = int(x)

    return known, to_solve


def part1(s: str):
    known, to_solve = parse(s)

    def solve(monkey):
        try:
            return known[monkey]
        except KeyError:
            f, monkey_1, monkey_2 = to_solve[monkey]
            return f(solve(monkey_1), solve(monkey_2))

    return int(solve('root'))


def part2(s: str):
    known, to_solve = parse(s)

    def solve(monkey):
        try:
            return known[monkey]
        except KeyError:
            f, monkey_1, monkey_2 = to_solve[monkey]
            return f(solve(monkey_1), solve(monkey_2))

    _, monkey_1, monkey_2 = to_solve.pop('root')

    right = solve(monkey_2)

    known['humn'] = 1j
    left = solve(monkey_1)

    return int((right - left.real) / left.imag)


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
