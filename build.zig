const std = @import("std");

pub fn build(b: *std.build.Builder) void {
    // Standard release options allow the person running `zig build` to select
    // between Debug, ReleaseSafe, ReleaseFast, and ReleaseSmall.
    const mode = b.standardReleaseOptions();

    const lib = b.addSharedLibrary("ex19", "src/ex19.zig", b.version(0, 0, 1));
    lib.addPackagePath("zig-deque", "lib/zig-deque/src/deque.zig");
    lib.setBuildMode(mode);
    lib.install();
}
