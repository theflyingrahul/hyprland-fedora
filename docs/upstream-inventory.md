# Upstream repository inventory

Audit date: **2026-07-15**

## Method

The organization inventory was enumerated from the
[HyprWM GitHub organization API](https://api.github.com/orgs/hyprwm/repos?per_page=100&type=all).
Versions were then checked with authoritative Git tag refs. Build and export
information was read from tagged `CMakeLists.txt`, `meson.build`,
`*.pc.in`, CMake package templates, install rules, and integration files.

The organization contained 41 public repositories at the audit date.

## Classification

### Core, libraries, and protocols

| Repository | Status and current stable version | Purpose | Packaging classification |
|---|---|---|---|
| [Hyprland](https://github.com/hyprwm/Hyprland) | Active, `v0.55.4` | Wayland compositor | Required target |
| [hyprutils](https://github.com/hyprwm/hyprutils) | Active, `v0.13.1` | Common utility library | Required target |
| [hyprlang](https://github.com/hyprwm/hyprlang) | Active, `v0.6.8` | Hypr configuration-language parser | Required target |
| [hyprgraphics](https://github.com/hyprwm/hyprgraphics) | Active, `v0.5.1` | Image, graphics, and resource utilities | Required target |
| [hyprcursor](https://github.com/hyprwm/hyprcursor) | Active, `v0.1.13` | Hypr cursor-format library and utility | Required target |
| [aquamarine](https://github.com/hyprwm/aquamarine) | Active, `v0.12.1` | DRM, KMS, input, and rendering backend | Required target |
| [hyprwayland-scanner](https://github.com/hyprwm/hyprwayland-scanner) | Active, `v0.4.6` | C++ Wayland protocol code generator | Required build-tool target; Fedora binary package is `hyprwayland-scanner-devel` |
| [hyprland-protocols](https://github.com/hyprwm/hyprland-protocols) | Active, `v0.7.0` | Hyprland Wayland protocol XML | Required build-data target |
| [hyprwire](https://github.com/hyprwm/hyprwire) | Active, `v0.3.1` | IPC wire library and scanner | Required by newer applications |
| [hyprwire-protocols](https://github.com/hyprwm/hyprwire-protocols) | Active, no tag or version | Hyprwire protocol XML | Experimental build-data target |
| [hyprtavern](https://github.com/hyprwm/hyprtavern) | Active, no tag; `VERSION=0.1.0` | Session-bus and IPC discovery daemon | Experimental; defer from initial stable set |
| [hyprtoolkit](https://github.com/hyprwm/hyprtoolkit) | Active, `v0.5.4` | Native C++ Wayland GUI toolkit | Required by newer applications |

### Applications and integration components

| Repository | Status and current stable version | Purpose | Packaging classification |
|---|---|---|---|
| [hyprpaper](https://github.com/hyprwm/hyprpaper) | Active, `v0.8.4` | Wallpaper daemon and IPC client | Recommended |
| [hyprlock](https://github.com/hyprwm/hyprlock) | Active, `v0.9.5` | GPU-accelerated screen locker | Recommended |
| [hypridle](https://github.com/hyprwm/hypridle) | Active, `v0.1.7` | Idle daemon | Recommended |
| [hyprpicker](https://github.com/hyprwm/hyprpicker) | Active, `v0.4.7` | Wayland color picker | Optional |
| [hyprsunset](https://github.com/hyprwm/hyprsunset) | Active, `v0.4.0` | Color-temperature and CTM controller | Recommended |
| [xdg-desktop-portal-hyprland](https://github.com/hyprwm/xdg-desktop-portal-hyprland) | Active, `v1.3.12` | XDG desktop portal backend | Recommended desktop integration |
| [hyprland-plugins](https://github.com/hyprwm/hyprland-plugins) | Active, latest tag `v0.55.0`; newer commit pins cover Hyprland 0.55.4 | Official runtime-loaded plugins | Optional and exact-ABI-coupled |
| [hyprlauncher](https://github.com/hyprwm/hyprlauncher) | Active, `v0.1.6` | Launcher and picker | Optional |
| [hyprpolkitagent](https://github.com/hyprwm/hyprpolkitagent) | Active, `v0.1.3` | Polkit authentication agent | Recommended desktop integration |
| [hyprpwcenter](https://github.com/hyprwm/hyprpwcenter) | Active, `v0.1.2` | PipeWire control center | Optional |
| [hyprshutdown](https://github.com/hyprwm/hyprshutdown) | Active, `v0.1.1` | Graceful shutdown UI | Optional |
| [hyprqt6engine](https://github.com/hyprwm/hyprqt6engine) | Active, `v0.1.0` | Qt 6 platform-theme engine | Optional |
| [hyprsysteminfo](https://github.com/hyprwm/hyprsysteminfo) | Active, `v0.2.0` | System-information GUI | Optional |
| [hyprland-guiutils](https://github.com/hyprwm/hyprland-guiutils) | Active, `v0.2.1` | Dialog, update, donate, welcome, and run utilities | Optional |
| [hyprland-qt-support](https://github.com/hyprwm/hyprland-qt-support) | Active, `v0.1.0` | Qt Quick Controls style provider | Optional |
| [hyprland-qtutils](https://github.com/hyprwm/hyprland-qtutils) | Archived, `v0.1.5` | Former Qt utility suite | Do not introduce as a new package |
| [hyprland-welcome](https://github.com/hyprwm/hyprland-welcome) | Archived, no tag; `VERSION=0.1.0` | Former standalone welcome application | Do not package; functionality moved to guiutils |

### Related but outside the Hyprland RPM dependency graph

| Repository | Status/version | Purpose | Decision |
|---|---|---|---|
| [Hypr](https://github.com/hyprwm/Hypr) | Active but dormant, tag `1.1.4` | Separate X11/XCB tiling window manager | Out of scope; not a Hyprland dependency |
| [contrib](https://github.com/hyprwm/contrib) | Active scripts collection, tag `v0.1` | Community shell utilities such as Grimblast | Consider later as independently reviewed script packages |
| [wlroots-hyprland](https://github.com/hyprwm/wlroots-hyprland) | Archived, untagged | Historical wlroots fork | Obsolete; replaced by aquamarine |

### Documentation, packaging, and infrastructure repositories

| Repository | Purpose/build form | Versioning and license | RPM decision |
|---|---|---|---|
| [hyprland-wiki](https://github.com/hyprwm/hyprland-wiki) | Hugo documentation site | No tags; BSD-3-Clause | Not an RPM target |
| [hyprland-website](https://github.com/hyprwm/hyprland-website) | SvelteKit/Vite website | Package metadata `1.1.0`; BSD-3-Clause | Not an RPM target |
| [hyprnix](https://github.com/hyprwm/hyprnix) | Upstream Nix release-set flake and updater | No tags; no root license detected | Research input, not an RPM target |
| [hyprland-infra](https://github.com/hyprwm/hyprland-infra) | NixOS infrastructure | No tags; no root license detected | Not an RPM target |
| [RFCs](https://github.com/hyprwm/RFCs) | Project RFC documents | No tags; CC-BY-SA-4.0 | Not an RPM target |
| [standards](https://github.com/hyprwm/standards) | Development standards | No tags; BSD-3-Clause | Policy reference only |
| [aur](https://github.com/hyprwm/aur) | Upstream-maintained AUR PKGBUILDs | No current release process; BSD-3-Clause | Downstream packaging reference |
| [actions](https://github.com/hyprwm/actions) | Shared GitHub Actions, currently Nix-focused | No tags; no root license detected | CI reference only |
| [.github](https://github.com/hyprwm/.github) | Organization profile and policy files | No tags; no root license detected | Not an RPM target |

## Packageable project details

### Core exports

The table describes tagged stable sources, not unreleased default-branch
changes.

| Source | License | Build system | Installed compiled output | SONAME | pkg-config module | CMake package/export |
|---|---|---|---|---:|---|---|
| [Hyprland 0.55.4](https://github.com/hyprwm/Hyprland/tree/v0.55.4) | BSD-3-Clause | CMake >= 3.30, C++26 | `Hyprland` executable and `hyprland` symlink | - | `hyprland` | None |
| [hyprutils 0.13.1](https://github.com/hyprwm/hyprutils/tree/v0.13.1) | BSD-3-Clause | CMake >= 3.19, C++26 | `libhyprutils.so` | 12 | `hyprutils` | None |
| [hyprlang 0.6.8](https://github.com/hyprwm/hyprlang/tree/v0.6.8) | LGPL-3.0-only | CMake >= 3.19, C++23 | `libhyprlang.so` | 2 | `hyprlang` | No installed export; `hypr::hyprlang` is build-tree-only |
| [hyprgraphics 0.5.1](https://github.com/hyprwm/hyprgraphics/tree/v0.5.1) | BSD-3-Clause | CMake >= 3.19, C++26 | `libhyprgraphics.so` | 4 | `hyprgraphics` | None |
| [hyprcursor 0.1.13](https://github.com/hyprwm/hyprcursor/tree/v0.1.13) | BSD-3-Clause | CMake >= 3.19, C++23 | `libhyprcursor.so`, `hyprcursor-util` | 0 | `hyprcursor` | None |
| [aquamarine 0.12.1](https://github.com/hyprwm/aquamarine/tree/v0.12.1) | BSD-3-Clause | CMake >= 3.19, C++23 | `libaquamarine.so` | 11 | `aquamarine` | None |
| [hyprwayland-scanner 0.4.6](https://github.com/hyprwm/hyprwayland-scanner/tree/v0.4.6) | BSD-3-Clause | CMake >= 3.19, C++23 | `hyprwayland-scanner` executable | - | `hyprwayland-scanner` | `hyprwayland-scanner` config package; exports a helper function, not a library target |
| [hyprland-protocols 0.7.0](https://github.com/hyprwm/hyprland-protocols/tree/v0.7.0) | BSD-3-Clause | Meson >= 0.60.3, data-only | Protocol XML | - | `hyprland-protocols` | None |
| [hyprwire 0.3.1](https://github.com/hyprwm/hyprwire/tree/v0.3.1) | BSD-3-Clause | CMake >= 3.19 | `libhyprwire.so`, `hyprwire-scanner` | 3 | `hyprwire` | None |
| [hyprtoolkit 0.5.4](https://github.com/hyprwm/hyprtoolkit/tree/v0.5.4) | BSD-3-Clause | CMake >= 3.19 | `libhyprtoolkit.so` | 5 | `hyprtoolkit` | None |

Only `hyprwayland-scanner` installs a discoverable CMake config package in the
stable core. The other libraries rely on pkg-config and direct library/header
installation.

The stable `.pc.in` files for `hyprutils`, `hyprlang`, `hyprgraphics`,
`hyprcursor`, and `aquamarine` do not consistently encode their transitive
link dependencies. RPM specifications therefore cannot derive complete
`BuildRequires` from pkg-config metadata alone; they must mirror the direct
dependencies in each build manifest.

### Application build and integration surface

| Source | License | Build system | Exported library | Installed integration surface |
|---|---|---|---|---|
| hyprpaper 0.8.4 | BSD-3-Clause | CMake >= 3.12 | None | Binary; systemd user unit |
| hyprlock 0.9.5 | BSD-3-Clause | CMake >= 3.27 | None | Binary; PAM configuration; example configuration |
| hypridle 0.1.7 | BSD-3-Clause | CMake >= 3.19 | None | Binary; systemd user unit |
| hyprpicker 0.4.7 | BSD-3-Clause | CMake >= 3.12 | None | Binary; manual page |
| hyprsunset 0.4.0 | BSD-3-Clause | CMake >= 3.12 | None | Binary; systemd user unit |
| xdg-desktop-portal-hyprland 1.3.12 | BSD-3-Clause | CMake >= 3.19 and Meson >= 0.63 | None | Portal descriptor; D-Bus service; optional systemd user unit; libexec backend and share picker |
| hyprland-plugins 0.55.0 | BSD-3-Clause | CMake >= 3.27 plus per-plugin Makefiles | Four runtime-loaded plugin DSOs | No stable ABI; exact Hyprland commit pins |
| hyprlauncher 0.1.6 | BSD-3-Clause | CMake >= 3.19 | None | Binary |
| hyprpolkitagent 0.1.3 | BSD-3-Clause | CMake >= 3.16 | None | Libexec binary; systemd user unit; D-Bus service |
| hyprpwcenter 0.1.2 | BSD-3-Clause | CMake >= 3.19 | None | Binary; desktop entry |
| hyprshutdown 0.1.1 | BSD-3-Clause | CMake >= 3.19 | None | Binary |
| hyprqt6engine 0.1.0 | BSD-3-Clause | CMake >= 3.16 | Qt plugin | Qt platform-theme/plugin directories |
| hyprsysteminfo 0.2.0 | BSD-3-Clause | CMake >= 3.19 | None | Binary; desktop entry |
| hyprland-guiutils 0.2.1 | BSD-3-Clause | CMake >= 3.12 | None | Multiple utility binaries |
| hyprland-qt-support 0.1.0 | BSD-3-Clause | CMake >= 3.20 | QML module | Qt QML module directories |
| hyprtavern, untagged | BSD-3-Clause | CMake >= 3.19 | None | Daemon and tools; no upstream systemd unit |
| hyprwire-protocols, untagged | BSD-3-Clause | No build system | None | XML only; no upstream install rules or pkg-config file |

No inspected GUI application repository shipped AppStream metadata. Desktop
entries exist only for selected applications. Fedora packaging will need to
validate each upstream desktop file and either add downstream metainfo or
upstream it before software-center integration is considered complete.

## Release cadence

Cadence is irregular and must be handled per repository rather than by a
single polling interval.

| Project | Recent release evidence | Maintenance interpretation |
|---|---|---|
| Hyprland | `0.55.0` through `0.55.4` in 33 days | Fast minor train with patch bursts |
| hyprutils | `0.11.0`, `0.11.1`, `0.12.0`, `0.13.0`, `0.13.1` in about five months | Fast and ABI-sensitive |
| hyprlang | Five `0.6.x` tags from 2025-07 to 2026-01 | Bursty |
| hyprgraphics | `0.2.0` through `0.5.1` in about six months | Fast, expanding feature set |
| aquamarine | `0.9.5` through `0.12.1` in about eight months | Fast and coupled to compositor releases |
| hyprwayland-scanner | `0.4.5` to `0.4.6` took about nine months | Slower tool release cycle |
| hyprcursor | `0.1.12` to `0.1.13` in four months; no release for about a year afterward | Relatively stable/dormant |
| hyprland-protocols | Four patch releases in early 2025, then `0.7.0` in October | Irregular data release |
| hyprpaper | Five releases from 2025-12 to 2026-04 | Active |
| hyprlock | Four `0.9.x` releases from 2025-10 to 2026-04 | Active patch cadence |
| hypridle | Last release 2025-08 | Slow |
| hyprpicker | Three releases from 2026-02 to 2026-05 | Active |
| hyprsunset | Nine-month gap before `0.4.0` on 2026-07-13 | Irregular |
| xdg-desktop-portal-hyprland | Roughly semiannual recent releases | Stable but infrequent |
| hyprtoolkit | Five releases from 2025-12 to 2026-05 | Rapidly evolving |
| hyprlauncher | Five releases from 2025-10 to 2026-04 | Active |
| hyprwire | Six tags from 2025-10 to 2026-04 | Rapidly evolving |
| hyprpolkitagent | Four tags since inception; last 2025-07 | Slow |
| hyprpwcenter | Three tags since 2025-09 | Early-stage |
| hyprshutdown | Two tags | Early-stage |
| hyprqt6engine | One tag with unreleased default-branch changes | Early-stage |
| hyprsysteminfo | Four actual tags; latest `0.2.0` | Irregular |
| hyprland-guiutils | Three tags since 2025-11 | Early-stage |
| hyprland-qt-support | One tag with long unreleased drift | Slow |
| hyprtavern | No tags | Not ready for stable automated updates |
| hyprwire-protocols | No tags | Not ready for stable automated updates |

## Versioning anomalies that packaging must handle

1. Hyprland's patch tags do not necessarily update the `VERSION` file.
   `v0.55.4` still reports the `0.55.0` project version internally.
2. `hyprland-protocols` `v0.7.0` is Meson-only. Commit
   [`3f3860b`](https://github.com/hyprwm/hyprland-protocols/commit/3f3860b869014c00e8b9e0528c7b4ddc335c21ab)
   replaced Meson with CMake after the tag without changing `VERSION`.
3. `hyprsysteminfo` had a `VERSION=0.1.1` commit but no `v0.1.1` tag.
4. `hyprpolkitagent` has a `v0.1.1` tag not represented by a corresponding
   `VERSION`-file change.
5. `hyprland-plugins` has release tags, but compatibility is ultimately
   described by commit pairs in `hyprpm.toml`.
6. `hyprwire-protocols`, `hyprtavern`, and `hyprland-welcome` have no stable
   tag stream.

The update system must therefore inspect Git refs and pinned commits directly.
It must not use `VERSION` files as the sole release detector.
