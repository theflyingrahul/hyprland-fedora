# hyprwayland-scanner

Rebase of the official Fedora source package to upstream tag `v0.4.6`.

The binary package remains `hyprwayland-scanner-devel` for compatibility with
Fedora 44. The executable is a build-time code generator, not a Hyprland
runtime dependency.

The only downstream patch removes upstream's hard-coded `-O3` so Fedora's
standard optimization and hardening flags remain authoritative.
