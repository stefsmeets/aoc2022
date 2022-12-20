from pathlib import Path


def solve(s, *, markersize):
    line = s.splitlines()[0]

    for start in range(len(line)):
        stop = start + markersize
        marker = set(line[start: stop])
        if len(marker) == markersize:
            break

    return stop


def part1(s: str):
    return solve(s, markersize=4)


def part2(s: str):
    return solve(s, markersize=14)


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
