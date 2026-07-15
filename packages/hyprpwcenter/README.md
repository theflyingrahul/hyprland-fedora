# hyprpwcenter

Fedora packaging for official tag `v0.1.2`, commit
`2ce8f3d174f2ae1c50c7dcc182d809a5ab33cad2`. The GitHub tag archive SHA-256 is
`ab4cfd4710566b07e98973d6723c24802d95774aa9c02aca839ff03e3bf09659`.

The patch preserves RPM compiler flags. The upstream desktop file and
downstream AppStream metadata are validated offline. Translations are embedded
in the executable by upstream's Hyprutils i18n engine, so there are no locale
files to split. There is no upstream test suite; launching is excluded from
Mock because it requires PipeWire and a Wayland compositor.

Build after: `aquamarine`, `hyprgraphics`, `hyprtoolkit`, `hyprutils`.
