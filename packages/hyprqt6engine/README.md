# hyprqt6engine

Fedora packaging for official tag `v0.1.0`, commit
`e8a694d5fc7813cf477f426dce731967e4cf670b`. The GitHub tag archive SHA-256 is
`e52692168faa51a53e6f05c12114e79ead76787045668c65d41225a13a318f62`.

The patch declares the Qt Quick Controls and private Qt interfaces used by the
platform plugin, enables Fedora's KF6 color, configuration, and icon
integrations, and fixes GNU library-directory initialization. The common DSO
is private runtime code and upstream installs no headers or development
metadata, so no devel subpackage is created. Because private Qt headers are
used, the RPM requires the exact Qt base GUI runtime version from the build.
Upstream has no test suite;
`%check` verifies all installed plugin artifacts. Loading them is excluded
because it requires a graphical Qt session.

Build after: `hyprlang`, `hyprutils`.
