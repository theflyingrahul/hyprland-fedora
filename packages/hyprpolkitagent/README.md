# hyprpolkitagent

Fedora packaging for official tag `v0.1.3`, commit
`7e4054410f6d6331b239fea1c659ad6a917fbf6a`. The GitHub tag archive SHA-256 is
`a8fa714b92d47331f056b608cb731dd1f5cc3845a9109cb22c6e6eb55b4eac84`.

The package installs the agent in `%{_libexecdir}`, its D-Bus activation file,
and its systemd user unit. It requires `hyprland-qt-support` because upstream
selects `org.hyprland.style` at runtime. There is no upstream test suite; the
Mock-safe check validates the installed executable and both activation files.
Starting the agent is excluded because it requires a graphical user bus,
PolicyKit authority, and Wayland session.

Build after: `hyprland-qt-support`, `hyprutils`.
