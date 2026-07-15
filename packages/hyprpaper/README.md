# hyprpaper

Fedora 44 packaging for official upstream tag `v0.8.4`, commit
`20fc0fa6c2056c388a4cd69cb394a9f989dd27c0`.

The package builds against system HyprWM libraries and generators only. The
downstream patch replaces source-tree Git probing with immutable release
metadata supplied by the spec. `%check` runs the version path without a
Wayland compositor and verifies that the release commit is embedded.

Build ordering: `hyprlang`, `hyprtoolkit`, `hyprutils`,
`hyprwayland-scanner`, and `hyprwire`.
