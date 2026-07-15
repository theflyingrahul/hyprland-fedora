# Implementation and maintenance guide

## Authoritative state

`manifests/release-set.json` is the release lock. For every source package it
records:

- the package directory;
- RPM version and release;
- dependency-order edges;
- immutable source filenames and HTTPS URLs;
- SHA-256 checksums;
- official-upstream or official-Fedora provenance.

`make validate` rejects missing specs, version/release drift, invalid source
metadata, forbidden source hosts, unknown dependency edges, and graph cycles.
Remote content is never accepted merely because a URL succeeds: its checksum
must match the committed lock.

Validation executes the committed JSON Schema and an explicit upstream
allowlist: HyprWM packages must come from their matching `hyprwm` repository,
Glaze from `stephenberry/glaze`, Lua from `lua.org`, and Fedora-derived inputs
from Fedora infrastructure.

Packages without remote source archives, such as meta and local repository
configuration packages, use an empty `sources` array. Their local inputs live
under `packages/<source>/files/`.

## Package layout

Each source package owns:

```text
packages/<source>/
  <source>.spec
  README.md
  patches/
  files/
```

Only files below `patches/` and `files/` are copied into the SRPM source
directory. Remote archives remain in the ignored `.cache/sources/` cache and
are linked into a clean `.work/sources/<source>/` directory for each SRPM
build.

Downstream patches must state why Fedora needs the change. The common accepted
reasons are:

- removing hard-coded optimization so Fedora flags remain authoritative;
- making packaged dependencies mandatory instead of using FetchContent or a
  bundled subproject;
- fixing installed pkg-config metadata;
- injecting immutable release metadata when a release archive has no Git
  checkout.

Feature-changing patches require stronger justification and upstream review.

## Build commands

The authoritative builder is Mock.

```bash
make validate
make fetch PACKAGE=hyprutils
make srpm PACKAGE=hyprutils
make build PACKAGE=hyprutils
make build-set
```

`make build-set` starts from the lock graph, builds every source package in
topological order, and adds each successful result to `.work/repository`
before building its consumers.

For crash recovery during local development:

```bash
make resume-set
```

The resumable mode reconstructs the temporary repository from RPMs whose
source name, version, and release still match the manifest, then builds only
missing entries. It is not a release substitute. CI release jobs always
perform clean builds.

The Fedora 44 x86_64 Mock configuration caps RPM parallelism at four jobs to
avoid memory pressure on ordinary developer systems. Architecture-specific
configuration remains isolated under `mock/`.

## Quality assurance

Run:

```bash
make test-tooling
make audit
ci/install-test.sh mock/fedora-44-x86_64.cfg .work/repository
```

The audit command runs rpmlint over current specs and binary RPMs, rejects
payloads below `/usr/local` or containing build paths, and rejects duplicate
non-directory file ownership.

Release gating requires zero rpmlint errors. Missing-manual or
subpackage-documentation warnings are retained when upstream provides no
appropriate standalone manual and the package-level rationale documents the
headless test boundary.

The installation test creates clean Fedora 44 Mock roots for:

1. `hyprland` with weak dependencies disabled;
2. `hyprland-desktop`;
3. `hyprwm-complete`.

It checks the installed compositor version and verifies the resulting RPM
database. Graphical compositor, portal, PAM, and Qt interaction tests still
require hardware-capable release runners; a headless Mock result is not
treated as graphical validation.

## Repository generation

The mutable development repository is regenerated with:

```bash
make repo
```

It includes only current manifest versions found below
`results/fedora-44-x86_64`, plus DNF comps metadata for the supported desktop
and complete groups.

An immutable snapshot is created with:

```bash
python3 tooling/hyprwm-packaging snapshot \
  --config-name fedora-44-x86_64 fedora-44-aarch64 \
  --output repo/public \
  --baseurl https://packages.example.invalid/hyprwm/fedora/44/current \
  --signing-key KEY_ID \
  --public-key /path/to/RPM-GPG-KEY-hyprwm-fedora
```

Publication requires a complete artifact set for every requested
architecture. The tool:

1. stages binary RPMs and SRPMs;
2. optionally signs copies, never the build results in place;
3. normalizes snapshot timestamps from the release revision;
4. creates SHA-256 repository metadata and comps data;
5. signs `repomd.xml` when signing is enabled;
6. writes and signs a source/RPM/checksum manifest;
7. renames the completed staging tree into the immutable release path.

The snapshot is inactive by default. After signed DNF and upgrade tests pass,
activate it explicitly:

```bash
make activate PUBLIC_KEY=/secure/path/RPM-GPG-TRUSTED-KEYS
```

Activation re-verifies every RPM header signature, the signed manifest and
repository metadata, and exact manifest-to-file hashes immediately before the
symlink swap. It rejects a revision older than `current` and changes the
symlink atomically. Unsigned private development snapshots require the
explicit `make activate-unsigned` target. Finalized revision directories and
GitHub release assets are never deleted, replaced, or reused; a failed
candidate requires a new revision. If any validation step fails, the previous
`current` target remains unchanged.

Create the deterministic offline archive with:

```bash
make bundle
```

Signed release jobs also publish a SHA-256 checksum and detached signature for
the bundle.

`hyprwm-fedora-release-local` configures the unsigned filesystem repository
used for local development. Signed public snapshots distribute the generated
signature-enforcing `.repo` file and public key instead.

## Update workflow

Stable update detection uses:

```bash
make check-updates
python3 tooling/hyprwm-packaging check-updates --json
```

GitHub release and tag sources are compared with the lock. Commit-pinned
exact-ABI sources are deliberately marked for manual compatibility review.

A standard tag update can be prepared without modifying files:

```bash
python3 tooling/hyprwm-packaging prepare-update hyprutils --tag v0.14.0
```

After reviewing the proposed URL, checksum, tag commit, and version, apply it
with `--apply`. This updates the lock, spec version/release, and package
changelog. It does not guess dependency minima, SONAME compatibility, file
ownership, or patch applicability; the maintainer must inspect those changes
and rebuild the affected closure.

Packages marked `manual` or `pinned` include a committed reason and reject
automatic preparation unless the maintainer explicitly supplies `--force`
after reviewing that policy.

Hyprland itself is never accepted by `prepare-update`, even with `--force`.
Its update must be one reviewed transaction with the exact compatible
`hyprland-plugins` commit and every plugin/meta EVR changed together.

The `affected` command returns the changed package, all reverse dependencies,
and every prerequisite needed to build that closure.

## Continuous integration

- `ci.yml` validates every pull request and main-branch push, performs an
  unsigned Fedora 44 x86_64 Mock build, audits RPMs, and runs DNF installation
  tests in an ephemeral privileged Fedora container.
- `nightly.yml` checks official upstream tags, updates a deduplicated issue,
  rebuilds the lock, tests installation, and reports failures.
- `prepare-update.yml` is a maintainer-dispatched workflow that resolves an
  official tag, updates source/checksum/version/changelog metadata, validates
  the result, and opens a reviewable pull request.
- `release.yml` requires native ephemeral x86_64 and aarch64 Fedora 44
  runners. A protected release environment imports an operator-provided key,
  writes the signed atomic snapshot to the persistent filesystem mounted at
  `REPOSITORY_PUBLISH_ROOT`, tests the signed x86_64 repository through DNF,
  tests upgrade and downgrade against the retained prior snapshot, publishes
  retained offline artifacts, and activates the candidate as the final step.
  `REPOSITORY_BASEURL` must serve that same persistent tree.
- `rollback.yml` verifies every retained RPM plus its repository and manifest
  signatures, then checks dependency closure for both architectures before
  atomically reactivating an older snapshot.

GitHub Actions are pinned to full commits. Pull-request jobs receive no
signing or publication credentials and never run on long-lived release
runners.

Production publication is requested with a `repository_dispatch` payload
containing a `release-<revision>` tag. GitHub runs that workflow from the
default branch. A hosted verification job imports the trusted maintainer keys
from the protected `RELEASE_TAG_TRUSTED_KEYS` secret, verifies the annotated
tag signature, and outputs its commit SHA. Only then do self-hosted builders
check out and execute that verified SHA.

For example:

```bash
gh api --method POST repos/OWNER/REPOSITORY/dispatches \
  -f event_type=release \
  -F 'client_payload[tag]=release-2026.07.15-1'
```

## Adding Fedora 45 or later

1. Add reviewed Mock configurations under `mock/`.
2. Add the release to the manifest schema and validation policy.
3. Run the existing specs unchanged first.
4. Add `%if 0%{?fedora}` only for demonstrated dependency or macro
   differences.
5. Introduce the new release as non-publishing CI.
6. Promote it only after native builds and installation tests pass.

Do not fork every spec or create a release branch merely because Fedora's
version number changed.
