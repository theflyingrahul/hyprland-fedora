# Build, CI, and release design

## Recommended build workflow

Mock is the authoritative builder. GitHub Actions orchestrates builds but does
not replace the Fedora build environment.

| Tool | Strengths | Limitations | Role in this project |
|---|---|---|---|
| `rpmbuild` | Fast local syntax and package iteration | Host contamination; weak dependency-completeness signal | Developer convenience only |
| Mock | Clean Fedora chroot, repeatable config, complete BuildRequires check | Requires privileged/chroot-capable environment; not a security boundary for hostile code | Authoritative local and CI build |
| `fedpkg` | Fedora dist-git workflow, source lookaside, scratch builds | Assumes Fedora infrastructure and one-package-per-repository conventions | Compatibility and future Fedora-submission path |
| Koji | Production Fedora build model and auditable task graph | Requires infrastructure and authenticated builders | Compatibility target, not initial local infrastructure |
| GitHub Actions | PR, schedule, tag, artifact, and approval orchestration | Hosted runner is not itself Fedora/Koji | CI/CD controller |
| COPR | Convenient hosted RPM builds and repositories | Explicitly not allowed as a project dependency | Optional future publication target only |

### Decision

1. Generate an SRPM for every source package.
2. Rebuild the SRPM with Mock for each Fedora release and architecture.
3. Feed successful RPMs into a temporary local DNF repository.
4. Build the next dependency tier against that repository.
5. Run installation and upgrade tests with DNF.
6. Publish only the complete signed release set.

A bare `rpmbuild -bb` success is not a release result.

### Implemented entry points

The reviewed design is implemented by `tooling/hyprwm-packaging` and thin
Make targets:

| Operation | Command |
|---|---|
| Validate lock and package metadata | `make validate` |
| Run tooling regression tests | `make test-tooling` |
| Build one source package | `make build PACKAGE=<source>` |
| Clean full release-set build | `make build-set` |
| Crash-recovery local build | `make resume-set` |
| Audit specs, payloads, and ownership | `make audit` |
| Rebuild development repository | `make repo` |
| Create immutable snapshot | `make snapshot` |
| Detect official upstream tags | `make check-updates` |

`resume-set` is deliberately separate from the release path. It validates
artifact source name, version, and release before reuse; protected release
jobs never enable it.

## Proposed implementation repository structure

The example structure in the project brief separates all specs and patches.
For a multi-package repository, package-local ownership is easier to review
and less error-prone:

```text
hyprwm-fedora/
  README.md
  docs/
  manifests/
    ecosystem.yaml
    compatibility.yaml
    fedora-releases.yaml
    release-sets/
  packages/
    hyprutils/
      hyprutils.spec
      sources
      patches/
      files/
      README.md
    hyprlang/
    ...
    hyprland/
  mock/
    fedora-44-x86_64.cfg
    fedora-44-aarch64.cfg
  tooling/
    update/
    build/
    qa/
    repository/
  ci/
    package-tiers.yaml
  repo/
    config/
    comps/
    README.md
  .github/
    workflows/
```

Directory responsibilities:

| Directory | Responsibility |
|---|---|
| `docs/` | Investigation, architecture, policy, maintenance, and runbooks |
| `manifests/` | Machine-readable upstream pins, checksums, dependency edges, ABI observations, and supported Fedora releases |
| `packages/<source>/` | One upstream source package's spec, patches, auxiliary source files, and package-specific rationale |
| `mock/` | Reviewed build-root configuration and local-repository injection |
| `tooling/update/` | Tag detection, source checksum, compatibility, and update-PR generation |
| `tooling/build/` | SRPM, Mock, dependency-tier, and reproducibility orchestration |
| `tooling/qa/` | RPM lint, dependency, install, upgrade, file, ABI, and metadata checks |
| `tooling/repository/` | `createrepo_c`, signing handoff, snapshot, and publication logic |
| `ci/` | Declarative build tiers and architecture/release matrices |
| `repo/config/` | Public repository templates and policy; never private keys |
| `repo/comps/` | Optional DNF group metadata |
| `.github/workflows/` | Thin orchestration that calls versioned repository tooling |

Generated RPMs, SRPMs, build roots, private keys, and published repository
trees are ignored artifacts, not source.

## Release channels

| Channel | Source policy | Purpose | Retention |
|---|---|---|---|
| stable | Tagged upstream releases and reviewed lock set | Normal user installation and upgrade | Current plus at least three prior snapshots |
| testing | Candidate stable lock set | Upgrade and integration validation | Until promoted or rejected |
| nightly | Pinned default-branch commits | Early breakage detection only | Short retention |

Nightly packages must have distinct snapshot EVRs and a distinct repository.
They never replace stable packages accidentally.

## Pull request CI

Every pull request runs without signing or publication credentials.

### Documentation-only changes

- local-link checks;
- manifest/schema checks if documentation references machine-readable IDs;
- no RPM build unless package metadata changed.

### Package or manifest changes

1. Validate YAML/JSON schemas and source checksums.
2. Confirm every source URL is immutable or commit-pinned.
3. Verify license files and SPDX expressions.
4. Generate SRPMs.
5. Build affected packages and reverse dependencies in Mock.
6. Run RPM lint and file-ownership checks.
7. Inspect SONAME and exported RPM provides before and after the change.
8. Run DNF install tests against a temporary repository.
9. Validate desktop, AppStream, systemd, D-Bus, PAM, and pkg-config files.
10. Verify no build attempted network access.
11. Upload unsigned RPM/SRPM/log artifacts.

For changes to a core library, the affected set is calculated from the
manifest graph. A "changed package only" build is insufficient.

## Continuous integration

On every merge to the protected default branch:

- rebuild the changed dependency closure;
- compare it with PR artifacts;
- run clean installation and previous-snapshot upgrade tests;
- update a trusted unsigned candidate repository;
- retain logs and manifests.

Default-branch CI does not sign or publish stable content.

## Nightly workflow

The scheduled workflow:

1. Enumerates upstream Git refs.
2. Compares tags and default-branch commits with the lock manifest.
3. Opens or updates one deduplicated update issue/PR per compatible release
   set.
4. Builds selected default-branch snapshots in the separate nightly channel.
5. Runs the complete dependency and installation tests.
6. Reports newly raised dependency minima, SONAME changes, build-system
   changes, and missing releases.

The workflow must detect:

- tags not reflected in `VERSION`;
- `VERSION` changes without tags;
- build-system migrations without version changes;
- new FetchContent or submodule fallback;
- new installed files or services;
- changed plugin commit pins.

## Upstream release update workflow

An update is a repository-wide transaction:

1. Discover the new tag and resolve its commit.
2. Download the release source and calculate its checksum.
3. Read the tagged build manifests.
4. Extract internal minimum versions and external dependency changes.
5. Compare SONAMEs and exported pkg-config/CMake metadata.
6. Select compatible companion versions.
7. Update the release-set manifest.
8. Regenerate package changelog input.
9. Build the complete affected graph.
10. Open a reviewable PR with evidence and generated compatibility changes.

The updater may propose a change. It must not merge or publish a stable
release merely because a tag exists.

## Version and release mapping

- Strip the leading upstream `v` from stable RPM `Version`.
- Use Fedora-compatible `~` ordering for upstream prereleases.
- Use caret snapshot ordering for commits after a release, for example a
  version conceptually equivalent to `0.55.4^20260715git<sha>`.
- Use the explicit per-package release counter stored in the release manifest
  and rendered into `Release:`.
- Never derive the stable version solely from an upstream `VERSION` file.
- Record upstream tag, full commit, source checksum, and source date epoch in
  the release manifest.

Repositories without tags are not admitted to stable automatically. If an
experimental package is approved later, its snapshot version starts below a
future real upstream release and records the commit date and hash.

## Changelog generation

Changelog entries are generated from structured update metadata:

- old and new upstream versions;
- upstream release URL or compare URL;
- dependency/SONAME changes;
- downstream patches added, changed, or removed;
- Fedora-specific integration changes;
- rebuild-only reason when an ABI dependency changed.

Do not use rpmautospec directly in the monorepo. Its release calculation is
based on a persistent dist-git history, while generated per-package filtered
views would make monotonic release counting and cross-package rebuild commits
needlessly fragile.

Instead:

- each package manifest stores an explicit RPM release counter;
- package changes and rebuild-only changes increment that counter
  deterministically;
- update automation generates a package-scoped changelog entry from reviewed
  structured metadata;
- the rendered `Release:` and `%changelog` are committed with the package;
- an export to a future one-package Fedora dist-git repository may convert
  that package to `%autorelease` and `%autochangelog`.

This remains valid Fedora packaging and avoids coupling release numbers to a
synthetic Git history. Automation does not scrape arbitrary upstream commit
messages directly into user-facing changelogs.

## Release workflow

A stable release starts only from a protected signed repository tag and an
approved testing snapshot.

The release workflow is started through a `repository_dispatch` event, so its
orchestration always comes from the protected default branch. Before any
self-hosted runner executes candidate code, a hosted job verifies the
requested `release-<revision>` annotated tag against the protected trusted-key
set and passes only the verified commit SHA to the build matrix.

1. Rebuild all SRPMs in clean Mock roots.
2. Build x86_64 and aarch64 natively.
3. Perform a second independent build for reproducibility comparison.
4. Run DNF install, upgrade, downgrade, and removal tests.
5. Run the [graphical smoke-test plan](graphical-smoke-tests.md) on
   hardware-capable runners.
6. Verify expected compiler/LTO flags and ABI metadata.
7. Produce unsigned immutable artifacts.
8. Approve the protected signing environment.
9. Sign RPMs and `repomd.xml`.
10. Generate and verify the immutable repository snapshot.
11. Atomically publish it and move `current`.
12. Publish SRPMs, RPMs, manifests, checksums, logs, and the offline bundle as
    release artifacts.

## Architectures

Initial publication targets:

- x86_64
- aarch64

Both require native release builders. QEMU builds may be useful for early
compile checks but are not the release authority for compositor timing,
graphics, or architecture-specific behavior.

No `ExcludeArch` is added without a reproduced build or runtime defect.

## Fedora release scaling

The default branch supports the current Fedora release and the next Fedora
release where practical.

- Common specs remain shared.
- `%if 0%{?fedora}` conditionals are used only for real dependency or macro
  differences.
- Mock configuration and publication paths are release-specific.
- A new Fedora release is added first as a non-publishing CI target.
- Release-specific branches are created only when support policies or
  dependency availability cause sustained divergence.

This avoids copying every package directory for Fedora 45.

## GitHub Actions security

- Pull-request jobs use `contents: read` only.
- Fork PRs never run on signing or long-lived self-hosted release runners.
- Build jobs have no GPG or publication credentials.
- Release signing is isolated behind a protected environment and manual
  approval.
- Third-party actions are pinned to full commits.
- Workflow-generated source archives are checksummed before use.
- Self-hosted runners are ephemeral and destroyed after each trusted job.
- Private keys are held outside the repository and ordinary workflow
  artifacts.

Untrusted RPM builds are not treated as sandboxed merely because Mock is
used.

## Failure notifications

- Pull requests receive normal required-check failures and workflow summaries.
- Scheduled failures update one deduplicated GitHub issue with the failing
  package, Fedora release, architecture, upstream ref, and log link.
- Release failures block the protected deployment and leave `current`
  unchanged.
- CODEOWNERS and GitHub notification routing provide the default maintainer
  notification path.
- Optional external notifications are isolated behind repository secrets and
  are not required for correctness.

## Artifact policy

Every successful trusted build retains:

- source RPM;
- binary RPMs;
- build logs;
- package file lists;
- dependency/provides output;
- ABI/SONAME report;
- source and build manifest;
- checksums;
- reproducibility comparison;
- repository metadata for published snapshots.

Artifacts from untrusted PRs are unsigned and expire. Signed release artifacts
and manifests are retained.

## Koji compatibility

Even before a Koji service is deployed, every source package must be
Koji-compatible:

- all sources declared before the build;
- no network access;
- complete BuildRequires;
- standard Fedora macros;
- no dependence on the checkout's untracked files;
- successful SRPM rebuild in a clean Mock root;
- no host-specific paths or CPU flags.

This preserves a future path to Fedora dist-git, private Koji, or optional
COPR publishing without redesigning the packages.
