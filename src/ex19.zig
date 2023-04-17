const std = @import("std");
const deque = @import("zig-deque");

const State = struct {
    robots_ore: u32,
    robots_clay: u32,
    robots_obsidian: u32,
    robots_geode: u32,
    resources_ore: u32,
    resources_clay: u32,
    resources_obsidian: u32,
    resources_geode: u32,
    timer: u32,
};

const allocator = std.heap.page_allocator;

export fn zig_run(bp_ore_ore: u32, bp_clay_ore: u32, bp_obs_ore: u32, bp_obs_clay: u32, bp_geo_ore: u32, bp_geo_obs: u32, time_limit: u32) u32 {
    const max_ore = @max(bp_geo_ore, @max(bp_obs_ore, @max(bp_clay_ore, bp_ore_ore)));

    // var stack = std.ArrayList(State).init(allocator);
    // defer stack.deinit();

    var stack = deque.Deque(State).init(std.heap.page_allocator) catch unreachable;
    defer stack.deinit();

    const start_state = State{
        .timer = 0,
        .robots_clay = 0,
        .robots_geode = 0,
        .robots_obsidian = 0,
        .robots_ore = 1,
        .resources_clay = 0,
        .resources_geode = 0,
        .resources_obsidian = 0,
        .resources_ore = 0,
    };

    stack.pushBack(start_state) catch unreachable;
    var seen = std.AutoHashMap(State, bool).init(allocator);
    defer seen.deinit();
    var ret_max: u32 = 0;
    var gen: u32 = 0;
    var geodes_at_gen: u32 = 0;

    while (stack.len() > 0) {
        // std.debug.print("stack.items.len: {d}\n", .{stack.items.len});
        const state = stack.popFront().?;
        // std.debug.print("state: {d}\n", .{state.timer});

        if (seen.contains(state)) {
            // std.debug.print("existing: {any}\n", .{v});
            continue;
        }
        seen.put(state, true) catch unreachable;
        if (state.timer == time_limit) {
            if (state.resources_geode > ret_max) {
                ret_max = state.resources_geode;
            }
            continue;
        }

        gen = @max(gen, state.timer);
        geodes_at_gen = @max(geodes_at_gen, state.robots_geode);

        if ((state.timer == gen) and (state.robots_geode < geodes_at_gen)) {
            continue;
        }

        stack.pushBack(State{
            .robots_ore = state.robots_ore,
            .robots_clay = state.robots_clay,
            .robots_obsidian = state.robots_obsidian,
            .robots_geode = state.robots_geode,
            .resources_ore = state.robots_ore + state.resources_ore,
            .resources_clay = state.robots_clay + state.resources_clay,
            .resources_obsidian = state.robots_obsidian + state.resources_obsidian,
            .resources_geode = state.robots_geode + state.resources_geode,
            .timer = state.timer + 1,
        }) catch unreachable;

        // create an ore robot
        if ((bp_ore_ore <= state.resources_ore) and (state.robots_ore < max_ore)) {
            stack.pushBack(State{
                .robots_ore = state.robots_ore + 1,
                .robots_clay = state.robots_clay,
                .robots_obsidian = state.robots_obsidian,
                .robots_geode = state.robots_geode,
                .resources_ore = state.robots_ore + state.resources_ore - bp_ore_ore,
                .resources_clay = state.robots_clay + state.resources_clay,
                .resources_obsidian = state.robots_obsidian + state.resources_obsidian,
                .resources_geode = state.robots_geode + state.resources_geode,
                .timer = state.timer + 1,
            }) catch unreachable;
        }

        // clay robot
        if ((bp_clay_ore <= state.resources_ore) and (state.robots_clay < bp_obs_clay)) {
            stack.pushBack(State{
                .robots_ore = state.robots_ore,
                .robots_clay = state.robots_clay + 1,
                .robots_obsidian = state.robots_obsidian,
                .robots_geode = state.robots_geode,
                .resources_ore = state.robots_ore + state.resources_ore - bp_clay_ore,
                .resources_clay = state.robots_clay + state.resources_clay,
                .resources_obsidian = state.robots_obsidian + state.resources_obsidian,
                .resources_geode = state.robots_geode + state.resources_geode,
                .timer = state.timer + 1,
            }) catch unreachable;
        }

        //obsidian robot
        if ((bp_obs_ore <= state.resources_ore) and (bp_obs_clay <= state.resources_clay) and (state.robots_obsidian < bp_geo_obs)) {
            stack.pushBack(State{
                .robots_ore = state.robots_ore,
                .robots_clay = state.robots_clay,
                .robots_obsidian = state.robots_obsidian + 1,
                .robots_geode = state.robots_geode,
                .resources_ore = state.robots_ore + state.resources_ore - bp_obs_ore,
                .resources_clay = state.robots_clay + state.resources_clay - bp_obs_clay,
                .resources_obsidian = state.robots_obsidian + state.resources_obsidian,
                .resources_geode = state.robots_geode + state.resources_geode,
                .timer = state.timer + 1,
            }) catch unreachable;
        }

        //geode robot
        if ((bp_geo_ore <= state.resources_ore) and (bp_geo_obs <= state.resources_obsidian)) {
            stack.pushBack(State{
                .robots_ore = state.robots_ore,
                .robots_clay = state.robots_clay,
                .robots_obsidian = state.robots_obsidian,
                .robots_geode = state.robots_geode + 1,
                .resources_ore = state.robots_ore + state.resources_ore - bp_geo_ore,
                .resources_clay = state.robots_clay + state.resources_clay,
                .resources_obsidian = state.robots_obsidian + state.resources_obsidian - bp_geo_obs,
                .resources_geode = state.robots_geode + state.resources_geode,
                .timer = state.timer + 1,
            }) catch unreachable;
        }
    }

    return ret_max;
}
