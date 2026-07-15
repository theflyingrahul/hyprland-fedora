# hyprsunset

Fedora 44 packaging for official upstream tag `v0.4.0`, commit
`25f704346ec22e7623b0873ef8c4573b57ca1512`.

The package builds from system protocol, scanner, language, and utility
packages. The downstream patch replaces source-tree Git probing with values
from the spec and corrects the protocol minimum to the first release containing
the `blocked` event used by 0.4.0. `%check` runs the version path headlessly and
confirms the release commit is embedded.

Build ordering: `hyprland-protocols`, `hyprlang`, `hyprutils`, and
`hyprwayland-scanner`.
