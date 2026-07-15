# hyprpicker

Fedora 44 packaging for official upstream tag `v0.4.7`, commit
`8c163ce9b8a40f85babe4dd6e23a238787351164`.

The package uses only system Wayland and HyprWM dependencies. Clipboard and
desktop-notification helpers remain weak dependencies because their features
are explicitly optional. The downstream patch removes build-time Git probing,
and `%check` exercises `--version` headlessly.

Build ordering: `hyprutils` and `hyprwayland-scanner`.
