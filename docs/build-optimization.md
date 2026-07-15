# Compiler and optimization policy

## Objective

Produce Fedora-native binaries that are reproducible, debuggable, hardened,
and portable across each supported Fedora architecture.

Performance changes are accepted only when they preserve those properties and
are justified by measurements representative of compositor workloads.

## Fedora 44 baseline

Fedora's `redhat-rpm-config` supplies the distribution build flags through the
RPM macros used by `%cmake`, `%meson`, and `%set_build_flags`.

Primary reference:
[Fedora 44 buildflags.md](https://src.fedoraproject.org/rpms/redhat-rpm-config/raw/f44/f/buildflags.md).

The baseline includes:

- `-O2`
- debug information
- format-security checks
- `_FORTIFY_SOURCE=3`
- stack protector and stack-clash protection
- PIE and hardened linker flags
- architecture-appropriate control-flow protection
- annobin metadata
- frame-pointer policy from Fedora's RPM configuration
- LTO by default
- automatic build IDs, debuginfo, and debugsource extraction

These flags are the default. Upstream flags do not replace them without a
documented package-specific reason.

## Build type

### Decision

Use CMake `RelWithDebInfo` and the normal Fedora `%cmake` macro for release
packages. Use the corresponding Fedora `%meson` release/debug-optimized
configuration for Meson projects.

Why:

- `Debug` changes Hyprland behavior by adding profiling/no-PIE/no-builtin
  flags and is not a production configuration.
- plain upstream `Release` often adds its own optimization and removes useful
  debug assumptions.
- Fedora already controls optimization and debug information through RPM
  flags.
- `RelWithDebInfo` expresses the desired upstream semantic while Fedora's
  build flags remain authoritative.

### Upstream `-O3`

The core CMake projects add `-O3` in non-Debug builds. That trailing flag can
override Fedora's `-O2` and makes package behavior depend on upstream flag
ordering.

Policy:

1. Patch hard-coded optimization flags out of tagged release sources.
2. Submit equivalent changes upstream where practical.
3. Preserve the rest of the upstream warning and language-standard flags.
4. Verify the final compiler invocation in `compile_commands.json`.

Using `Debug` merely to avoid `-O3` is rejected because it also enables
unwanted debug-only behavior.

## Optimization decisions

| Optimization | Decision | Rationale |
|---|---|---|
| Fedora `-O2` | Enable | Distribution default, broadly tested, portable |
| Upstream hard-coded `-O3` | Remove | Overrides Fedora policy without project-specific benchmark evidence |
| `-Ofast` | Never enable | Relaxes language and floating-point semantics |
| `-march=native` | Never enable | Produces host-specific RPMs that may fail on other Fedora systems |
| `-mtune=native` | Never enable | Harms reproducibility and portability |
| Fedora architecture baseline | Enable | Correct place to select architecture support |
| x86_64-v3 | Do not force on Fedora 44 | Not the Fedora 44 baseline; future Fedora support should follow distribution policy |
| PGO | Do not enable initially | No representative, reproducible compositor training workload exists |
| ThinLTO | Do not introduce | Not a Fedora default and offers no demonstrated project benefit |
| Manual stripping | Do not use | Breaks Fedora debuginfo/debugsource generation |
| Alternate linker such as mold | Do not force | Nix prior art is not sufficient to override Fedora's supported linker baseline |

## LTO

### Hyprland and plugins

Hyprland's own
[CMakeLists.txt](https://github.com/hyprwm/Hyprland/blob/v0.55.4/CMakeLists.txt)
adds `-fno-lto` with the explicit comment that LTO may break plugins.

Policy:

- Disable Fedora LTO in the `hyprland` source package with
  `%global _lto_cflags %{nil}`.
- Disable LTO in `hyprland-plugins` as well.
- Keep upstream `-fno-lto`.
- Verify compile and link commands; do not rely only on assumed flag order.
- Treat accidental `-flto` in either package as a CI failure.

The RPM macro is used even though upstream adds `-fno-lto` because it removes
ambiguity from compiler and post-processing behavior and documents the
package-level exception.

### Independent shared libraries and applications

Keep Fedora's default LTO for hyprutils, hyprlang, hyprgraphics, hyprcursor,
aquamarine, hyprwire, hyprtoolkit, and ordinary applications unless a
reproducible test demonstrates a defect.

LTO policy is source-package-local. Hyprland's directory-scoped
`add_compile_options(-fno-lto)` does not affect separately built libraries.

## C++ standard and compiler policy

Hyprland, hyprutils, and hyprgraphics request C++26. Other current libraries
request C++23.

Policy:

- Build with Fedora's default GCC first.
- Add Clang as a scheduled compatibility build, not as the release compiler.
- Never add `-fpermissive` to hide source errors.
- Carry a narrowly scoped upstream/backport patch if Fedora's compiler exposes
  a confirmed source issue.
- Record the exact GCC, binutils, CMake, and standard-library NVR in release
  metadata.
- Add a Rawhide build before adding support for the next Fedora release.

The implementation phase must run an actual Fedora 44 Mock build. Compiler
flag support alone is not proof that every C++26 construct used by the source
is implemented correctly.

## Hardening

Keep Fedora's hardening flags unless upstream functionality makes a specific
flag impossible.

- PIE remains enabled for executables.
- Stack and control-flow protection remain enabled.
- Fortification remains enabled.
- No executable stack or text relocation is accepted.
- Linker undefined-symbol checks should be enabled where compatible.
- Security exceptions must be package-specific, documented, and tested.

Hyprland's Debug-only no-PIE flags are another reason not to use Debug builds
for release RPMs.

## Debug information

Keep Fedora's automatically generated `-debuginfo` and `-debugsource`
packages.

This is especially important for a compositor:

- crashes end the graphical session;
- stack traces need matching debug symbols across the Hypr library stack;
- plugin crashes otherwise look like compositor crashes;
- upstream frequently asks for detailed crash information.

Do not strip binaries manually and do not disable debug packages to reduce
repository size. Repository retention policy handles storage pressure.

## Reproducibility

Hyprland derives build metadata from Git and falls back to `unknown` when a
release archive lacks `.git`.

The spec must inject deterministic values for:

- commit hash
- tag
- branch label
- commit date
- dirty state
- commit count

Values come from the locked source manifest, not the build host.

Additional requirements:

- use source archive checksums;
- set a stable source date epoch from the upstream tag commit;
- preserve Fedora path-remapping flags;
- prevent network access and FetchContent fallback;
- start every architecture build from a clean source tree because protocol
  and shader generation writes into the source directory;
- compare two independent release builds before publication.

## Feature determinism

hyprgraphics silently includes JPEG XL and HEIF/AVIF support when their
development packages are present.

Policy:

- Declare the complete intended feature set as `BuildRequires`.
- Fail configuration if an expected feature is absent.
- Record enabled codecs in build logs and package metadata.
- Do not let incidental Mock buildroot contents change the exported library.

The same principle applies to XWayland, systemd, UWSM, portal services, and
all optional CMake features.

## PGO reconsideration criteria

PGO may be reconsidered only after all of the following exist:

1. A deterministic workload covering frame scheduling, rendering, input,
   window management, IPC, and XWayland.
2. Native training on every published architecture.
3. A measured improvement that exceeds noise on representative hardware.
4. Reproducible profile collection and retention.
5. No regression in startup, latency, debug quality, or build time.

Until then, PGO adds maintenance and hardware bias without a defensible gain.
