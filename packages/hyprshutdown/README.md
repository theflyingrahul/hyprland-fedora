# hyprshutdown

Fedora packaging for official tag `v0.1.1`, commit
`db1f38b03b173984ae9ed3abeb9750583c9bbd91`. The GitHub tag archive SHA-256 is
`32adb385b7bfe22398d45cd5325416bf0ac3ae4a5bd89678353dae96f92ba638`.

The patch makes system Glaze mandatory, removes FetchContent, and preserves
RPM compiler flags. CMake is also configured fully disconnected.
`hyprshutdown --help` runs headlessly in `%check`; shutdown behavior is
excluded because it requires a live Hyprland session and would terminate
processes.

Build after: `aquamarine`, `glaze`, `hyprgraphics`, `hyprtoolkit`, `hyprutils`.
