# HyprWM Fedora Packaging

Production-oriented Fedora packaging for Hyprland and the wider HyprWM
ecosystem.

Repository-authored tooling and packaging metadata are licensed under MIT.
Upstream source packages retain their own licenses as recorded by each spec.

## Project status

Phase 1 investigation and design are complete. Phase 2 contains the native
Fedora implementation for the locked Fedora 44 stable set:

- 29 separately buildable source packages;
- Mock-based dependency-ordered builds for x86_64 and aarch64;
- source provenance and checksum validation;
- a resumable local development workflow and clean release rebuild workflow;
- immutable, optionally signed DNF snapshots and offline bundles;
- pull-request, nightly, and protected release GitHub Actions;
- official-upstream update detection and changelog generation;
- minimal, desktop, complete, and exact-plugin-ABI package sets.

Only official upstream archives and official Fedora sources are accepted.
COPR, AUR, personal mirrors, `/usr/local` payloads, and build-time network
fallbacks are prohibited.

## Local build

On Fedora 44, install the tools listed in [CONTRIBUTING.md](CONTRIBUTING.md)
and ensure the build user belongs to the `mock` group.

```bash
make validate
make test-tooling
make build-set
make audit
make repo
```

During interrupted local development, `make resume-set` reuses RPMs whose
source-package version and release still match the lock manifest. Trusted
release jobs always use `make build-set` for a clean rebuild.

The working repository is `.work/repository`. A complete local installation
test is:

```bash
ci/install-test.sh mock/fedora-44-x86_64.cfg .work/repository
```

Immutable publication uses:

```bash
make snapshot
```

Publication requires complete native x86_64 and aarch64 result trees matching
the manifest. A single-architecture development repository is intentionally
not activatable as a release snapshot. After validating the inactive
candidate, run `make activate PUBLIC_KEY=<trusted-keyring>`. Unsigned local
snapshots require the explicitly named `make activate-unsigned` target.

Retained signed snapshots can be restored with
`make rollback REVISION=<revision> PUBLIC_KEY=<trusted-keyring>`, which
verifies package, metadata, and manifest signatures before changing `current`.

Unsigned local snapshots are supported. Public snapshots require an
operator-provided RPM signing key and public key; private keys are never stored
in this repository.

## Documentation

- [Documentation index](docs/README.md)
- [Phase 1 investigation report](docs/phase-1-report.md)
- [Upstream repository inventory](docs/upstream-inventory.md)
- [Dependency graph and build order](docs/dependency-graph.md)
- [Downstream packaging survey](docs/downstream-packaging-survey.md)
- [Fedora packaging design](docs/fedora-packaging-design.md)
- [Build, CI, and release design](docs/build-release-design.md)
- [Local DNF repository design](docs/local-repository-design.md)
- [Compiler and optimization policy](docs/build-optimization.md)
- [Risk assessment](docs/risk-assessment.md)
- [Primary source index](docs/source-index.md)

## Current evidence baseline

The upstream inventory and version checks were performed on 2026-07-15.
Release versions are taken from Git refs, not only from upstream `VERSION`
files. This distinction matters because Hyprland patch tags such as
`v0.55.4` retain `VERSION=0.55.0`, and several other repositories have tagged
releases that do not correspond one-for-one with `VERSION`-file commits.

The stable core baseline under investigation is:

| Project | Version |
|---|---:|
| Hyprland | 0.55.4 |
| aquamarine | 0.12.1 |
| hyprutils | 0.13.1 |
| hyprlang | 0.6.8 |
| hyprgraphics | 0.5.1 |
| hyprcursor | 0.1.13 |
| hyprwayland-scanner | 0.4.6 |
| hyprland-protocols | 0.7.0 |

The release lock is machine-readable in
[`manifests/release-set.json`](manifests/release-set.json).
