# hyprland-guiutils

Fedora packaging for official tag `v0.2.1`, commit
`c2e906261142f5dd1ee0bfc44abba23e2754c660`. The GitHub tag archive SHA-256 is
`8de6ab7295dd120bab6b6b3e884b27b3c6ccc38ae345f3144bf9b5ad79251bcb`.

The patch lets release archives use the official tag metadata supplied by RPM
instead of invoking Git and embedding empty values. `%check` confirms all five
utilities were built. Upstream has no automated tests; executing the dialog,
donation, run, update, and welcome interfaces is excluded because each creates
a Hyprtoolkit Wayland window.

Build after: `aquamarine`, `hyprgraphics`, `hyprlang`, `hyprtoolkit`,
`hyprutils`.
