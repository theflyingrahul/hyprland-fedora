# hyprsysteminfo

Fedora packaging for official tag `v0.2.0`, commit
`6f68a726531b53d87c6dd6ce474face27dde02ff`. The GitHub tag archive SHA-256 is
`4f875e7e986deeda35c05090b59f11f3b5802cac8863dafcc6e8251ea37530b1`.

The patch requires packaged Glaze, removes FetchContent and appended `-O3`,
and completes the upstream desktop entry. The desktop and downstream AppStream
metadata are validated offline. There is no upstream suite; launching is
excluded because Hyprtoolkit requires a Wayland compositor and the Hyprland
IPC panel requires a live compositor.

Build after: `aquamarine`, `glaze`, `hyprgraphics`, `hyprtoolkit`, `hyprutils`.
