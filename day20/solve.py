from pathlib import Path


class Node:
    def __init__(self, value):
        self.value = value


def solve(s: str, times=1, multiplier=1):
    numbers = [Node(int(line) * multiplier) for line in s.splitlines()]

    result = numbers.copy()
    n = len(numbers)

    for _ in range(times):
        for number in numbers:
            result.pop(idx_old := result.index(number))
            result.insert((idx_old + number.value) % (n - 1), number)

    values = [number.value for number in result]

    zero = values.index(0)

    return sum([values[(zero + p) % (n)] for p in (1000, 2000, 3000)])


def part1(s: str):
    return solve(s)


def part2(s: str):
    return solve(s, times=10, multiplier=811589153)


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text().read_text()

    print(part1(DATA))
    print(part2(DATA))
