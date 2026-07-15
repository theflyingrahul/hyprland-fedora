# xdg-desktop-portal-hyprland

Fedora 44 packaging for official upstream tag `v1.3.12`, commit
`01e13c0a027a2d177df4dead76ac9d069e2cc8e6`.

The package uses upstream's CMake installation for the libexec backend,
Qt share picker, portal descriptor, session D-Bus service, and systemd user
unit. The downstream patch removes forced optimization and makes system
`sdbus-cpp` and `hyprland-protocols` mandatory; release archives contain no
submodule payloads. `%check` runs the backend version path headlessly and
validates the installed activation metadata.

Build ordering: `hyprland-protocols`, `hyprlang`, `hyprutils`, and
`hyprwayland-scanner`.
