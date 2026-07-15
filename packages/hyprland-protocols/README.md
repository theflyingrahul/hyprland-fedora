# hyprland-protocols

Rebase of the official Fedora source package to upstream tag `v0.7.0`.

The tagged release is Meson-only. Upstream changed `main` to CMake after this
tag without publishing a new release, so this stable package intentionally
continues to use Fedora's Meson macros.

The binary package remains `hyprland-protocols-devel`; the XML is build-time
data and is not a runtime requirement of the compiled compositor.
