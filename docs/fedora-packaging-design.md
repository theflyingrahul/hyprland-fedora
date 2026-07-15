# Fedora packaging design

## Design goals

The package architecture must:

- use separate native RPM source packages;
- resolve through ordinary DNF transactions;
- follow Fedora naming, filesystem, macro, license, and dependency practices;
- avoid COPR and private bundled prefixes;
- keep the compositor usable with only weakly recommended companions;
- support a complete desktop through a meta package;
- rebuild coherently when internal ABIs change;
- remain compatible with Mock and Koji-style isolated builds.

## Supported package tiers

### Tier 1: compositor foundation

Required to build and run Hyprland:

- hyprwayland-scanner
- hyprutils
- hyprlang
- hyprgraphics
- hyprcursor
- aquamarine
- hyprland-protocols
- hyprland

### Tier 2: recommended desktop integration

Installed by default either directly through weak dependencies of `hyprland`
or transitively as hard dependencies of another recommended component. The
complete set is guaranteed by the `hyprland-desktop` meta package:

- xdg-desktop-portal-hyprland
- hyprpaper
- hyprlock
- hypridle
- hyprsunset
- hyprpolkitagent
- hyprwire
- hyprtoolkit

### Tier 3: stable optional applications

- hyprpicker
- hyprlauncher
- hyprpwcenter
- hyprshutdown
- hyprsysteminfo
- hyprland-guiutils
- hyprqt6engine
- hyprland-qt-support

### Tier 4: exact-ABI plugins

- hyprland-plugin-borders-plus-plus
- hyprland-plugin-csgo-vulkan-fix
- hyprland-plugin-hyprbars
- hyprland-plugin-hyprfocus
- `hyprland-plugins` meta package

The plugin source must be the exact commit selected by upstream's
`hyprpm.toml` for the packaged Hyprland commit. A similarly numbered plugin
tag is not sufficient evidence.

### Deferred from the first stable repository

- hyprtavern: no stable tag and no systemd integration contract.
- hyprwire-protocols: no tag, version, build system, install rule, or
  pkg-config template.
- hyprland-qtutils: archived and replaced.
- hyprland-welcome: archived and moved into guiutils.
- wlroots-hyprland: archived and replaced by aquamarine.
- Hypr: separate X11 window manager, not part of the Hyprland graph.
- contrib: independently reviewable scripts, not a single coherent binary
  package.

Deferral is a support decision, not an assertion that these sources cannot
ever be packaged.

## Source and binary package layout

| Source package | Binary packages | Contents and rationale |
|---|---|---|
| `hyprutils` | `hyprutils`, `hyprutils-devel` | Shared library; headers, unversioned linker symlink, and pkg-config metadata split into `-devel` |
| `hyprlang` | `hyprlang`, `hyprlang-devel` | Shared parser library and development files |
| `hyprgraphics` | `hyprgraphics`, `hyprgraphics-devel` | Shared graphics library and development files |
| `hyprcursor` | `hyprcursor`, `hyprcursor-devel` | Runtime library plus `hyprcursor-util`; development files split |
| `aquamarine` | `aquamarine`, `aquamarine-devel` | Runtime backend library and development files |
| `hyprwayland-scanner` | `hyprwayland-scanner-devel` | Retains Fedora's existing binary-package name; contains the build-tool executable, pkg-config file, and CMake config |
| `hyprland-protocols` | `hyprland-protocols-devel` | Architecture-independent XML and pkg-config build data; retain Fedora's existing binary-package convention |
| `hyprwire` | `hyprwire`, `hyprwire-devel`, `hyprwire-scanner-devel` | Runtime library, development files, and independently consumable code generator; no approved stable in-repository consumer needs the scanner yet |
| `hyprtoolkit` | `hyprtoolkit`, `hyprtoolkit-devel` | Runtime GUI library and development files |
| `hyprland` | `hyprland`, `hyprland-devel`, `hyprland-backgrounds`, `hyprpm` | Compositor/runtime files; plugin headers and `hyprland.pc`; large noarch backgrounds; optional local plugin build manager |
| `hyprpaper` | `hyprpaper` | Binary and user unit |
| `hyprlock` | `hyprlock` | Binary, PAM configuration, documentation/example config |
| `hypridle` | `hypridle` | Binary and user unit |
| `hyprpicker` | `hyprpicker` | Binary and manual |
| `hyprsunset` | `hyprsunset` | Binary and user unit |
| `xdg-desktop-portal-hyprland` | same name | Portal backend, share picker, portal descriptor, D-Bus activation, user unit |
| `hyprpolkitagent` | same name | Authentication agent, D-Bus activation, user unit |
| `hyprlauncher` | same name | Launcher binary |
| `hyprpwcenter` | same name | PipeWire GUI and desktop entry |
| `hyprshutdown` | same name | Shutdown UI |
| `hyprsysteminfo` | same name | System information GUI and desktop entry |
| `hyprland-guiutils` | same name | Dialog, donate, update, welcome, and run utilities |
| `hyprqt6engine` | same name | Qt platform-theme/plugin files |
| `hyprland-qt-support` | same name | QML style-provider module |
| `hyprland-plugins` | four plugin packages plus `hyprland-plugins` meta | Per-plugin installation/removal with one source build |
| `hyprwm-meta` | `hyprland-desktop`, `hyprwm-complete` | Noarch dependency-only packages |
| `glaze` | `glaze-devel` | Header-only C++ dependency and CMake package needed by hyprpm and newer apps |
| `lua5.5` | `lua5.5`, `lua5.5-libs`, `lua5.5-devel` | Parallel-installable Lua 5.5 tool, library, headers, and `lua5.5.pc` for Fedora 44 |
| `hyprwm-fedora-release-local` | same name | Unsigned local filesystem repository configuration; signed snapshots distribute their checked `.repo` file and public key separately |

No separate completion subpackages are planned initially. Shell completions
are small and belong with the executable package that uses them. They can be
split later only if repository measurements show a practical benefit.

## Core package dependency policy

### Build dependencies

Specs express build dependencies with Fedora virtual provides where possible:

- `pkgconfig(hyprutils)`
- `pkgconfig(hyprlang)`
- `pkgconfig(hyprgraphics)`
- `pkgconfig(hyprcursor)`
- `pkgconfig(aquamarine)`
- `pkgconfig(hyprland-protocols)`
- `pkgconfig(hyprwire)`
- `pkgconfig(hyprtoolkit)`
- `cmake(hyprwayland-scanner)`
- `cmake(hyprwire-scanner)`

Upstream pkg-config templates omit several transitive dependencies. Each spec
must include every direct dependency from the tagged build manifest rather
than assume `pkg-config --libs` is complete.

### Runtime dependencies

RPM's automatic ELF dependency generator records shared-library SONAMEs. Add
explicit internal minimum package versions where upstream declares a minimum
that cannot be represented by a SONAME alone.

Examples for Hyprland 0.55.4:

- aquamarine >= 0.9.3
- hyprlang >= 0.6.7
- hyprcursor >= 0.1.7
- hyprutils >= 0.13.1
- hyprgraphics >= 0.5.1

Do not add runtime requirements for build-only protocol XML or scanner
executables.

Every `-devel` package requires its matching runtime library with exact EVR:

```text
Requires: %{name}%{?_isa} = %{version}-%{release}
```

Public header dependencies that consumers need must also be represented in
the `-devel` package even when upstream's `.pc` file omits them.

## External Fedora 44 dependency feasibility

### Stock Fedora dependencies that meet the stable tagged requirements

| Upstream token or feature | Fedora 44 package(s) | Observed Fedora 44 version/result |
|---|---|---|
| C++ compiler | [`gcc-c++`](https://packages.fedoraproject.org/pkgs/gcc/gcc-c++/fedora-44.html) | GCC 16 snapshot accepts the requested C++26 dialect; actual Mock build remains authoritative |
| CMake/Meson/pkg-config | [`cmake`](https://packages.fedoraproject.org/pkgs/cmake/cmake/fedora-44.html), [`meson`](https://packages.fedoraproject.org/pkgs/meson/meson/fedora-44.html), `pkgconf-pkg-config`, `ninja-build` | New enough for all tagged sources |
| Wayland client/server/EGL | [`wayland-devel`](https://packages.fedoraproject.org/pkgs/wayland/wayland-devel/fedora-44.html) | 1.24.0; meets Hyprland server floor 1.22.91 |
| Wayland protocols | [`wayland-protocols-devel`](https://packages.fedoraproject.org/pkgs/wayland-protocols/wayland-protocols-devel/fedora-44.html) | 1.47; exactly meets Hyprland 0.55.4 floor 1.47 |
| input and seat | [`libinput-devel`](https://packages.fedoraproject.org/pkgs/libinput/libinput-devel/fedora-44.html), [`libseat-devel`](https://packages.fedoraproject.org/pkgs/seatd/libseat-devel/fedora-44.html) from `seatd` | 1.31.0 and 0.9.3; meet upstream floors |
| DRM/GBM/EGL/GLES | [`libdrm-devel`](https://packages.fedoraproject.org/pkgs/libdrm/libdrm-devel/fedora-44.html), [Mesa development packages](https://packages.fedoraproject.org/pkgs/mesa/) | Available and current |
| display/hardware data | [`libdisplay-info-devel`](https://packages.fedoraproject.org/pkgs/libdisplay-info/libdisplay-info-devel/fedora-44.html), [`hwdata`](https://packages.fedoraproject.org/pkgs/hwdata/hwdata/fedora-44.html), systemd/libudev development files | Available |
| graphics base | [`pixman-devel`](https://packages.fedoraproject.org/pkgs/pixman/pixman-devel/fedora-44.html), [`cairo-devel`](https://packages.fedoraproject.org/pkgs/cairo/cairo-devel/fedora-44.html), [`pango-devel`](https://packages.fedoraproject.org/pkgs/pango/pango-devel/fedora-44.html), [`librsvg2-devel`](https://packages.fedoraproject.org/pkgs/librsvg2/librsvg2-devel/fedora-44.html) | Available |
| image formats | [`libjpeg-turbo-devel`](https://packages.fedoraproject.org/pkgs/libjpeg-turbo/libjpeg-turbo-devel/fedora-44.html), [`libwebp-devel`](https://packages.fedoraproject.org/pkgs/libwebp/libwebp-devel/fedora-44.html), [`libpng-devel`](https://packages.fedoraproject.org/pkgs/libpng/libpng-devel/fedora-44.html), [`libjxl-devel`](https://packages.fedoraproject.org/pkgs/jpegxl/libjxl-devel/fedora-44.html), [`libheif-devel`](https://packages.fedoraproject.org/pkgs/libheif/libheif-devel/fedora-44.html), [`file-devel`](https://packages.fedoraproject.org/pkgs/file/file-devel/fedora-44.html) | Available; declare optional hyprgraphics formats explicitly for deterministic features |
| XKB/cursor/XCB | [`libxkbcommon-devel`](https://packages.fedoraproject.org/pkgs/libxkbcommon/libxkbcommon-devel/fedora-44.html), [`libXcursor-devel`](https://packages.fedoraproject.org/pkgs/libXcursor/libXcursor-devel/fedora-44.html), [`libxcb-devel`](https://packages.fedoraproject.org/pkgs/libxcb/libxcb-devel/fedora-44.html), xcb-util development packages | Available |
| PipeWire/SPA | [`pipewire-devel`](https://packages.fedoraproject.org/pkgs/pipewire/pipewire-devel/fedora-44.html) | 1.6.2; exceeds portal floor |
| D-Bus C++ | [`sdbus-cpp-devel`](https://packages.fedoraproject.org/pkgs/sdbus-cpp/sdbus-cpp-devel/fedora-44.html) | 2.2.1; provides the upstream `sdbus-c++` pkg-config module and exceeds current floors |
| PAM | [`pam-devel`](https://packages.fedoraproject.org/pkgs/pam/pam-devel/fedora-44.html) | Available |
| zip/TOML/XML | [`libzip-devel`](https://packages.fedoraproject.org/pkgs/libzip/libzip-devel/fedora-44.html), [`tomlplusplus-devel`](https://packages.fedoraproject.org/pkgs/tomlplusplus/tomlplusplus-devel/fedora-44.html), [`pugixml-devel`](https://packages.fedoraproject.org/pkgs/pugixml/pugixml-devel/fedora-44.html) | Available |
| math/parsing/color | [`re2-devel`](https://packages.fedoraproject.org/pkgs/re2/re2-devel/fedora-44.html), [`muparser-devel`](https://packages.fedoraproject.org/pkgs/muParser/muParser-devel/fedora-44.html), [`lcms2-devel`](https://packages.fedoraproject.org/pkgs/lcms2/lcms2-devel/fedora-44.html) | Available |
| shader compiler | [`glslang-devel`](https://packages.fedoraproject.org/pkgs/glslang/glslang-devel/fedora-44.html) | Provides the required CMake package |
| GLib/GIO/UUID/FFI | [`glib2-devel`](https://packages.fedoraproject.org/pkgs/glib2/glib2-devel/fedora-44.html), [`libuuid-devel`](https://packages.fedoraproject.org/pkgs/util-linux/libuuid-devel/fedora-44.html), [`libffi-devel`](https://packages.fedoraproject.org/pkgs/libffi/libffi-devel/fedora-44.html) | Available |
| toolkit helpers | [`iniparser-devel`](https://packages.fedoraproject.org/pkgs/iniparser/iniparser-devel/fedora-44.html), [`abseil-cpp-devel`](https://packages.fedoraproject.org/pkgs/abseil-cpp/abseil-cpp-devel/fedora-44.html) | Abseil provides `pkgconfig(absl_flat_hash_map)` |
| launcher dependencies | [`libicu-devel`](https://packages.fedoraproject.org/pkgs/icu/libicu-devel/fedora-44.html), [`fontconfig-devel`](https://packages.fedoraproject.org/pkgs/fontconfig/fontconfig-devel/fedora-44.html), [`libqalculate-devel`](https://packages.fedoraproject.org/pkgs/libqalculate/libqalculate-devel/fedora-44.html) | ICU 77.1 and libqalculate 5.9.0 observed |
| system information | [`pciutils-devel`](https://packages.fedoraproject.org/pkgs/pciutils/pciutils-devel/fedora-44.html) | 3.14.0 and `libpci.pc` available |
| Qt 6 | [`qt6-qtbase-devel`](https://packages.fedoraproject.org/pkgs/qt6-qtbase/qt6-qtbase-devel/fedora-44.html), [`qt6-qtdeclarative-devel`](https://packages.fedoraproject.org/pkgs/qt6-qtdeclarative/qt6-qtdeclarative-devel/fedora-44.html), [`qt6-qtwayland-devel`](https://packages.fedoraproject.org/pkgs/qt6-qtwayland/qt6-qtwayland-devel/fedora-44.html) | Qt 6.10.2; exceeds hyprqt6engine floor 6.9 |
| optional KF6 integration | [`kf6-kconfig-devel`](https://packages.fedoraproject.org/pkgs/kf6-kconfig/kf6-kconfig-devel/fedora-44.html), [`kf6-kcolorscheme-devel`](https://packages.fedoraproject.org/pkgs/kf6-kcolorscheme/kf6-kcolorscheme-devel/fedora-44.html), [`kf6-kiconthemes-devel`](https://packages.fedoraproject.org/pkgs/kf6-kiconthemes/kf6-kiconthemes-devel/fedora-44.html) | Available; include all three for a deterministic full-feature engine |
| udis86 | [`udis86-devel`](https://packages.fedoraproject.org/pkgs/udis86/udis86-devel/fedora-44.html) | Library and headers available; no pkg-config file |

The tagged Hyprland 0.55.4 requirement is
`wayland-protocols >= 1.47`. The unreleased default branch later raised this
to 1.49. Fedora 44 therefore needs no Wayland-protocols override for the
stable package, but Fedora 44 nightly builds of current `main` may be blocked
while Rawhide already carries 1.49.

### Packages this repository must add

#### glaze-devel

Fedora 44 and Rawhide do not provide glaze
([Fedora package search](https://packages.fedoraproject.org/search?query=glaze)).
Hyprland builds `hyprpm` by default and requests glaze 7.x, otherwise
attempting a network FetchContent clone. Newer optional applications also use
glaze.

Decision:

- package upstream glaze 7.2.0 as a separate `glaze-devel` package;
- install the upstream CMake config and headers;
- use it for every consumer;
- disable all FetchContent fallback;
- validate hyprshutdown and hyprsysteminfo, whose tagged fallbacks reference
  glaze 6.x, against the selected 7.2 API.

If a tagged consumer proves incompatible with glaze 7, that consumer is held
or patched with an upstream-supported change. Two conflicting header trees
are not installed in the same prefix.

#### Parallel Lua 5.5

Fedora 44's
[lua-devel](https://packages.fedoraproject.org/pkgs/lua/lua-devel/fedora-44.html)
is 5.4.8. Rawhide's
[lua-devel](https://packages.fedoraproject.org/pkgs/lua/lua-devel/fedora-rawhide.html)
moved the primary package to 5.5.
Hyprland's CMake search contains alternatives that can accidentally accept
the final `lua < 5.6` expression and silently select Fedora 44's Lua 5.4,
despite the preceding 5.5-specific module names and `lua >= 5.5` expression.

Decision:

- provide a parallel-installable `lua5.5` source package for Fedora 44;
- do not replace Fedora's system `lua` or `lua-libs`;
- install a versioned interpreter, library, include directory, and
  `lua5.5.pc`;
- make Hyprland's configure result fail unless the selected module reports
  Lua 5.5.x;
- stop publishing the compatibility package for Fedora releases whose
  standard Lua is 5.5 or newer.

This avoids a system-wide Lua ABI replacement and follows the upstream
version intent instead of relying on the permissive search-expression bug.

### Conditional source-compatibility gate: udis86

Fedora's `udis86-devel` lacks `udis86.pc`, but Hyprland has a direct
`find_library` fallback. Add `BuildRequires: udis86-devel` explicitly and
verify that the tagged source compiles, links, and passes tests with Fedora's
library.

If the Fedora library lacks APIs or fixes from Hyprland's fork:

1. document the exact incompatibility;
2. prefer an upstreamable compatibility patch;
3. otherwise package the maintained fork under a parallel name and patch
   Hyprland to link it without file conflicts;
4. request a bundling exception only if parallel packaging is technically
   impossible.

The build must never reach the bundled submodule silently.

### UWSM

Fedora 44 and Rawhide do not package UWSM
([Fedora package search](https://packages.fedoraproject.org/search?query=uwsm)).
Hyprland can install an additional UWSM session entry by default.

Initial decision:

- build Hyprland with `NO_UWSM=ON`;
- ship the normal Hyprland Wayland session;
- do not install a desktop entry that invokes a missing executable.

UWSM can be added later as an independently reviewed external source package,
after which the session entry can be enabled in the same release transaction.

## Hyprland package design

### `hyprland`

Owns:

- compositor executable and lowercase symlink;
- `hyprctl`, `start-hyprland`, and other ordinary runtime tools;
- normal Wayland session desktop file;
- XDG portal configuration supplied by Hyprland;
- systemd integration that does not require UWSM;
- manuals, Lua stubs, small runtime assets, and licenses.

Build policy:

- XWayland enabled;
- systemd enabled;
- UWSM disabled until packaged;
- hyprpm enabled through packaged glaze;
- Tracy disabled;
- tests enabled where the tagged source supports them;
- deterministic Git metadata injected;
- LTO disabled;
- upstream hard-coded optimization removed.

### `hyprland-devel`

Owns:

- `/usr/include/hyprland/` internal/plugin headers;
- generated protocol headers;
- `/usr/share/pkgconfig/hyprland.pc`;
- other files required to compile external plugins.

Requires the exact `hyprland` EVR and the development dependencies exposed by
the headers.

### `hyprland-backgrounds`

Owns large architecture-independent wallpaper/background assets and requires
no architecture-specific runtime.

`hyprland` recommends this package rather than hard-requiring it.

### `hyprpm`

Owns:

- `hyprpm`;
- its shell completions;
- plugin-manager-specific documentation.

`hyprpm` clones and compiles plugins on the user's machine. Keeping it in the
main compositor package would either leave a command that fails without a
toolchain or force every compositor installation to pull compilers and
development headers.

The subpackage therefore requires:

- exact `hyprland-devel`;
- `git-core`;
- CMake and the build backend used by supported plugins;
- `gcc-c++` and ordinary native build tools;
- pkg-config.

Packaged official plugins remain the preferred reproducible path. `hyprpm` is
optional for users who intentionally build third-party plugins locally.

## Provides

### Automatic provides

Allow RPM generators to produce:

- shared-library SONAME provides;
- `pkgconfig(...)` provides;
- CMake provides where installed;
- executable and MIME/desktop metadata where standard generators apply.

Do not replace generated dependencies with hand-written approximations.

### Manual provides

`hyprland`:

- `Provides: wayland-compositor`
- versioned `Provides: hyprland-plugin-api = <exact Hyprland EVR>`

Plugin packages require both:

- exact `hyprland` EVR; and
- exact `hyprland-plugin-api`.

The duplicate check is intentional: the package relationship is
human-readable while the virtual capability makes ABI purpose explicit.

## Weak dependencies and meta packages

### `hyprland`

Recommended:

- xdg-desktop-portal-hyprland
- hyprpaper
- hypridle
- hyprlock
- hyprsunset
- hyprpolkitagent
- hyprland-backgrounds
- xorg-x11-server-Xwayland

Suggested:

- hyprpm
- hyprpicker
- hyprlauncher
- hyprpwcenter
- hyprshutdown
- hyprsysteminfo
- hyprland-guiutils
- hyprqt6engine
- hyprland-qt-support

DNF installs `Recommends` by default. Users can obtain a minimal compositor
with weak dependencies disabled.

### `hypridle`

`Recommends: hyprlock`, because lock invocation is the common configuration
but not an intrinsic daemon requirement.

### `hyprland-desktop`

Hard-requires the supported standard desktop set:

- hyprland
- portal
- wallpaper
- idle and lock
- night-light/color-temperature support
- polkit agent
- XWayland

This package is for users who want the complete supported baseline even when
weak dependencies are globally disabled.

### `hyprwm-complete`

Requires `hyprland-desktop` and every stable optional Tier 3 application.
The local plugin manager and plugin RPMs remain separate opt-ins because of
their toolchain footprint, tighter ABI, and support surface.

## Conflicts, Obsoletes, and transitions

### No broad conflicts

- Hyprland does not conflict with GNOME, KDE, Sway, or other compositors.
- xdg-desktop-portal-hyprland does not conflict with other portal backends.
- Qt theme components do not conflict with unrelated Qt themes merely because
  both are installed.

Portal selection is solved through correct portal/session metadata, not RPM
conflicts.

### Existing Fedora packages

Use the same package names and normal higher EVRs so DNF performs an upgrade.
Do not add `Obsoletes` for the same package name.

Preserve any official Fedora Epoch that exists. Do not add a new Epoch merely
to outrank arbitrary COPR packages; migration from third-party epochs is
documented below.

### Archived replacements

Tagged guiutils 0.2.1 installs the same `hyprland-dialog`,
`hyprland-update-screen`, and `hyprland-donate-screen` command names as
qtutils 0.1.5, and also installs `hyprland-welcome`. It is the upstream
successor. Use Fedora's normal rename/replacement pair:

- versioned `Obsoletes: hyprland-qtutils < 0.2.0`;
- versioned `Provides: hyprland-qtutils = %{version}-%{release}`;
- versioned `Obsoletes: hyprland-welcome < 0.2.0`;
- versioned `Provides: hyprland-welcome = %{version}-%{release}`.

The archived sources are not built in this repository.

### Migration from COPR packages and epochs

The release documentation includes a migration procedure:

1. identify installed Hypr packages and their source repository/EVR;
2. disable and remove conflicting COPR repository definitions;
3. use `dnf distro-sync` or an explicit `dnf swap`/remove-and-install
   transaction with `--allowerasing` when a COPR package carries a higher
   Epoch;
4. verify that every installed Hypr package now comes from this repository or
   Fedora.

This repository does not add an Epoch solely to outrank a third-party COPR.
Users with a higher third-party Epoch require the documented one-time
migration transaction.

## File ownership

### Runtime libraries

Own only versioned shared objects and licenses in the runtime package.

### Development packages

Own:

- headers;
- unversioned `.so` linker symlink;
- pkg-config files;
- CMake package files;
- development-only code generators only where no separate tool package is
  defined.

### Common directories

Specs explicitly own project-specific directories they create. They do not
claim ownership of common system directories such as:

- `%{_bindir}`
- `%{_libdir}`
- `%{_datadir}/applications`
- `%{_userunitdir}`
- D-Bus system directories

Where multiple Hypr packages use `/usr/share/hypr`, RPM directory
co-ownership with identical mode/ownership is acceptable and explicit. A
filesystem-only package is introduced only if implementation proves that
co-ownership causes maintainability problems.

### No unmanaged paths

No package installs under:

- `/usr/local`
- a home directory
- `/opt`
- a private bundled library prefix

All generated state belongs under standard user cache/config/state paths at
runtime and is not owned by RPM.

## Desktop and AppStream metadata

Upstream currently provides desktop entries only for selected applications
and no inspected AppStream metainfo.

Policy:

- validate every upstream desktop file;
- add downstream metainfo for user-facing GUI applications where Fedora
  software-center integration is appropriate;
- use the same reverse-DNS basename for desktop and metainfo files;
- install icons in standard hicolor locations;
- submit metadata upstream;
- keep downstream metadata as package-local source files until accepted.

Command-oriented tools such as hyprpicker do not receive artificial desktop
entries solely to appear in a GUI store.

## systemd user integration

Install upstream user units to `%{_userunitdir}` and use Fedora's
`%systemd_user_*` lifecycle macros.

Initial preset policy:

- do not globally enable hyprpaper, hypridle, or hyprsunset;
- preserve explicit user choice and Hyprland configuration;
- allow D-Bus activation for services designed for it;
- ensure units stop with the graphical session;
- test login, logout, restart, and multiple user sessions.

The non-UWSM Hyprland session does not automatically start
`graphical-session.target` or these optional daemons. Installation therefore
means the companions and units are available, not that all are activated.
For the initial non-UWSM profile, package documentation uses ordinary
Hyprland `exec-once` actions equivalent to:

```text
hyprpaper
hypridle
hyprpolkitagent
```

Users may add `hyprsunset`. The installed systemd units remain available for
UWSM or another correctly managed `graphical-session.target`, but are not
globally enabled for non-Hyprland sessions. No package edits a user's
configuration automatically.

No system service or system user is needed for the stable package set.

## D-Bus, portal, and polkit

### Portal

The portal package owns:

- its libexec backend;
- share picker;
- `.portal` descriptor;
- D-Bus service file;
- user unit when enabled by the selected upstream build mode.

It hard-requires `xdg-desktop-portal`. It does not retain obsolete `grim` or
`slurp` runtime requirements unless current tagged source actually executes
them.

### Polkit agent

The agent communicates with polkit over D-Bus through sdbus-c++. It still
requires the polkit runtime service to provide useful authentication.

Install the executable in libexec and keep the D-Bus service and systemd user
unit executable paths identical.

## PAM

`hyprlock` owns `/etc/pam.d/hyprlock` as `%config(noreplace)`.

The default stack must be reviewed against Fedora's `system-auth` convention
and tested for:

- correct password authentication;
- locked accounts;
- smart-card/fingerprint configurations managed through authselect;
- package upgrade preserving administrator changes;
- failure without bypassing authentication.

No PAM file is generated at install time.

## File capabilities

Debian and Gentoo grant `cap_sys_nice` to Hyprland; the retired Fedora package
did not.

Initial decision: do **not** grant the capability.

Rationale:

- it is a broad privilege on a large in-process C++ compositor with plugin
  support;
- upstream metadata does not make it a hard runtime requirement;
- the compositor remains functional without it;
- performance benefit must be measured against the security expansion.

Capability use can be reconsidered through a separate reviewed change with
latency measurements and a security analysis.

## SELinux

Do not ship a custom SELinux policy initially.

All stable components run in the user session or install ordinary shared
libraries and metadata. Test with SELinux enforcing and add policy only for a
reproducible denial that cannot be fixed through standard paths, D-Bus policy,
permissions, or systemd configuration.

## Documentation and licenses

Each source package installs:

- upstream license text with `%license`;
- relevant README/change documentation without duplicating large developer
  content;
- packaged manual pages;
- package-specific Fedora notes only where behavior differs.

Subpackages that can be installed independently must have access to their
applicable license text.

## Debug packages

Use Fedora's automatic `-debuginfo` and `-debugsource` generation. Do not
create hand-written debug subpackages and do not strip binaries manually.

## Fedora 44 bootstrap order

1. `glaze-devel` and parallel `lua5.5` prerequisites
2. `hyprwayland-scanner`, `hyprutils`, `hyprland-protocols-devel`
3. `hyprlang`, `hyprgraphics`, `hyprwire`, `hyprwire-scanner-devel`
4. `hyprcursor`, `aquamarine`
5. `hyprtoolkit`
6. `hyprland`
7. recommended applications and portal
8. optional applications
9. exact-commit plugins
10. meta and release packages

The glaze and Lua compatibility packages do not block the lowest-level Hypr
libraries and may build in parallel with them; they are listed first so the
complete prerequisite repository exists before the Hyprland source package is
attempted.

The temporary build repository is regenerated between tiers so every Mock
build resolves only published outputs from completed prerequisite tiers.

## Acceptance criteria for implementation

Before the first stable snapshot:

- every source builds from declared sources with networking disabled;
- Fedora 44 uses Lua 5.5, not the accidental Lua 5.4 match;
- glaze is a separate package and no FetchContent path runs;
- system udis86 compatibility is proved or a reviewed alternative is in
  place;
- no UWSM desktop entry points to a missing command;
- the complete dependency graph installs through DNF;
- a clean `dnf install hyprland` provides a loginable compositor session,
  installs the recommended companions, and documents their explicit
  activation without editing user configuration;
- weak-dependency-disabled installation remains valid;
- upgrade from the previous candidate works;
- plugin RPMs load only with their exact Hyprland build;
- desktop, AppStream, PAM, systemd, D-Bus, and portal checks pass;
- all RPM and repository metadata can be signed and verified;
- no COPR or `/usr/local` dependency exists.
