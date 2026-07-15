# hypridle

Fedora 44 packaging for official upstream tag `v0.1.7`, commit
`5430b73ddf148651bcf35fa39ed4d757c7534028`.

The package uses system HyprWM protocol and utility packages. The downstream
patch removes upstream's unconditional release `-O3`, allowing Fedora's flags
to control optimization and hardening. `%check` exercises `--version`
headlessly.

Build ordering: `hyprland-protocols`, `hyprlang`, `hyprutils`, and
`hyprwayland-scanner`.
