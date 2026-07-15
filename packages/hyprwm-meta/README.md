# HyprWM meta packages

This source package contains no upstream code. It defines the supported
installation sets described by the repository design:

- `hyprland-desktop` hard-requires the complete supported desktop baseline.
- `hyprwm-complete` adds every stable optional HyprWM application.
- `hyprwm-meta` is a convenience alias for `hyprwm-complete`.

Hyprpm and exact-ABI plugin packages remain explicit opt-ins because they add
a compiler toolchain or a tighter support surface.
