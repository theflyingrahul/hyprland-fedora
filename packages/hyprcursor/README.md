# hyprcursor

Rebase of the official Fedora source package to upstream tag `v0.1.13`.

The upstream Fedora lookaside test theme is retained solely for `%check`.
The patch removes hard-coded optimization and adds Cairo to the pkg-config
public dependency list because installed headers include `cairo/cairo.h`.
