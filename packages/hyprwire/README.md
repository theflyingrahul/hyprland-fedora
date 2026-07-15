# hyprwire

Fedora packaging for the official upstream tag `v0.3.1`.

The downstream patch removes hard-coded optimization, keeps the upstream test
suite enabled for release builds, removes a reference to a script absent from
the release archive, and fixes the installed pkg-config and CMake version
metadata. The scanner is split into `hyprwire-scanner-devel` because it is a
build-time code generator rather than a runtime component of the library.
