# Primary source index

Audit date: **2026-07-15**

This index records the authoritative sources used by the Phase 1
investigation. Links to mutable default branches are used only for explicitly
labeled unreleased observations. Stable build decisions use tags, immutable
commits, or distribution source-package versions.

## HyprWM organization

- [HyprWM organization repositories API](https://api.github.com/orgs/hyprwm/repos?per_page=100&type=all)
- [Hyprland](https://github.com/hyprwm/Hyprland)
- [HyprWM development standards](https://github.com/hyprwm/standards)
- [Upstream Nix release set](https://github.com/hyprwm/hyprnix)

## Stable core sources

| Project | Stable source | Key metadata |
|---|---|---|
| Hyprland 0.55.4 | [tag tree](https://github.com/hyprwm/Hyprland/tree/v0.55.4) | [CMakeLists.txt](https://github.com/hyprwm/Hyprland/blob/v0.55.4/CMakeLists.txt), [pkg-config template](https://github.com/hyprwm/Hyprland/blob/v0.55.4/hyprland.pc.in), [license](https://github.com/hyprwm/Hyprland/blob/v0.55.4/LICENSE) |
| hyprutils 0.13.1 | [tag tree](https://github.com/hyprwm/hyprutils/tree/v0.13.1) | [CMakeLists.txt](https://github.com/hyprwm/hyprutils/blob/v0.13.1/CMakeLists.txt), [pkg-config template](https://github.com/hyprwm/hyprutils/blob/v0.13.1/hyprutils.pc.in) |
| hyprlang 0.6.8 | [tag tree](https://github.com/hyprwm/hyprlang/tree/v0.6.8) | [CMakeLists.txt](https://github.com/hyprwm/hyprlang/blob/v0.6.8/CMakeLists.txt), [COPYRIGHT](https://github.com/hyprwm/hyprlang/blob/v0.6.8/COPYRIGHT), [pkg-config template](https://github.com/hyprwm/hyprlang/blob/v0.6.8/hyprlang.pc.in) |
| hyprgraphics 0.5.1 | [tag tree](https://github.com/hyprwm/hyprgraphics/tree/v0.5.1) | [CMakeLists.txt](https://github.com/hyprwm/hyprgraphics/blob/v0.5.1/CMakeLists.txt), [pkg-config template](https://github.com/hyprwm/hyprgraphics/blob/v0.5.1/hyprgraphics.pc.in) |
| hyprcursor 0.1.13 | [tag tree](https://github.com/hyprwm/hyprcursor/tree/v0.1.13) | [CMakeLists.txt](https://github.com/hyprwm/hyprcursor/blob/v0.1.13/CMakeLists.txt), [pkg-config template](https://github.com/hyprwm/hyprcursor/blob/v0.1.13/hyprcursor.pc.in) |
| aquamarine 0.12.1 | [tag tree](https://github.com/hyprwm/aquamarine/tree/v0.12.1) | [CMakeLists.txt](https://github.com/hyprwm/aquamarine/blob/v0.12.1/CMakeLists.txt), [pkg-config template](https://github.com/hyprwm/aquamarine/blob/v0.12.1/aquamarine.pc.in) |
| hyprwayland-scanner 0.4.6 | [tag tree](https://github.com/hyprwm/hyprwayland-scanner/tree/v0.4.6) | [CMakeLists.txt](https://github.com/hyprwm/hyprwayland-scanner/blob/v0.4.6/CMakeLists.txt), [CMake config template](https://github.com/hyprwm/hyprwayland-scanner/blob/v0.4.6/hyprwayland-scanner-config.cmake.in), [pkg-config template](https://github.com/hyprwm/hyprwayland-scanner/blob/v0.4.6/hyprwayland-scanner.pc.in) |
| hyprland-protocols 0.7.0 | [tag tree](https://github.com/hyprwm/hyprland-protocols/tree/v0.7.0) | [Meson build](https://github.com/hyprwm/hyprland-protocols/blob/v0.7.0/meson.build), [pkg-config template](https://github.com/hyprwm/hyprland-protocols/blob/v0.7.0/hyprland-protocols.pc.in) |

### Unreleased protocol build-system migration

- [`meson -> cmake` commit](https://github.com/hyprwm/hyprland-protocols/commit/3f3860b869014c00e8b9e0528c7b4ddc335c21ab)
- [Current CMake-only protocol source at audited commit](https://github.com/hyprwm/hyprland-protocols/blob/1cb6db5fd6bb8aee419f4457402fa18293ace917/CMakeLists.txt)

The migration occurred after 0.7.0 and has no tagged release. Fedora packaging
of 0.7.0 must use Meson.

## Extended libraries and applications

- [hyprwire 0.3.1](https://github.com/hyprwm/hyprwire/tree/v0.3.1)
- [hyprtoolkit 0.5.4](https://github.com/hyprwm/hyprtoolkit/tree/v0.5.4)
- [hyprpaper 0.8.4](https://github.com/hyprwm/hyprpaper/tree/v0.8.4)
- [hyprlock 0.9.5](https://github.com/hyprwm/hyprlock/tree/v0.9.5)
- [hypridle 0.1.7](https://github.com/hyprwm/hypridle/tree/v0.1.7)
- [hyprpicker 0.4.7](https://github.com/hyprwm/hyprpicker/tree/v0.4.7)
- [hyprsunset 0.4.0](https://github.com/hyprwm/hyprsunset/tree/v0.4.0)
- [xdg-desktop-portal-hyprland 1.3.12](https://github.com/hyprwm/xdg-desktop-portal-hyprland/tree/v1.3.12)
- [hyprland-plugins 0.55.0](https://github.com/hyprwm/hyprland-plugins/tree/v0.55.0)
- [hyprlauncher 0.1.6](https://github.com/hyprwm/hyprlauncher/tree/v0.1.6)
- [hyprpolkitagent 0.1.3](https://github.com/hyprwm/hyprpolkitagent/tree/v0.1.3)
- [hyprpwcenter 0.1.2](https://github.com/hyprwm/hyprpwcenter/tree/v0.1.2)
- [hyprshutdown 0.1.1](https://github.com/hyprwm/hyprshutdown/tree/v0.1.1)
- [hyprqt6engine 0.1.0](https://github.com/hyprwm/hyprqt6engine/tree/v0.1.0)
- [hyprsysteminfo 0.2.0](https://github.com/hyprwm/hyprsysteminfo/tree/v0.2.0)
- [hyprland-guiutils 0.2.1](https://github.com/hyprwm/hyprland-guiutils/tree/v0.2.1)
- [hyprland-qt-support 0.1.0](https://github.com/hyprwm/hyprland-qt-support/tree/v0.1.0)
- [hyprtavern](https://github.com/hyprwm/hyprtavern)
- [hyprwire-protocols](https://github.com/hyprwm/hyprwire-protocols)

### Integration-file examples

- [hyprpaper user unit](https://github.com/hyprwm/hyprpaper/blob/c011bd20886ea3301474e77d7fa4d22ab013ece0/systemd/hyprpaper.service.in)
- [hypridle user unit](https://github.com/hyprwm/hypridle/blob/128dcfa96dfc9c90136c9a80c6e2443f8b54928c/systemd/hypridle.service.in)
- [hyprsunset user-unit install](https://github.com/hyprwm/hyprsunset/blob/25f704346ec22e7623b0873ef8c4573b57ca1512/CMakeLists.txt)
- [hyprlock PAM file](https://github.com/hyprwm/hyprlock/blob/ef8ebe821be16394747c09fa0881c9322a56f7f1/pam/hyprlock)
- [portal D-Bus service](https://github.com/hyprwm/xdg-desktop-portal-hyprland/blob/0e832b50ecc49d4bae01a29845c1b3fafc5c5c99/org.freedesktop.impl.portal.desktop.hyprland.service.in)
- [portal descriptor](https://github.com/hyprwm/xdg-desktop-portal-hyprland/blob/0e832b50ecc49d4bae01a29845c1b3fafc5c5c99/hyprland.portal)
- [hyprpolkitagent user unit](https://github.com/hyprwm/hyprpolkitagent/blob/0ee0fd94464434c87c3e8a4b98b56ab6f0466760/assets/hyprpolkitagent-service.in)
- [hyprpolkitagent D-Bus service](https://github.com/hyprwm/hyprpolkitagent/blob/0ee0fd94464434c87c3e8a4b98b56ab6f0466760/assets/hyprpolkitagent-dbus.in)
- [hyprpwcenter desktop file](https://github.com/hyprwm/hyprpwcenter/blob/fd4fd52bd3fe7fbefa23a93acf44cd8b9a2a0a0b/contrib/hyprpwcenter.desktop)
- [hyprsysteminfo desktop file](https://github.com/hyprwm/hyprsysteminfo/blob/b68809ab37c00676db1dcfe734d2548260ea658f/assets/install/hyprsysteminfo.desktop)
- [plugin compatibility pins at audited commit](https://github.com/hyprwm/hyprland-plugins/blob/7644cecdb947060682891a0db2a0cdc5c0b9e704/hyprpm.toml)
- [guiutils 0.2.1 targets](https://github.com/hyprwm/hyprland-guiutils/tree/v0.2.1/utils)
- [archived qtutils 0.1.5 targets](https://github.com/hyprwm/hyprland-qtutils/tree/v0.1.5/utils)

## Fedora policy and tooling

- [Fedora Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/)
- [CMake packaging guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/CMake/)
- [Meson packaging guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/Meson/)
- [Systemd packaging guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/Systemd/)
- [Licensing guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/)
- [Package naming](https://docs.fedoraproject.org/en-US/packaging-guidelines/Naming/)
- [Versioning](https://docs.fedoraproject.org/en-US/packaging-guidelines/Versioning/)
- [Source URL guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/SourceURL/)
- [Weak dependencies](https://docs.fedoraproject.org/en-US/packaging-guidelines/WeakDependencies/)
- [Unowned directories](https://docs.fedoraproject.org/en-US/packaging-guidelines/UnownedDirectories/)
- [AppStream/AppData](https://docs.fedoraproject.org/en-US/packaging-guidelines/AppData/)
- [Users and groups](https://docs.fedoraproject.org/en-US/packaging-guidelines/UsersAndGroups/)
- [Fedora 44 build flags](https://src.fedoraproject.org/rpms/redhat-rpm-config/raw/f44/f/buildflags.md)
- [Mock documentation](https://rpm-software-management.github.io/mock/)
- [Fedora Package Maintenance Guide](https://docs.fedoraproject.org/en-US/package-maintainers/Package_Maintenance_Guide/)
- [DNF5 configuration reference](https://dnf5.readthedocs.io/en/latest/dnf5.conf.5.html)
- [DNF5 history](https://dnf5.readthedocs.io/en/latest/commands/history.8.html)
- [DNF5 offline transactions](https://dnf5.readthedocs.io/en/latest/commands/offline.8.html)
- [Fedora reproducible builds change](https://fedoraproject.org/wiki/Changes/ReproduciblePackageBuilds)

## Fedora package history

- [retired Hyprland spec](https://src.fedoraproject.org/rpms/hyprland/raw/ae2f9c98ecbb4f9b4177a48438cf586f352d94e7/f/hyprland.spec)
- [Hyprland retirement marker](https://src.fedoraproject.org/rpms/hyprland/raw/e4974798107d72a89e3c3f828d5133bdd1a874a0/f/dead.package)
- [hypridle dist-git](https://src.fedoraproject.org/rpms/hypridle)
- [hyprlock dist-git](https://src.fedoraproject.org/rpms/hyprlock)
- [hyprpaper dist-git](https://src.fedoraproject.org/rpms/hyprpaper)
- [hyprpicker dist-git](https://src.fedoraproject.org/rpms/hyprpicker)
- [xdg-desktop-portal-hyprland dist-git](https://src.fedoraproject.org/rpms/xdg-desktop-portal-hyprland)
- [aquamarine dist-git](https://src.fedoraproject.org/rpms/aquamarine)
- [udis86 spec](https://src.fedoraproject.org/rpms/udis86/raw/rawhide/f/udis86.spec)

### Fedora 44 Hypr library builds

- [hyprutils 0.7.1](https://packages.fedoraproject.org/pkgs/hyprutils/hyprutils/fedora-44.html)
- [hyprcursor 0.1.11](https://packages.fedoraproject.org/pkgs/hyprcursor/hyprcursor/fedora-44.html)
- [hyprwayland-scanner-devel 0.4.2](https://packages.fedoraproject.org/pkgs/hyprwayland-scanner/hyprwayland-scanner-devel/fedora-44.html)
- [hyprland-protocols-devel 0.4.0](https://packages.fedoraproject.org/pkgs/hyprland-protocols/hyprland-protocols-devel/fedora-44.html)
- [hyprlang 0.6.4](https://packages.fedoraproject.org/pkgs/hyprlang/hyprlang/fedora-44.html)
- [hyprgraphics 0.1.5](https://packages.fedoraproject.org/pkgs/hyprgraphics/hyprgraphics/fedora-44.html)
- [Fedora 44 Lua 5.4 development package](https://packages.fedoraproject.org/pkgs/lua/lua-devel/fedora-44.html)
- [Rawhide Lua 5.5 development package](https://packages.fedoraproject.org/pkgs/lua/lua-devel/fedora-rawhide.html)
- [Fedora glaze package search](https://packages.fedoraproject.org/search?query=glaze)
- [Fedora UWSM package search](https://packages.fedoraproject.org/search?query=uwsm)

The full external Fedora 44 dependency matrix links each package page directly
in [Fedora packaging design](fedora-packaging-design.md#stock-fedora-dependencies-that-meet-the-stable-tagged-requirements).

## Downstream packaging

### openSUSE

- [Hyprland spec, OBS revision 157](https://api.opensuse.org/public/source/X11:Wayland/hyprland/hyprland.spec?rev=157)
- [Hyprland OBS source service](https://api.opensuse.org/public/source/X11:Wayland/hyprland/_service)
- [X11:Wayland project](https://build.opensuse.org/project/show/X11:Wayland)

### Arch Linux

- [Hyprland 0.55.4 packaging commit](https://gitlab.archlinux.org/archlinux/packaging/packages/hyprland/-/commit/cdfe2c3062da1745b0aaa59874663088b0d4b7c4)
- [Aquamarine rebuild commit](https://gitlab.archlinux.org/archlinux/packaging/packages/hyprland/-/commit/c4c42cc84192cd7e0459a3a9bbd4a38a6feab129)

### Nix

- [Nixpkgs Hyprland package](https://github.com/NixOS/nixpkgs/tree/master/pkgs/by-name/hy/hyprland)
- [hyprnix flake](https://github.com/hyprwm/hyprnix/blob/main/flake.nix)
- [hyprnix updater](https://github.com/hyprwm/hyprnix/blob/main/update.py)

### Gentoo

- [Official-suite last-rite commit](https://github.com/gentoo/gentoo/commit/1d4db2ff53c5461db0c8aa1a93f4707593c8a4f3)
- [hyproverlay](https://codeberg.org/hyproverlay/hyproverlay)

### Debian and Ubuntu

- [Debian Hyprland 0.55.4+ds-2](https://sources.debian.org/src/hyprland/0.55.4+ds-2/)
- [Debian control](https://sources.debian.org/data/main/h/hyprland/0.55.4+ds-2/debian/control)
- [Debian repack rationale](https://sources.debian.org/src/hyprland/0.55.4+ds-2/debian/README.source/)
- [Ubuntu 26.04 Hyprland](https://packages.ubuntu.com/resolute/hyprland)
- [Ubuntu 25.10 Hyprland](https://packages.ubuntu.com/questing/hyprland)

### COPR reference implementations

- [solopasha/hyprlandRPM](https://github.com/solopasha/hyprlandRPM)
- [AshBuk/Hyprland-Fedora](https://github.com/AshBuk/Hyprland-Fedora)

These projects are packaging references only. They are not dependencies of
the repository designed here.
