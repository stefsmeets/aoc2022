from functools import reduce
from pathlib import Path

encode = {v - 2: k for v, k in enumerate('=-012')}
decode = {v: k for k, v in encode.items()}


def snafu2int(s):
    return reduce(lambda x, y: x * 5 + decode[y], (0, *s))


def int2snafu(d):
    q, r = divmod(d + 2, 5)
    return (int2snafu(q) if q else '') + encode[r - 2]


def part1(s: str):
    tot = sum(snafu2int(line) for line in s.splitlines())
    return int2snafu(tot)


def part2(s: str):
    return '🎄'


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
