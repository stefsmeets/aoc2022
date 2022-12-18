from pathlib import Path


def part1(s: str):
    lines = s.splitlines()

    total_score = 0

    points = {'X': 1, 'Y': 2, 'Z': 3}

    for line in lines:
        left, right = line.split()
        match left, right:
            # losses
            case ('A', 'Z') | ('B', 'X') | ('C', 'Y'):
                round_score = 0
            # draws
            case ('A', 'X') | ('B', 'Y') | ('C', 'Z'):
                round_score = 3
            # wins
            case ('A', 'Y') | ('B', 'Z') | ('C', 'X'):
                round_score = 6

        total_score += (round_score + points[right])

    return total_score


def part2(s: str):
    lines = s.splitlines()

    total_score = 0

    points = {'X': 0, 'Y': 3, 'Z': 6}

    for line in lines:
        left, right = line.split()
        match left, right:
            case ('A', 'Y') | ('B', 'X') | ('C', 'Z'):
                round_score = 1
            case ('A', 'Z') | ('B', 'Y') | ('C', 'X'):
                round_score = 2
            case ('A', 'X') | ('B', 'Z') | ('C', 'Y'):
                round_score = 3

        total_score += (round_score + points[right])

    return total_score


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt')

    print(part1(DATA))
    print(part2(DATA))
