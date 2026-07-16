# HyprWM Fedora packaging instructions

This repository packages a locked HyprWM ecosystem for Fedora 44. It is not the
Hyprland upstream source tree. Fedora RPM specs, the release manifest, and the
repository tooling are the product.

## Development environment and commands

Use Fedora 44 with the packages listed in `CONTRIBUTING.md`; Mock builds require
membership in the `mock` group. `ci/install-build-dependencies.sh` installs the
CI build tool set when run with sufficient DNF privileges.

### Validation and tests

```bash
# Validate the JSON schema, manifest/spec synchronization, source policy,
# package-local inputs, exact-EVR coupling, and dependency graph.
make validate

# Run all Python packaging-tool regression tests.
make test-tooling

# Run one regression test.
python3 -m unittest \
  tooling.test_hyprwm_packaging.PackagingToolTests.test_repository_manifest_is_valid

# Check local Markdown links.
make check-docs

# CI-equivalent syntax/static checks.
python3 -m py_compile tooling/hyprwm-packaging
find packages -name '*.spec' -print0 | sort -z | \
  xargs -0 -n1 rpmspec -P >/dev/null
git diff --check
```

Add tooling regressions to `tooling/test_hyprwm_packaging.py`. The tests load the
extensionless `tooling/hyprwm-packaging` script with `runpy`, so test functions
through the returned `MODULE` dictionary.

### Builds and package QA

Mock is the authoritative builder; host `rpmbuild` is only useful for quick
iteration.

```bash
# Source/SRPM/single-package operations.
make fetch PACKAGE=hyprutils
make srpm PACKAGE=hyprutils
make build PACKAGE=hyprutils

# Clean full graph build; override MOCK_CONFIG for aarch64.
make build-set
make build-set MOCK_CONFIG=mock/fedora-44-aarch64.cfg

# Preview and build the full affected closure for a package.
python3 tooling/hyprwm-packaging affected hyprutils
python3 tooling/hyprwm-packaging build-set hyprutils \
  --mock-config mock/fedora-44-x86_64.cfg --repo .work/repository

# Reuse only matching local artifacts after an interrupted development build.
make resume-set

# QA requiring built RPMs, then installation tests against the generated repo.
make audit
ci/install-test.sh mock/fedora-44-x86_64.cfg .work/repository
```

`make build PACKAGE=...` does not build prerequisites; they must already be in
the repository. Prefer the affected-closure command for dependency or ABI
changes. Never use `resume-set` for a release build. The Mock configurations
disable build networking and cap RPM parallelism at four because Hyprland's
C++/PCH build is memory-bound.

### Repository and release operations

```bash
make repo
make snapshot
make activate PUBLIC_KEY=/path/to/trusted-keyring
make activate-unsigned
make rollback REVISION=YYYY.MM.DD-N PUBLIC_KEY=/path/to/trusted-keyring
make bundle
make check-updates
```

`make audit`, `make repo`, snapshots, and installation tests consume current
artifacts under `results/<mock-config>/<source>/{srpm,rpm}`.

## Architecture

- `manifests/release-set.json` is the release lock. It records every source
  package's path, RPM version/release, build graph edges, update policy, and
  immutable source URL/checksum/provenance. The adjacent JSON Schema defines
  its shape; `validate_manifest()` adds repository-specific semantic checks.
- `tooling/hyprwm-packaging` is the implementation. The Makefile is a thin
  stable interface over its commands for source fetching, SRPM/Mock builds,
  graph selection, auditing, updates, repository generation, signing,
  activation, rollback, and offline bundles.
- Each `packages/<source>/` directory owns one source RPM: a same-named spec,
  rationale in `README.md`, and optional `patches/` and `files/`. Remote inputs
  are cached in `.cache/sources/`; the tool assembles a clean
  `.work/sources/<source>/` tree before invoking Mock.
- `build_after` edges and `tier` values form the build order. A set build adds
  each completed package to `.work/repository`, regenerates DNF metadata, then
  builds consumers against that repository. `affected` includes changed
  packages, all reverse dependencies, and all prerequisites needed to build
  that closure.
- `repo/comps/hyprwm.xml` defines the supported `hyprland-desktop` and
  `hyprwm-complete` groups. The latter is the maximal ready-to-use environment,
  including concrete Fedora desktop utilities and official plugins.
  `repo/config/hyprwm-fedora.repo.in` is rendered with signed or explicitly
  unsigned policy.
- Development repositories are mutable. Publication creates a complete,
  read-only snapshot for both native `x86_64` and `aarch64` under
  `repo/public/fedora/44/releases/<revision>/`; activation verifies it and
  atomically swaps the `current` symlink. Snapshots are immutable and may not
  reuse a revision.
- GitHub workflows are thin orchestration around repository commands. PR CI
  validates, builds, audits, and install-tests unsigned x86_64 artifacts.
  Protected releases verify a signed tag, build both architectures natively,
  sign and verify the complete snapshot, and activate only as the final step.

## Packaging and update conventions

- Keep manifest and spec `Version`/integer `Release` synchronized. Reset
  `Release` to `1` for a new upstream version; increment it for packaging-only
  changes and ABI-triggered rebuilds. Add the corresponding committed
  `%changelog` entry.
- Treat an update as a release-set transaction, not an isolated URL change.
  Review dependency minima, SONAMEs, installed files, patch applicability, and
  rebuild the affected closure. `prepare-update` is a proposal helper; dry-run
  it before `--apply`.
- Hyprland updates are always manual and atomic with the exact
  `hyprland-plugins` commit selected by upstream `hyprpm.toml`. Update
  Hyprland/plugin exact EVRs and the exact requirements in `hyprwm-meta`
  together. `make validate` deliberately rejects drift in these couplings.
- Record every remote input in the manifest using an immutable HTTPS URL,
  SHA-256, provenance, and human-readable reference. Only the package's
  official upstream or official Fedora infrastructure is accepted. Do not
  commit downloaded archives.
- Specs must not fetch during `%prep`, `%build`, `%install`, or `%check`; remove
  bundled/FetchContent fallbacks and declare packaged dependencies instead.
  Never add COPR/AUR/personal-mirror inputs or install payloads under
  `/usr/local`.
- Put downstream patches only in `packages/<source>/patches/` and auxiliary
  sources only in `files/`. Every local file must be referenced by the spec,
  and every referenced local file must exist. Document package-specific patch,
  test-boundary, split-package, or rpmlint rationale in that package's
  `README.md`; keep rpmlint filters narrow and justified.
- Prefer Fedora virtual build dependencies such as `pkgconfig(...)` and
  `cmake(...)`. Declare every direct tagged build dependency because upstream
  metadata may omit transitive requirements. Do not add runtime requirements
  for build-only protocol XML or scanner tools. A `-devel` package requires its
  matching runtime library at exact EVR.
- Preserve Fedora macros, hardening, debug information, and build flags. Patch
  out upstream hard-coded optimization; never introduce `-march=native`,
  manual stripping, or build-host-derived release metadata. LTO stays enabled
  normally but is explicitly disabled for both `hyprland` and
  `hyprland-plugins` because of their in-process plugin ABI.
- `%check` must run inside a headless, network-disabled Mock buildroot.
  Graphical compositor, portal, PAM, and Qt interaction checks belong on the
  hardware-capable release runners; package specs should still exercise every
  meaningful headless path available.
- Generated `.cache/`, `.work/`, `results/`, and `repo/public/` content is
  ignored and must not be edited or committed. Never place private signing keys
  in the repository.
- Keep GitHub Actions pinned to full commit SHAs. Pull-request workflows must
  remain credential-free and must not run untrusted package builds on
  long-lived release runners.
