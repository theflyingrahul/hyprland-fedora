# hyprlock

Fedora 44 packaging for official upstream tag `v0.9.5`, commit
`d75e93f8ee1721d70549d96f4d14bf2948aab70c`.

The upstream PAM service is installed as `%config(noreplace)` and delegates
authentication to Fedora's `login` PAM stack. The example configuration is
installed under `/usr/share/hypr`. The downstream patch removes upstream's
unconditional `-O3`; the spec supplies the immutable tagged commit to CMake.
`%check` runs the version path without a compositor or PAM conversation.

Build ordering: `hyprgraphics`, `hyprlang`, `hyprutils`, and
`hyprwayland-scanner`.
