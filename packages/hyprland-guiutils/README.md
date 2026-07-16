# hyprland-guiutils

Fedora packaging for official tag `v0.2.1`, commit
`c2e906261142f5dd1ee0bfc44abba23e2754c660`. The GitHub tag archive SHA-256 is
`8de6ab7295dd120bab6b6b3e884b27b3c6ccc38ae345f3144bf9b5ad79251bcb`.

The release-metadata patch lets release archives use the official tag metadata
supplied by RPM instead of invoking Git and embedding empty values. The welcome
patch also searches Fedora's libexec directory, where the portal backend and
polkit agent are intentionally installed, instead of incorrectly reporting
those packages as missing.

`%check` confirms all five utilities were built and that the welcome binary
contains the configured libexec path. Upstream has no automated tests;
executing the dialog, donation, run, update, and welcome interfaces is excluded
because each creates a Hyprtoolkit Wayland window.

Build after: `aquamarine`, `hyprgraphics`, `hyprlang`, `hyprtoolkit`,
`hyprutils`.
