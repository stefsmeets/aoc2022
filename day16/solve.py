import re
from pathlib import Path

import networkx as nx


VALVE_PAT = re.compile('[A-Z]{2}')
INT_PAT = re.compile('[0-9]+')


def parse_line(line):
    src, *dst = re.findall(VALVE_PAT, line)
    flow = int(re.search(INT_PAT, line).group())
    return src, dst, flow


def get_paths_and_flows(s):
    lines = s.splitlines()

    G = nx.DiGraph()

    flows = {}

    for line in lines:
        src, dsts, flow = parse_line(line)
        for dst in dsts:
            G.add_edge(src, dst, flow=flow)

        flows[src] = flow

    paths = dict(nx.all_pairs_dijkstra_path_length(G, cutoff=30))

    new_paths = {}
    for k, v in paths.items():
        if flows[k] == 0 and k != 'AA':
            new_v = {}
        else:
            new_v = {target: length for target, length in v.items() if flows[target] > 0 and target != k}

        new_paths[k] = new_v

    return new_paths, flows


def solve(s, time, part2=False):
    paths, flows = get_paths_and_flows(s)

    max_pressure = 0

    def search(time, valve='AA', pressure=0, opened={'AA'}, elephant=False):
        nonlocal max_pressure
        max_pressure = max(max_pressure, pressure)

        if time <= 0:
            return

        if valve not in opened:
            flow = flows[valve] * time

            search(time - 1, valve, pressure + flow, opened | {valve}, elephant)

            if part2 and not elephant:
                search(25, 'AA', pressure + flow, opened | {valve}, True)

        else:
            unopened = (v for v in paths[valve] if v not in opened)

            for next_valve in unopened:
                search(time - paths[valve][next_valve], next_valve, pressure, opened, elephant)

    search(time)

    return max_pressure


def part1(s: str):
    return solve(s, time=29)


def part2(s: str):
    return solve(s, time=25, part2=True)


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
