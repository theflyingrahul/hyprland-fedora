# Downstream packaging survey

Audit date: **2026-07-15**

## Summary

No current Fedora 44 spec set can be copied unchanged to produce a supported
HyprWM stack.

- Fedora's compositor and application packages were retired after dependency
  SONAME changes were not followed by coordinated rebuilds.
- Fedora still carries several older Hypr libraries, but their versions are
  not a coherent set for Hyprland 0.55.4.
- RPM Fusion does not package Hyprland.
- Current openSUSE, Arch, Nix, Gentoo-overlay, and Debian packaging provides
  strong prior art.
- Debian has the strongest unbundling and regression-testing approach.
- openSUSE has the most complete current RPM ecosystem.
- `hyprwm/hyprnix` provides the best upstream-owned model for maintaining a
  coherent multi-repository version lock.

The design in this repository reuses those patterns, but not distribution-
specific macros or downstream changes without independent justification.

## Fedora

### Current official package state

The official application layer is retired. The following table points to the
last live spec or current `dead.package`.

| Source package | Last live Fedora package | Current state | Evidence |
|---|---:|---|---|
| hyprland | 0.45.2, Fedora 42 | Retired after a fails-to-install event | [last spec](https://src.fedoraproject.org/rpms/hyprland/raw/ae2f9c98ecbb4f9b4177a48438cf586f352d94e7/f/hyprland.spec), [dead.package](https://src.fedoraproject.org/rpms/hyprland/raw/e4974798107d72a89e3c3f828d5133bdd1a874a0/f/dead.package) |
| hypridle | 0.1.2, Fedora 41 | Retired after orphaning | [last spec](https://src.fedoraproject.org/rpms/hypridle/raw/93935734546569ad8708a195e2bab8cd5e739167/f/hypridle.spec) |
| hyprlock | 0.4.1, Fedora 41 | Retired after orphaning | [dist-git](https://src.fedoraproject.org/rpms/hyprlock) |
| hyprpaper | 0.7.1, Fedora 41 | Retired after orphaning | [dist-git](https://src.fedoraproject.org/rpms/hyprpaper) |
| hyprpicker | 0.4.1, Fedora 41 | Retired after orphaning | [dist-git](https://src.fedoraproject.org/rpms/hyprpicker) |
| xdg-desktop-portal-hyprland | 1.3.6, Fedora 43 | Fedora 44 branch was created and then retired for failure to install | [last spec commit](https://src.fedoraproject.org/rpms/xdg-desktop-portal-hyprland/tree/bc97212b64287625c8475141dbdc0f5361beec95), [dist-git](https://src.fedoraproject.org/rpms/xdg-desktop-portal-hyprland) |
| aquamarine | 0.8.0, Fedora 43 | Retired after orphaning | [last spec commit](https://src.fedoraproject.org/rpms/aquamarine/tree/27be27b6cfda124b268455920dfeedc4a0748702) |
| nwg-dock-hyprland | 0.4.0, Fedora 43 | Retired after orphaning | [last spec commit](https://src.fedoraproject.org/rpms/nwg-dock-hyprland/tree/405479d862ec48b74fbb1774d2f07df829b79bce) |

Several library packages remain in Fedora 44/Rawhide, but they are older than
the selected upstream release set:

| Package | Fedora version observed | Upstream stable | Compatibility consequence |
|---|---:|---:|---|
| [hyprutils](https://packages.fedoraproject.org/pkgs/hyprutils/hyprutils/fedora-44.html) | 0.7.1 | 0.13.1 | Does not meet Hyprland 0.55.4 minimum 0.13.1 |
| [hyprcursor](https://packages.fedoraproject.org/pkgs/hyprcursor/hyprcursor/fedora-44.html) | 0.1.11 | 0.1.13 | Meets Hyprland's old minimum but is not the selected release |
| [hyprwayland-scanner-devel](https://packages.fedoraproject.org/pkgs/hyprwayland-scanner/hyprwayland-scanner-devel/fedora-44.html) | 0.4.2 | 0.4.6 | Meets Hyprland's minimum; older than other consumers' preferred version |
| [hyprland-protocols-devel](https://packages.fedoraproject.org/pkgs/hyprland-protocols/hyprland-protocols-devel/fedora-44.html) | 0.4.0 | 0.7.0 | Does not meet Hyprland 0.55.4 minimum 0.6.4 |
| [hyprlang](https://packages.fedoraproject.org/pkgs/hyprlang/hyprlang/fedora-44.html) | 0.6.4 | 0.6.8 | Does not meet Hyprland 0.55.4 minimum 0.6.7 |
| [hyprgraphics](https://packages.fedoraproject.org/pkgs/hyprgraphics/hyprgraphics/fedora-44.html) | 0.1.5 | 0.5.1 | Does not meet Hyprland 0.55.4 minimum 0.5.1 |

This repository must therefore publish the core stack as one coordinated set.
Depending on a mixture of Fedora's older libraries and this repository's
newer applications would repeat the failure mode that caused retirement.

### Retirement root cause

The decisive failure was not that Hyprland was intrinsically unpackageable.
The compositor package was left linked against
`libhyprutils.so.1` after Fedora's hyprutils package moved to a different
SONAME. The reverse dependency was not rebuilt, Fedora's fails-to-install
policy elapsed, and the package was retired.

This establishes a non-negotiable design requirement:

> Every Hypr library update must calculate and rebuild its complete reverse
> dependency set before new repository metadata is published.

### Useful conventions from the retired Fedora specs

The old Fedora specs remain useful for naming and integration conventions:

- Fedora-native `%cmake`, `%meson`, pkg-config dependency expressions, and
  `%autorelease`.
- `hyprlock` marked `/etc/pam.d/hyprlock` as `%config(noreplace)`.
- `hyprpicker` used `Recommends: wl-clipboard`.
- `xdg-desktop-portal-hyprland` required the base portal and used weak
  relationship metadata for Hyprland.
- The portal carried one Fedora-version-gated compatibility patch.

They are not a sufficient implementation base:

- Hyprland 0.45.2 used an older build system and dependency graph.
- The `hyprland-devel` subpackage was effectively an empty dependency
  metapackage rather than owning the installed plugin headers and
  `hyprland.pc`.
- There was no compiler-version gate or ecosystem rebuild automation.
- Hyprland explicitly declared a bundled udis86 fork.
- No package encoded exact plugin ABI coupling.

### udis86

Fedora 44 still carries `udis86`:

- Fedora NVR observed: `1.7.2-30.56ff6c8`.
- It installs a shared library, `udcli`, headers, and the unversioned
  development symlink.
- It does not install `udis86.pc` or provide `pkgconfig(udis86)`.
- The current spec carries four build-portability patches.

Source: [Fedora udis86 spec](https://src.fedoraproject.org/rpms/udis86/raw/rawhide/f/udis86.spec).

Hyprland first checks pkg-config, then performs a direct library lookup, then
falls back to its submodule. The absence of a `.pc` file is therefore not
automatically fatal. The more important question is source compatibility:
Hyprland's submodule is a different maintained fork from Fedora's package.
The implementation phase must prove that Fedora's system library builds and
passes tests before the bundled fallback is disabled. If it does not, a
parallel, explicitly named fork package or a reviewed bundling exception is
required; silently using the submodule is not acceptable.

## RPM Fusion

No Hyprland or HyprWM package was found in RPM Fusion free or nonfree. RPM
Fusion is therefore neither a dependency nor a source of reusable packaging
for this project.

## COPR packaging references

COPR projects are references only. Users of this repository must not need a
COPR enabled.

### solopasha/hyprlandRPM

[solopasha/hyprlandRPM](https://github.com/solopasha/hyprlandRPM) uses
separate RPMs for the Hypr projects and mostly system dependencies. It has
useful compatibility handling and snapshot-version examples, but its main
Hyprland build was behind the current stable release during the audit.

Concerns:

- Complex RPM Lua metaprogramming makes review and maintenance harder.
- Selected dependencies and protocol sources are still vendored.
- System-library use leaves it exposed to the same unsynchronized SONAME
  changes as the retired Fedora package unless all packages are rebuilt
  together.

### sdegler/hyprland

The sdegler COPR identifies itself as a clone of solopasha's work updated to
newer versions. It is useful evidence of maintainer succession and lag, not an
independent packaging architecture.

### AshBuk/Hyprland-Fedora

[AshBuk/Hyprland-Fedora](https://github.com/AshBuk/Hyprland-Fedora) packages a
current 0.55.4 stack by building many Hypr libraries, Lua, glaze, and udis86
inside one SRPM and installing them below a private
`/usr/libexec/hyprland/vendor` prefix with RPATH isolation.

That architecture is technically effective at preventing ABI collisions, but
it is not the architecture selected here:

- It bundles projects that should be independent Fedora packages.
- It suppresses automatic dependency generation for vendored libraries.
- Multiple upstream projects are built by one spec.
- Some source assets are republished from the packager's own GitHub Releases
  rather than fetched directly from their upstream provenance.

The reusable idea is the coherent version table. This project implements that
idea as a repository-wide lock manifest and separate source packages, not as a
private bundled prefix.

## openSUSE

openSUSE's `X11:Wayland` project is the most complete current RPM reference.
Its [Hyprland spec](https://api.opensuse.org/public/source/X11:Wayland/hyprland/hyprland.spec?rev=157)
packaged 0.55.4 and produced:

- `hyprland`
- `hyprland-wallpapers`
- `hyprland-devel`
- separate Bash, Fish, and Zsh completion packages

Its OBS `_service` file pulls Git sources and submodules, creates a tarball,
recompresses it, and sets the version automatically. The project also
packages most current libraries and applications.

Useful patterns:

- Full-ecosystem ownership by one packaging project.
- Automated source-service updates.
- Separate development and large data outputs.
- Explicit handling of git-derived build metadata.
- A pattern/meta package for a usable Hyprland desktop.

Downstream changes not adopted automatically:

- `disable-donation-nag-popup.patch` changes upstream product behavior.
- `start_hyprland_no_nixgl.patch` is openSUSE-specific.
- Archived `hyprland-qtutils` is kept building with a Qt 6.10 patch; this
  project instead follows the upstream replacement.
- OBS macros and source services do not map directly to Fedora/Koji.

## Arch Linux

Arch `[extra]` packaged Hyprland 0.55.4 and current major companions at the
audit date. The version bump is pinned in
[Arch packaging commit cdfe2c30](https://gitlab.archlinux.org/archlinux/packaging/packages/hyprland/-/commit/cdfe2c3062da1745b0aaa59874663088b0d4b7c4).

Useful patterns:

- Release tarballs and explicit package dependency lists.
- SONAME-aware dependency comments and rebuilds.
- A recorded rebuild specifically for aquamarine 0.12.0:
  [commit c4c42cc8](https://gitlab.archlinux.org/archlinux/packaging/packages/hyprland/-/commit/c4c42cc84192cd7e0459a3a9bbd4a38a6feab129).
- `provides=(wayland-compositor)` for the compositor.

Patterns not adopted:

- `xdg-desktop-portal-hyprland` vendors a pinned protocol commit rather than
  depending on a separately versioned protocol package.
- Arch's patched archived qtutils package is historical compatibility work,
  not a reason to introduce that package in a new Fedora repository.

## Nix and upstream hyprnix

Nixpkgs packaged Hyprland 0.55.4 with separate output, manual, and development
outputs. Its expression injects deterministic Git version information rather
than letting a source archive produce `unknown` metadata.

The most important reference is upstream
[hyprnix](https://github.com/hyprwm/hyprnix):

- It pins ecosystem repositories together.
- Shared inputs use `follows` relationships to avoid duplicate or skewed
  dependency instances.
- A dedicated `update.py` updates one component or the complete set.
- Tags are deliberately locked; a generic flake update is not trusted to
  maintain compatibility.

This repository adopts the same coherent-set principle in an RPM-oriented
manifest. It does not adopt Nix-specific toolchain choices such as GCC 15 or
the mold linker without Fedora-specific evidence.

## Gentoo

Hyprland was formerly in the official Gentoo tree through 0.51.1. Gentoo
last-rited the suite in
[commit 1d4db2ff](https://github.com/gentoo/gentoo/commit/1d4db2ff53c5461db0c8aa1a93f4707593c8a4f3)
because the ecosystem's release velocity and proxy-maintainer workload were
not sustainable. Removal completed in March 2026, and users were directed to
the dedicated `hyproverlay`.

The overlay provides two valuable mechanisms:

- The Hyprland slot/subslot is tied to the upstream release.
- `:=` dependencies force reverse rebuilds when a library ABI changes.

It also enforces minimum compiler versions and grants `cap_sys_nice` to the
compositor. Fedora does not have Gentoo slot operators, so this project
reproduces the effect through SONAME inspection, exact build-set manifests,
automatic reverse-dependency rebuilds, and atomic repository publication.

## Void Linux

Void does not carry Hyprland. Multiple package requests were closed as not
planned:

- [#37544](https://github.com/void-linux/void-packages/issues/37544)
- [#44731](https://github.com/void-linux/void-packages/issues/44731)
- [#50824](https://github.com/void-linux/void-packages/issues/50824)
- [#51414](https://github.com/void-linux/void-packages/issues/51414)
- [#51610](https://github.com/void-linux/void-packages/issues/51610)

There is no reusable official Void template. Third-party templates are not
treated as authoritative packaging evidence.

## Debian and Ubuntu

Debian provides the strongest current policy-oriented packaging reference:

- Hyprland 0.55.4+ds-2 in sid/forky.
- A dedicated multi-maintainer team.
- `hyprland`, `hyprland-backgrounds`, and `hyprland-dev` binary packages.
- Separate source packages for protocols, guiutils, plugins, portal, and Qt
  support.
- A `+ds` repack that removes embedded udis86, hyprland-protocols, and Tracy.
- A custom ABI-version extractor and autopkgtests for pkg-config/dependency
  regressions.
- Updates commonly landed within days of upstream releases.
- `cap_sys_nice` is granted to the compositor.

Primary sources:

- [Debian control](https://sources.debian.org/data/main/h/hyprland/0.55.4+ds-2/debian/control)
- [Debian source-repack rationale](https://sources.debian.org/src/hyprland/0.55.4+ds-2/debian/README.source/)
- [Debian changelog](https://sources.debian.org/src/hyprland/0.55.4+ds-2/debian/changelog/)

Debian's unbundling, team ownership, ABI checks, and test discipline are
selected as design inputs.

Ubuntu follows Debian but demonstrates why an explicit update policy is
needed: Ubuntu 26.04 carried 0.53.3 while 25.10 still exposed 0.41.2 during the
audit. Distribution sync alone does not guarantee a current coherent stack.

## Comparison

| Distribution/channel | Current stable compositor | Packaging model | Main lesson |
|---|---:|---|---|
| Fedora official | Retired; last 0.45.2 | Separate packages, uncoordinated ownership | Reverse rebuild automation is mandatory |
| RPM Fusion | Absent | - | Not a dependency source |
| COPR | Varies | Separate or heavily bundled | Useful experiments, not a production dependency |
| openSUSE | 0.55.4 | Complete RPM ecosystem and OBS automation | Best current RPM reference |
| Arch | 0.55.4 | Simple per-project packages | Rebuild immediately on dependency bumps |
| Nixpkgs/hyprnix | 0.55.4 | Locked dependency graph | Maintain one coherent release set |
| Gentoo hyproverlay | Current/live | Slots and subslot rebuilds | Encode ABI rebuild relationships |
| Void | Absent | Not planned | No official prior art |
| Debian | 0.55.4+ds | Unbundled team-maintained source packages | Best policy, ABI, and regression-test reference |
| Ubuntu | Distribution-dependent lag | Debian synchronization | Do not rely on passive syncing |

## Reusable decisions

1. Build each upstream project as its own source package.
2. Maintain one machine-readable ecosystem release lock.
3. Build and publish reverse dependencies with every SONAME change.
4. Inject deterministic Git metadata into Hyprland builds.
5. Keep protocol XML and code generators as separate build dependencies.
6. Split shared-library development files from runtime libraries.
7. Split large architecture-independent backgrounds from the compositor.
8. Keep plugin packages exact-version coupled to Hyprland.
9. Use a multi-maintainer review model and automated update PRs.
10. Publish a repository snapshot only after the entire dependency graph
    succeeds.

## Rejected patterns

- Bundling the complete Hypr stack into one RPM.
- Pulling sources from a packager-controlled binary mirror.
- Building from moving branches for stable releases.
- Treating `VERSION` files as authoritative release discovery.
- Carrying archived qtutils as a new compatibility burden.
- Publishing a successful subset of a failed ecosystem rebuild.
- Depending on COPR, RPM Fusion, or manual files under `/usr/local`.

## Survey conclusion

There is no single current Fedora spec to reuse wholesale. The implementation
should start from:

- Fedora macros, naming, filesystem, and scriptlet conventions;
- Debian's unbundling and ABI/regression checks;
- openSUSE's complete package coverage and automation;
- Arch's prompt reverse rebuilds; and
- hyprnix's coherent release lock.

That combination addresses the exact maintenance failure that removed
Hyprland from Fedora while retaining native, separately upgradable RPMs.
