import argparse
from collections import defaultdict
from pathlib import Path

from helpers import timeit


DATA = Path(__file__).with_name('data.txt')


def get_dir_sizes(s):
    lines = s.splitlines()

    sizes = defaultdict(int)
    p = Path()

    for line in lines:
        match line.split():
            case ('$', 'cd', '..'):
                p = p.parent
            case ('$', 'cd', drc):
                p = p / drc
            case ('$', 'ls'):
                pass
            case ('dir', drc):
                pass
            case (size, _):
                size = int(size)

                sizes[p] += size

                for parent in p.parents:
                    sizes[parent] += size

    return sizes


@timeit
def part1(s: str):
    sizes = get_dir_sizes(s)
    return sum(size for size in sizes.values() if size < 100000)


@timeit
def part2(s: str):
    sizes = get_dir_sizes(s)

    total_space = 70_000_000
    min_space = 30_000_000
    root_space = sizes[Path('\\')]

    to_free = root_space - (total_space - min_space)

    for size in sorted(sizes.values()):
        if size > to_free:
            break

    return size


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
