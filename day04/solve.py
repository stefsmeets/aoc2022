from pathlib import Path


def get_sections(line):
    sections = []

    for elf in line.split(','):
        a, b = (int(val) for val in elf.split('-'))
        sections.append(set(range(a, b + 1)))

    return sections


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


def part2(s: str):
    lines = s.splitlines()

    result = 0

    for line in lines:
        sections_a, sections_b = get_sections(line)

        result += len(sections_a & sections_b) > 0

    return result


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
