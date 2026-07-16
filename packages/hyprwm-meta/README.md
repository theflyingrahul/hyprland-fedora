# HyprWM meta packages

This source package contains no upstream code. It defines the supported
installation sets described by the repository design:

- `hyprland-desktop` hard-requires the complete supported desktop baseline.
- `hyprwm-complete` adds every stable optional HyprWM application, the exact
  official plugin set, and concrete Fedora packages for the terminal, file
  manager, notification daemon, status bar, PipeWire session, clipboard, and
  fallback portal interfaces expected by the first-run welcome screen. It also
  selects Qt 5 and Qt 6 Wayland backends, Noto and Font Awesome fonts, the
  Grim/Slurp screenshot workflow, Cliphist clipboard history, and LXAppearance
  for GTK themes.
- `hyprwm-meta` is a convenience alias for `hyprwm-complete`.

Hyprpm remains an explicit opt-in because it installs a local compiler
toolchain; the reproducible exact-ABI plugin RPMs are part of the complete set.
