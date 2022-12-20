import string
from pathlib import Path


LETTERS = '_' + string.ascii_lowercase + string.ascii_uppercase


def split_in_two(lst):
    n = int(len(lst) / 2)

    a = lst[:n]
    b = lst[n:]
    assert len(a) == len(b), (a, b)

    return a, b


def group_by_three(lst) -> list[tuple[str]]:
    args = [iter(lst)] * 3
    return list(zip(*args, strict=True))


def part1(s: str):
    lines = s.splitlines()

    result = 0

    for line in lines:
        a, b = split_in_two(line)
        letter = (set(a) & set(b)).pop()
        result += LETTERS.index(letter)

    return result


def part2(s: str):
    lines = s.splitlines()

    result = 0

    for a, b, c in group_by_three(lines):
        letter = (set(a) & set(b) & set(c)).pop()
        result += LETTERS.index(letter)

    return result


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
