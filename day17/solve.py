import argparse
from itertools import cycle
from pathlib import Path

from helpers import timeit

DATA = Path(__file__).with_name('data.txt')

ROCKS = (
    ((0, 2), (0, 3), (0, 4), (0, 5)),
    ((0, 3), (1, 2), (1, 3), (1, 4), (2, 3)),
    ((0, 2), (0, 3), (0, 4), (1, 4), (2, 4)),
    ((0, 2), (1, 2), (2, 2), (3, 2)),
    ((0, 2), (0, 3), (1, 2), (1, 3)),
)


def ecycle(lst, i=0):
    c = cycle(lst)
    length = len(lst)

    for item in c:
        i = (i + 1) % length
        yield (i, item)


def solve(s: str, *, n_rocks):
    jets = ecycle(s.splitlines()[0])
    rocks = ecycle(ROCKS)
    cache = {}

    tower = {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)}

    def empty(pr, pc, dr, dc):
        new_r, new_c = pr + dr, pc + dc
        return new_c in range(7) and (new_r, new_c) not in tower

    for n in range(n_rocks + 1):
        height = max(r for r, c in tower)

        irock, rock = next(rocks)

        pr, pc = height + 4, 0

        for ijet, jet in jets:
            jet = -1 if jet == '<' else 1

            if all(empty(pr, pc, r, c + jet) for r, c in rock):
                pc += jet

            if all(empty(pr, pc, r - 1, c) for r, c in rock):
                pr -= 1
            else:
                break

        tower |= {(pr + r, pc + c) for (r, c) in rock}

        if cached := cache.get((irock, ijet)):
            n_c, height_c = cached
            div, mod = divmod(n_rocks - n, n_c - n)
            if not mod:
                height += (height_c - height) * div
                break
        else:
            cache[irock, ijet] = n, height

    return height


@timeit
def part1(s: str):
    return solve(s, n_rocks=2022)


@timeit
def part2(s: str):
    return solve(s, n_rocks=1_000_000_000_000)


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
