# hyprlauncher

Fedora packaging for official tag `v0.1.6`, commit
`c682906a0836447c27c8d974f35493d3baa79d64`. The GitHub tag archive SHA-256 is
`f02f93584e1017d7a466d0cafed910f630be39eba6b433922e645c834c4abf59`.

The patch removes upstream's appended `-O3` so RPM optimization and hardening
flags remain authoritative. The generated Hyprwire client and server sources
use the packaged scanner; no bundled or network dependency path exists.
`hyprlauncher --version` is run in `%check`. Interactive finder and rendering
tests are excluded because upstream provides no suite and they require a
Wayland compositor.

Build after: `aquamarine`, `hyprgraphics`, `hyprlang`, `hyprtoolkit`,
`hyprutils`, `hyprwayland-scanner`, `hyprwire`.
