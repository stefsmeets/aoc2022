from pathlib import Path


def calc_calories(s):
    return (sum(int(val) for val in group.splitlines()) for group in s.split('\n\n'))


def part1(s: str):
    calories = calc_calories(s)
    return max(calories)


def part2(s: str):
    calories = calc_calories(s)
    return sum(sorted(calories)[-3:])


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt')

    print(part1(DATA))
    print(part2(DATA))
