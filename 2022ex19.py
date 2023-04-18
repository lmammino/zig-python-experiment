from multiprocessing import Pool
import time
import os
import platform
from cffi import FFI


cffi = FFI()
cffi.cdef(
    """
      unsigned long zig_run(unsigned long bp_ore_ore, unsigned long bp_clay_ore, unsigned long bp_obs_ore, unsigned long bp_obs_clay, unsigned long bp_geo_ore, unsigned long bp_geo_obs, unsigned long time_limit);
    """
)


if platform.uname()[0] == "Windows":
    lib_path = "zig-out/lib/libex19.dll"
elif platform.uname()[0] == "Linux":
    lib_path = "zig-out/lib/libex19.so"
else:
    lib_path = "zig-out/lib/libex19.dylib"


ex19 = cffi.dlopen(os.path.abspath(lib_path))


_input = """Blueprint 1: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 15 clay. Each geode robot costs 3 ore and 9 obsidian.
Blueprint 2: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 12 clay. Each geode robot costs 4 ore and 19 obsidian.
Blueprint 3: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 14 clay. Each geode robot costs 3 ore and 16 obsidian.
Blueprint 4: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 17 clay. Each geode robot costs 3 ore and 19 obsidian.
Blueprint 5: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 10 clay. Each geode robot costs 2 ore and 10 obsidian.
Blueprint 6: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 16 clay. Each geode robot costs 3 ore and 9 obsidian.
Blueprint 7: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 7 clay. Each geode robot costs 3 ore and 9 obsidian.
Blueprint 8: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 19 clay. Each geode robot costs 2 ore and 12 obsidian.
Blueprint 9: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 16 clay. Each geode robot costs 3 ore and 20 obsidian.
Blueprint 10: Each ore robot costs 2 ore. Each clay robot costs 2 ore. Each obsidian robot costs 2 ore and 7 clay. Each geode robot costs 2 ore and 14 obsidian.
Blueprint 11: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 16 clay. Each geode robot costs 4 ore and 12 obsidian.
Blueprint 12: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 15 clay. Each geode robot costs 2 ore and 15 obsidian.
Blueprint 13: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 5 clay. Each geode robot costs 2 ore and 10 obsidian.
Blueprint 14: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 15 clay. Each geode robot costs 3 ore and 16 obsidian.
Blueprint 15: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 19 clay. Each geode robot costs 2 ore and 9 obsidian.
Blueprint 16: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 4 ore and 15 clay. Each geode robot costs 4 ore and 9 obsidian.
Blueprint 17: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 17 clay. Each geode robot costs 3 ore and 16 obsidian.
Blueprint 18: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 13 clay. Each geode robot costs 3 ore and 12 obsidian.
Blueprint 19: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 10 clay. Each geode robot costs 4 ore and 10 obsidian.
Blueprint 20: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 17 clay. Each geode robot costs 3 ore and 10 obsidian.
Blueprint 21: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 22: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 20 clay. Each geode robot costs 3 ore and 14 obsidian.
Blueprint 23: Each ore robot costs 2 ore. Each clay robot costs 2 ore. Each obsidian robot costs 2 ore and 17 clay. Each geode robot costs 2 ore and 10 obsidian.
Blueprint 24: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 19 clay. Each geode robot costs 3 ore and 19 obsidian.
Blueprint 25: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 14 clay. Each geode robot costs 3 ore and 14 obsidian.
Blueprint 26: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 13 clay. Each geode robot costs 3 ore and 19 obsidian.
Blueprint 27: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 7 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 28: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 20 clay. Each geode robot costs 2 ore and 19 obsidian.
Blueprint 29: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 16 clay. Each geode robot costs 2 ore and 15 obsidian.
Blueprint 30: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 19 clay. Each geode robot costs 2 ore and 18 obsidian."""

from collections import deque
import re


def parser(s):
    ret = []
    for line in s.splitlines():
        parsed_line = re.findall(
            r"Blueprint \d+: Each (\w+) robot costs (\d+) (\w+). Each (\w+) robot costs (\d+) (\w+). Each (\w+) robot costs (\d+) (\w+) and (\d+) (\w+). Each (\w+) robot costs (\d+) (\w+) and (\d+) (\w+).",
            line,
            re.I | re.S,
        )[0]
        ret.append(
            {
                "ore": {"ore": int(parsed_line[1])},
                "clay": {"ore": int(parsed_line[4])},
                "obsidian": {"ore": int(parsed_line[7]), "clay": int(parsed_line[9])},
                "geode": {
                    "ore": int(parsed_line[12]),
                    "obsidian": int(parsed_line[14]),
                },
            }
        )
    return ret


def run_blueprint(bp, time_limit=24):
    max_ore = max([x["ore"] for x in bp.values()])
    max_clay = max([x.get("clay", 0) for x in bp.values()])
    max_obsidian = max([x.get("obsidian", 0) for x in bp.values()])
    bp_ore_ore = bp["ore"]["ore"]
    bp_clay_ore = bp["clay"]["ore"]
    bp_o_o = bp["obsidian"]["ore"]
    bp_o_c = bp["obsidian"]["clay"]
    bp_gore = bp["geode"]["ore"]
    bp_go = bp["geode"]["obsidian"]

    # robots, resources, timer
    stack = deque([(1, 0, 0, 0, 0, 0, 0, 0, 0)])
    seen = set()
    ret_max = 0
    gen = 0
    geodes_at_gen = 0

    while stack:
        # print(len(stack), end=" ")
        state = (
            robots_ore,
            robots_clay,
            robots_obsidian,
            robots_geode,
            resources_ore,
            resources_clay,
            resources_obsidian,
            resources_geode,
            timer,
        ) = stack.popleft()

        if state in seen:
            continue
        seen.add(state)

        if timer == time_limit:
            if resources_geode > ret_max:
                ret_max = resources_geode
                # print(f"geode {resources_geode}")
        else:
            gen = max(gen, timer)
            geodes_at_gen = max(robots_geode, geodes_at_gen)

            if timer == gen and robots_geode < geodes_at_gen:
                continue

            # no robot build, just storage
            stack.append(
                (
                    robots_ore,
                    robots_clay,
                    robots_obsidian,
                    robots_geode,
                    robots_ore + resources_ore,
                    robots_clay + resources_clay,
                    robots_obsidian + resources_obsidian,
                    robots_geode + resources_geode,
                    timer + 1,
                )
            )
            # robot build
            if bp_ore_ore <= resources_ore and robots_ore < max_ore:
                stack.append(
                    (
                        robots_ore + 1,
                        robots_clay,
                        robots_obsidian,
                        robots_geode,
                        robots_ore + resources_ore - bp_ore_ore,
                        robots_clay + resources_clay,
                        robots_obsidian + resources_obsidian,
                        robots_geode + resources_geode,
                        timer + 1,
                    )
                )
            if bp_clay_ore <= resources_ore and robots_clay < max_clay:
                stack.append(
                    (
                        robots_ore,
                        robots_clay + 1,
                        robots_obsidian,
                        robots_geode,
                        robots_ore + resources_ore - bp_clay_ore,
                        robots_clay + resources_clay,
                        robots_obsidian + resources_obsidian,
                        robots_geode + resources_geode,
                        timer + 1,
                    )
                )
            if (
                bp_o_o <= resources_ore
                and bp_o_c <= resources_clay
                and robots_obsidian < max_obsidian
            ):
                stack.append(
                    (
                        robots_ore,
                        robots_clay,
                        robots_obsidian + 1,
                        robots_geode,
                        robots_ore + resources_ore - bp_o_o,
                        robots_clay + resources_clay - bp_o_c,
                        robots_obsidian + resources_obsidian,
                        robots_geode + resources_geode,
                        timer + 1,
                    )
                )
            if bp_gore <= resources_ore and bp_go <= resources_obsidian:
                stack.append(
                    (
                        robots_ore,
                        robots_clay,
                        robots_obsidian,
                        robots_geode + 1,
                        robots_ore + resources_ore - bp_gore,
                        robots_clay + resources_clay,
                        robots_obsidian + resources_obsidian - bp_go,
                        robots_geode + resources_geode,
                        timer + 1,
                    )
                )
    return ret_max


def parallel_function_pure(i_blueprint):
    i, blueprint = i_blueprint
    n = run_blueprint(blueprint, 24)
    print(i, n)
    return (i + 1) * n


def parallel_function_zig(i_blueprint):
    i, blueprint = i_blueprint
    bp_ore_ore = blueprint["ore"]["ore"]
    bp_clay_ore = blueprint["clay"]["ore"]
    bp_obs_ore = blueprint["obsidian"]["ore"]
    bp_obs_clay = blueprint["obsidian"]["clay"]
    bp_geo_ore = blueprint["geode"]["ore"]
    bp_geo_obs = blueprint["geode"]["obsidian"]
    n = ex19.zig_run(bp_ore_ore, bp_clay_ore, bp_obs_ore, bp_obs_clay,bp_geo_ore,bp_geo_obs , 24)
    print(i, n)
    return (i + 1) * n


def execute(solver):
    t0 = time.monotonic()
    ret = 0

    with Pool(8) as p:
        ret = sum(p.map(solver, enumerate(parser(_input))))

    print(solver.__name__, time.monotonic() - t0, ret)


if __name__ == "__main__":
    execute(parallel_function_zig)
    execute(parallel_function_pure)
