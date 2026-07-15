# Hyprland

Fedora packaging for the official upstream release archive `v0.55.4`.

The package is built only against separately packaged dependencies. The
downstream patch removes hard-coded optimization and makes the system
`udis86`, Glaze, and hyprland-protocols dependencies mandatory, eliminating
all bundled or FetchContent fallbacks. UWSM integration is disabled because
Fedora 44 does not package UWSM.

Binary payloads are split into the compositor runtime, plugin development
headers, architecture-independent backgrounds, and the optional `hyprpm`
local plugin build manager. The development package explicitly requires
glslang because installed renderer headers include its C interface. Upstream's
compositor-driven test harness cannot
run in a headless Mock buildroot; `%check` instead exercises the built
version-reporting path and verifies the pinned release commit.
