# Phase 1 investigation report

Audit date: **2026-07-15**

## Outcome

The HyprWM ecosystem can be packaged as native Fedora RPMs without COPR or
`/usr/local`, but it cannot be maintained reliably as a set of independent,
manually updated specs.

The required architecture is:

1. separate source packages for each upstream project;
2. a machine-readable, repository-wide compatibility lock;
3. Mock builds in dependency order;
4. automatic reverse-dependency rebuilds on every internal ABI change;
5. atomic DNF repository snapshots;
6. exact Hyprland/plugin coupling;
7. separate Fedora 44 packages for dependencies not supplied at the required
   version.

No spec file or workflow has been implemented during this phase.

## Scope completed

- Enumerated all 41 repositories in the HyprWM organization.
- Classified required, recommended, optional, experimental, archived, legacy,
  documentation, packaging, and infrastructure repositories.
- Read stable build manifests, pkg-config templates, CMake exports, install
  rules, protocol generation, and integration files.
- Constructed the internal build/link/data/runtime/plugin dependency graph.
- Recorded current stable versions, recent release cadence, licenses, build
  systems, SONAMEs, and exported metadata.
- Surveyed Fedora, RPM Fusion, COPR references, openSUSE, Arch, Nix, Gentoo,
  Void, Debian, and Ubuntu.
- Designed Fedora package/subpackage boundaries, dependency policy, file
  ownership, integration, and transition behavior.
- Designed Mock/Koji-compatible builds, GitHub Actions orchestration, update
  automation, signing, publication, offline use, and rollback.
- Evaluated Fedora build flags, C++26, LTO, debug information, hardening, and
  reproducibility.
- Identified ABI, dependency, desktop-integration, security, and maintenance
  risks with mitigations.

## Principal upstream findings

### Stable core release set

| Component | Version | ABI/build significance |
|---|---:|---|
| Hyprland | 0.55.4 | Patch tag retains internal `VERSION=0.55.0`; plugin ABI is commit-coupled |
| aquamarine | 0.12.1 | SOVERSION 11 |
| hyprutils | 0.13.1 | SOVERSION 12; exact current Hyprland minimum |
| hyprlang | 0.6.8 | SOVERSION 2; LGPL-3.0-only |
| hyprgraphics | 0.5.1 | SOVERSION 4; exact current Hyprland minimum |
| hyprcursor | 0.1.13 | SOVERSION 0 |
| hyprwayland-scanner | 0.4.6 | Build-time code generator, not runtime dependency |
| hyprland-protocols | 0.7.0 | Build-time XML; tagged release is Meson-only |

### Build-only components

`hyprwayland-scanner` generates C++ sources. `hyprland-protocols` supplies XML
consumed by that generator. Neither is loaded or read by the compiled
Hyprland binary at runtime.

They must be separately packaged because downstream projects also consume
them, but Hyprland's runtime RPM must not carry artificial scanner/protocol
requirements.

### Build-system drift

hyprland-protocols migrated from Meson to CMake after version 0.7.0 without a
new tag or version change. Stable 0.7.0 packaging must use Meson; nightly
packaging of the audited default branch would use CMake.

This proves that automated updates must compare build manifests, not only
version strings.

### Plugin ABI

Hyprland installs internal C++ headers and loads plugins in-process.
`hyprland-plugins` records exact compositor/plugin commit pairs.

Plugin RPMs therefore require:

- the exact selected plugin commit;
- the exact Hyprland EVR;
- the same compiler and relevant build flags;
- LTO disabled on both sides;
- a load test before publication.

### New application stack

Recent applications increasingly depend on:

- hyprtoolkit;
- hyprwire;
- aquamarine;
- hyprgraphics.

For example, hyprpaper is no longer a small isolated Wayland client: current
stable releases pull in the native toolkit and IPC stack. Package planning
must follow current manifests rather than historical assumptions.

## Fedora status

Fedora's former Hyprland compositor and application packages are retired.
Several older Hypr libraries remain, but they do not form a compatible set for
Hyprland 0.55.4.

The historical failure was an unreconstructed SONAME transition:
`hyprland-0.45.2` still required `libhyprutils.so.1` after the library package
changed. The compositor failed to install and was eventually retired.

This project's release process is specifically designed to prevent that
failure:

- inspect every SONAME;
- calculate reverse dependencies;
- rebuild the complete closure;
- solve the repository with DNF;
- publish atomically.

RPM Fusion carries no HyprWM packages.

## Fedora 44 feasibility

Most external dependencies required by the stable tagged sources are already
available at sufficient versions in Fedora 44, including:

- Wayland 1.24 and wayland-protocols 1.47;
- libinput 1.31 and libseat 0.9;
- current DRM, Mesa, PipeWire, sdbus-c++, graphics, image, parsing, and Qt
  development packages;
- Qt 6.10.2, which exceeds hyprqt6engine's 6.9 floor;
- ICU, libqalculate, and libpci for newer optional applications.

Each Fedora package and observed version is linked in the
[Fedora 44 dependency matrix](fedora-packaging-design.md#stock-fedora-dependencies-that-meet-the-stable-tagged-requirements).

### Required repository-owned prerequisites

#### glaze-devel

Fedora does not package glaze. Hyprland builds `hyprpm` by default and requests
glaze 7.x; several newer applications also use it and otherwise fetch from the
network.

The repository must package glaze separately and disable all FetchContent
fallbacks.

#### Parallel Lua 5.5

Fedora 44's primary Lua is 5.4.8, while Rawhide has moved to 5.5. Hyprland's
module search can accidentally accept Lua 5.4 because its final alternative
is only an upper-bound expression.

The Fedora 44 repository must provide a parallel `lua5.5` package and assert
that Hyprland selected Lua 5.5.x. It must not replace Fedora's system Lua 5.4.

### Required compatibility proof

Fedora's udis86 package has no pkg-config file, but Hyprland has a direct
library lookup fallback. Fedora's source is also a different fork from
Hyprland's submodule.

The implementation must prove source compatibility in Mock. A silent bundled
fallback is prohibited.

### UWSM

Fedora 44 and Rawhide do not package UWSM. The initial Hyprland package will
disable the optional UWSM session entry rather than install a launcher for a
missing executable. The normal Wayland session remains available.

### Stable versus nightly Wayland requirements

Hyprland 0.55.4 requires wayland-protocols 1.47, which Fedora 44 provides.
Current unreleased `main` later raised the floor to 1.49. That affects nightly
tracking, not the initial stable package.

## Downstream conclusions

No current Fedora spec set is suitable for direct reuse.

Best reusable patterns:

- Debian: unbundling, multi-maintainer team, ABI tooling, and regression tests.
- openSUSE: complete current RPM ecosystem and automated sources.
- Arch: prompt rebuilds when aquamarine and other dependencies change.
- hyprnix: one upstream-owned lock across all ecosystem repositories.
- Gentoo hyproverlay: explicit ABI/subslot rebuild relationships.

Rejected patterns:

- bundling the entire stack into one private prefix;
- publishing from a packager-owned binary/source mirror;
- carrying archived qtutils in a new repository;
- stable builds from moving branches;
- independently publishing packages after only leaf-package testing.

## Selected Fedora package architecture

### Main install behavior

`dnf install hyprland` installs:

- the compositor and required shared libraries;
- recommended portal, wallpaper, idle/lock, night-light, polkit agent,
  backgrounds, and XWayland through weak dependencies.

Users can disable weak dependencies for a minimal compositor. The
`hyprland-desktop` meta package hard-requires the supported desktop baseline.
Because the initial non-UWSM session does not globally enable optional user
services, the package documentation provides explicit activation/configuration
instructions; RPM does not edit user configuration.

### Development packages

Every shared library has a real `-devel` package. `hyprland-devel` owns the
large internal/plugin header surface and `hyprland.pc`; it is not an empty
dependency metapackage.

`hyprpm` is split into its own optional subpackage because using it requires
the exact development package, Git, and a native compiler toolchain. Packaged
official plugins remain the reproducible default.

### Protocol and scanner packages

- `hyprland-protocols-devel` contains architecture-independent build data.
- `hyprwayland-scanner-devel` contains its executable and discovery metadata.
- `hyprwire-scanner-devel` is split from the hyprwire runtime library.

### Archived transitions

Only `hyprland-guiutils` is introduced. Its tagged command targets match the
three qtutils commands and add `hyprland-welcome`, so it uses matching
versioned `Provides` and `Obsoletes` for the final archived package lines.
Archived sources are not maintained as parallel new packages.

## Build and publication decision

- Mock is authoritative.
- SRPMs are the build input.
- GitHub Actions is orchestration only.
- Stable release builds run on trusted ephemeral Fedora runners.
- Pull requests run without signing or publication credentials.
- x86_64 and aarch64 are the initial release architectures.
- each release is built twice for reproducibility comparison;
- `createrepo_c` produces immutable snapshots;
- RPMs and `repomd.xml` are signed separately;
- `current` changes only after complete validation.

## Optimization decision

- Fedora build and hardening flags remain authoritative.
- hard-coded upstream `-O3` is removed.
- `-march=native`, ThinLTO, PGO, alternate linkers, and manual stripping are
  not enabled.
- Fedora LTO remains enabled for ordinary libraries and applications.
- LTO is disabled for Hyprland and plugins because upstream explicitly warns
  that it can break plugins.
- automatic debuginfo and debugsource packages remain enabled.

## Local repository decision

The repository publishes immutable Fedora-release and architecture-specific
snapshots with:

- package metadata;
- source and binary RPMs;
- source/build manifests;
- package and repository signatures;
- a noarch release/bootstrap RPM;
- an offline bundle;
- retained prior snapshots.

Rollback combines a retained repository snapshot with DNF5 history
rollback/replay. DNF history alone is insufficient if old RPMs are no longer
available.

## Implementation gates

Implementation starts only after review accepts:

1. the supported package tiers;
2. separate glaze and Lua 5.5 prerequisite packages;
3. UWSM disabled for Fedora 44;
4. the udis86 compatibility decision after a proof build;
5. the weak-dependency contents of `dnf install hyprland`;
6. exact plugin EVR coupling;
7. x86_64 and aarch64 as initial architectures;
8. the no-file-capability default for Hyprland;
9. the immutable signed repository model;
10. the stable 0.55.4 compatibility lock.

The next phase is review and refinement of these decisions. RPM implementation
follows only after that gate.
