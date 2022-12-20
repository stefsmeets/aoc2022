import re
from collections import deque
from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path

PAT = re.compile(
    r'Blueprint (\d+): Each ore robot costs (\d+) ore. '
    r'Each clay robot costs (\d+) ore. '
    r'Each obsidian robot costs (\d+) ore and (\d+) clay. '
    r'Each geode robot costs (\d+) ore and (\d+) obsidian.'
)


@dataclass
class Blueprint:
    num: int
    obot_ore_cost: tuple[int]
    cbot_ore_cost: tuple[int]
    obsbot_ore_cost: tuple[int]
    obsbot_clay_cost: tuple[int]
    gbot_ore_cost: tuple[int]
    gbot_obs_cost: tuple[int]

    def max_ore_cost(self):
        return max(self.obot_ore_cost, self.cbot_ore_cost, self.obsbot_ore_cost, self.gbot_ore_cost)

    @classmethod
    def from_line(cls, line):
        m = PAT.match(line)
        return cls(*(int(val) for val in m.groups()))

    def can_make_obot(self, r):
        return r.o >= self.obot_ore_cost and r.obots < self.max_ore_cost()

    def can_make_cbot(self, r):
        return r.o >= self.cbot_ore_cost and r.cbots < self.obsbot_clay_cost

    def can_make_obsbot(self, r):
        return r.o >= self.obsbot_ore_cost and r.c >= self.obsbot_clay_cost and r.obsbots < self.gbot_obs_cost

    def can_make_gbot(self, r):
        return r.o >= self.gbot_ore_cost and r.obs >= self.gbot_obs_cost


Resources = namedtuple('Resources', 'o c obs g obots cbots obsbots gbots time'.split())


def tick(r):
    return Resources(
        r.o + r.obots,
        r.c + r.cbots,
        r.obs + r.obsbots,
        r.g + r.gbots,
        r.obots,
        r.cbots,
        r.obsbots,
        r.gbots,
        r.time - 1,
    )


def make_obot(r, blueprint):
    return Resources(
        r.o - blueprint.obot_ore_cost + r.obots,
        r.c + r.cbots,
        r.obs + r.obsbots,
        r.g + r.gbots,
        r.obots + 1,
        r.cbots,
        r.obsbots,
        r.gbots,
        r.time - 1,
    )


def make_cbot(r, blueprint):
    return Resources(
        r.o - blueprint.cbot_ore_cost + r.obots,
        r.c + r.cbots,
        r.obs + r.obsbots,
        r.g + r.gbots,
        r.obots,
        r.cbots + 1,
        r.obsbots,
        r.gbots,
        r.time - 1,
    )


def make_obsbot(r, blueprint):
    return Resources(
        r.o - blueprint.obsbot_ore_cost + r.obots,
        r.c - blueprint.obsbot_clay_cost + r.cbots,
        r.obs + r.obsbots,
        r.g + r.gbots,
        r.obots,
        r.cbots,
        r.obsbots + 1,
        r.gbots,
        r.time - 1,
    )


def make_gbot(r, blueprint):
    return Resources(
        r.o - blueprint.gbot_ore_cost + r.obots,
        r.c + r.cbots,
        r.obs - blueprint.gbot_obs_cost + r.obsbots,
        r.g + r.gbots,
        r.obots,
        r.cbots,
        r.obsbots,
        r.gbots + 1,
        r.time - 1,
    )


def trim(r, bp):
    max_ore_cost = bp.max_ore_cost()
    o = min(r.o, max_ore_cost + (max_ore_cost - r.obots) * (r.time - 1))
    c = min(r.c, bp.obsbot_clay_cost + (bp.obsbot_clay_cost - r.cbots) * (r.time - 1))
    obs = min(r.obs, bp.gbot_obs_cost + (bp.gbot_obs_cost - r.obots) * (r.time - 1))

    return Resources(
        o, c, obs, r.g, r.obots, r.cbots, r.obsbots, r.gbots, r.time)


def solve_blueprint(blueprint, total_time=24):
    initial_state = Resources(0, 0, 0, 0, 1, 0, 0, 0, total_time)

    q = deque([initial_state])
    seen = set()
    times = set()
    max_geodes = 0

    while q:
        r = q.popleft()

        if r.time not in times:
            times.add(r.time)
            print(f'[{blueprint.num}] Time left: {r.time:<2} | Queue size: {len(q)}')

        max_geodes = max(max_geodes, r.g)

        if r.time == 0:
            continue

        state = trim(r, blueprint)

        if state in seen:
            continue

        seen.add(state)

        if blueprint.can_make_gbot(r):
            q.append(make_gbot(r, blueprint))
        else:
            if blueprint.can_make_obot(r):
                q.append(make_obot(r, blueprint))
            if blueprint.can_make_cbot(r):
                q.append(make_cbot(r, blueprint))
            if blueprint.can_make_obsbot(r):
                q.append(make_obsbot(r, blueprint))

            q.append(tick(r))

    return max_geodes


def part1(s: str):
    blueprints = (Blueprint.from_line(line) for line in s.splitlines())

    quality = 0

    for blueprint in blueprints:
        max_geodes = solve_blueprint(blueprint, total_time=24)
        quality += max_geodes * blueprint.num

    return quality


def part2(s: str):
    blueprints = list(Blueprint.from_line(line) for line in s.splitlines())

    product = 1

    for blueprint in blueprints[0:3]:
        max_geodes = solve_blueprint(blueprint, total_time=32)
        product *= max_geodes

    return product


if __name__ == '__main__':
    DATA = Path(__file__).with_name('data.txt').read_text()

    print(part1(DATA))
    print(part2(DATA))
