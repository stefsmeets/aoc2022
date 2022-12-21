from pathlib import Path


def parse(s: str):
    lines = s.splitlines()

    known = {}
    to_solve = {}

    ops = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
    }

    for line in lines:
        name = line[0:4]

        match line.split():
            case (name, x, op, y):
                name = name[:-1]
                f = ops[op]
                to_solve[name] = (f, x, y)
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

    known['humn'] = magic_a = 0

    while solve(monkey_1) % 1 != 0:
        known['humn'] = magic_a = magic_a + 1

    magic_b = 1
    known['humn'] = magic_a + magic_b

    while solve(monkey_1) % 1 != 0:
        magic_b += 1
        known['humn'] = magic_a + magic_b

    known['humn'] = magic_a
    left1 = solve(monkey_1)

    known['humn'] = magic_a + magic_b
    left2 = solve(monkey_1)

    magic_multiplier = (left1 - right) / (left1 - left2)

    return int(magic_a + magic_b * magic_multiplier)


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
