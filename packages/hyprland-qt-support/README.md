# hyprland-qt-support

Fedora packaging for official tag `v0.1.0`, commit
`9d4437011b4f02e60e98a3e36c7fa14bb053b502`. The GitHub tag archive SHA-256 is
`cac1f980bd088b890097f3f999cfdf03e73ee94c53f3c92d0b3bc23baa9e7b2c`.

The package installs both `org.hyprland.style` QML modules, their plugins,
QML files, type information, and backing runtime DSOs in Fedora's Qt 6 paths.
Upstream exports no headers or CMake/pkg-config development interface, so no
devel split is appropriate. The visual style tester is enabled and compiled;
running it is excluded because Mock has no graphical Wayland session.
`%check` verifies the tester and installed module descriptors.

Build after: `hyprlang`.
