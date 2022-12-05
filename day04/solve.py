import argparse
from pathlib import Path

from helpers import timeit


DATA = Path(__file__).with_name('data.txt').read_text()


def get_sections(line) -> tuple[set[int], set[int]]:
    elf_a, elf_b = line.split(',')

    a0, a1 = (int(val) for val in elf_a.split('-'))
    sections_a = set(range(a0, a1 + 1))

    b0, b1 = (int(val) for val in elf_b.split('-'))
    sections_b = set(range(b0, b1 + 1))

    return sections_a, sections_b


@timeit
def part1(s: str):
    lines = s.splitlines()

    result = 0

    for line in lines:
        sections_a, sections_b = get_sections(line)

        result += (
            sections_a.issubset(sections_b) or
            sections_b.issubset(sections_a)
        )

    return result


@timeit
def part2(s: str):
    lines = s.splitlines()

    result = 0

    for line in lines:
        sections_a, sections_b = get_sections(line)

        result += len(sections_a & sections_b) > 0

    return result


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
