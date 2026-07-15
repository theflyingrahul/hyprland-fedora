# hyprtoolkit

Fedora packaging for official upstream tag `v0.5.4`, pinned to tag commit
`795d06e76434a951855762104f2b0c8c3842e052`.

The downstream patch leaves optimization and instrumentation to Fedora,
honors the packager's `BUILD_TESTING` selection, and records the public
pkg-config dependencies exposed by installed headers. The CMake build uses
only separately packaged dependencies; Nix flake inputs are not used.

All upstream GoogleTest tests run headlessly in `%check`. The `simpleWindow`,
`dialog`, `controls`, and `simpleSessionLock` example programs are compiled
but not executed: upstream does not register them with CTest, and they require
a running Wayland compositor and interactive validation.
