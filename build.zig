const std = @import("std");
const builtin = @import("builtin");

pub fn build(b: *std.build.Builder) void {
    const include_path_env = b.env_map.get("ADDINCLUDEPATH");
    if (include_path_env == null) {
        std.log.err("ADDINCLUDEPATH is not set\n", .{});
        return;
    }
    var paths = std.mem.tokenize(u8, include_path_env.?, " ");

    // Standard release options allow the person running `zig build` to select
    // between Debug, ReleaseSafe, ReleaseFast, and ReleaseSmall.
    const mode = std.builtin.Mode.ReleaseFast;

    const lib = switch (builtin.os.tag) {
        // .windows => {
        // },
        .macos => b.addObject("ex19", "src/ex19.zig"),
        .linux => b.addSharedLibrary("ex19", "src/ex19.zig", b.version(0, 0, 1)),
        else => {
            std.debug.print("Running on an unsupported operating system.\n");
            return;
        },
    };

    lib.addPackagePath("zig-deque", "lib/zig-deque/src/deque.zig");
    lib.setBuildMode(mode);
    lib.setOutputDir("zig-out/");

    switch (builtin.os.tag) {
        .macos => {
            lib.disable_stack_probing = true;
        },
        .linux => {
            lib.linkLibC();
        },
        else => {
            std.debug.print("Running on an unsupported operating system.\n");
            return;
        },
    }
    while (paths.next()) |path| {
        lib.addIncludePath(path);
    }
    b.default_step.dependOn(&lib.step);
}
