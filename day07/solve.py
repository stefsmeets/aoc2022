from collections import defaultdict
from pathlib import Path


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


def part1(s: str):
    sizes = get_dir_sizes(s)
    return sum(size for size in sizes.values() if size < 100000)


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


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
