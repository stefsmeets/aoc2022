from pathlib import Path


decode = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}

encode = {v: k for k, v in decode.items()}


def snafu2int(s):
    tot = 0

    for d in s:
        tot = tot * 5 + decode[d]

    return tot


def int2snafu(d):
    if d == 0:
        return ''

    r = (d + 2) % 5 - 2
    q = (d + 2) // 5

    return int2snafu(q) + encode[r]


def part1(s: str):
    tot = sum(snafu2int(line) for line in s.splitlines())
    return int2snafu(tot)


def part2(s: str):
    return '🎄'


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
