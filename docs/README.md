# Documentation index

This directory contains the completed investigation, design, and
implementation runbooks for the HyprWM Fedora packaging project.

## Reading order

1. [Phase 1 investigation report](phase-1-report.md)
2. [Upstream repository inventory](upstream-inventory.md)
3. [Dependency graph and build order](dependency-graph.md)
4. [Downstream packaging survey](downstream-packaging-survey.md)
5. [Fedora packaging design](fedora-packaging-design.md)
6. [Build, CI, and release design](build-release-design.md)
7. [Local DNF repository design](local-repository-design.md)
8. [Compiler and optimization policy](build-optimization.md)
9. [Risk assessment](risk-assessment.md)
10. [Primary source index](source-index.md)
11. [Implementation and maintenance guide](implementation-guide.md)
12. [Graphical release smoke tests](graphical-smoke-tests.md)

## Evidence rules

- Stable packaging decisions use tagged upstream sources. The explicit
  exception is an exact-ABI component, such as `hyprland-plugins`, when
  upstream's compatibility metadata pins a specific untagged commit to the
  selected tagged consumer.
- Default-branch observations are labeled as unreleased.
- Git tags are enumerated directly with Git; `VERSION` files are not assumed
  to identify the latest release.
- Build dependencies come from build manifests, package-config templates,
  generated-target declarations, and install rules.
- Downstream behavior comes from distribution packaging sources, not install
  guides or blog posts.
- Fedora requirements, Fedora defaults, and this project's policy are kept
  separate.
- Unknown or unverified compatibility is treated as a release blocker, not
  filled in by inference.

## Phase history

Phase 1 ended with documentation only. The reviewed design is now implemented
under `packages/`, `tooling/`, `mock/`, `ci/`, `repo/`, and
`.github/workflows/`. Generated RPMs, source caches, build roots, private keys,
and repository snapshots remain untracked.
