# hyprutils

Rebase of the official Fedora source package to upstream tag `v0.13.1`.

The package keeps Fedora's runtime/development split and updates the runtime
file list for SOVERSION 12.

The downstream CMake patch:

- removes hard-coded `-O3`;
- respects the packager's `BUILD_TESTING` setting; and
- prevents coverage instrumentation from leaking into the installed shared
  library.
