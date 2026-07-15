# Risk assessment

## Risk model

Impact is assessed against the primary promise: a coherent Fedora repository
where `dnf install hyprland` and later `dnf upgrade` remain reliable.

| Risk | Likelihood | Impact | Primary detection | Mitigation |
|---|---|---|---|---|
| Hypr library SONAME change | High | Critical | Compare built ELF SONAME/RPM provides | Rebuild full reverse dependency closure and publish atomically |
| Partial ecosystem publication | Medium without controls | Critical | Repository dependency solve and release-manifest completeness | Never move `current` unless every locked package succeeds |
| Hyprland plugin ABI mismatch | High | Critical for plugin users | Exact commit/EVR check and plugin load smoke test | Build plugins after Hyprland and require exact Hyprland EVR |
| Fedora 44 compiler cannot build new C++26 source | Medium | High | Scheduled Mock build of upstream tags/main | Compiler gate, narrow upstream patches, hold incompatible update |
| External dependency below upstream minimum | Medium | High | Fedora dependency feasibility matrix and Mock configure | Add a separate prerequisite package, patch only with evidence, or defer feature |
| Upstream FetchContent/submodule network fallback | High | High | Network-disabled Mock and source scan | Supply system dependency or declared Source; force offline configuration |
| Upstream tag/version mismatch | High | High | Git-ref discovery compared with `VERSION` | Treat Git refs and pinned commits as authoritative |
| Build-system change without release-version change | Medium | High | Diff tagged manifests and default branch | Record build system in lock manifest; human review before update |
| Source-tree-mutating code generation | High | Medium | Repeated clean-build comparison | Fresh source tree per build and no shared parallel source checkout |
| Non-reproducible Git metadata | High without injection | High | Rebuild comparison and version output | Inject deterministic tag/commit/date/dirty/count values |
| Hard-coded optimization overrides Fedora flags | High | Medium | Inspect compile commands | Patch out `-O3`; assert expected flags in CI |
| LTO breaks plugin compatibility | Medium | High | Compiler/link command check and plugin load test | Disable LTO for Hyprland and plugins |
| Optional codec support changes accidentally | Medium | Medium | Feature report comparison | Declare all intended codec BuildRequires and fail if missing |
| Fedora official stale packages mix with repository packages | Medium | High | DNF transaction tests using clean Fedora 44 | Publish complete higher-EVR set; require matching internal ABI/versions |
| Prior COPR epochs block upgrades | Medium for existing users | Medium | Upgrade test from known COPR NEVRAs | Document repository migration; do not inherit arbitrary third-party epochs blindly |
| Portal backend misselection | Medium | High for screen sharing | Portal integration smoke tests | Correct `.portal` metadata, session environment, and no unnecessary conflicts |
| Multiple portal backends conflict in files or selection | Medium | Medium | Install test with GNOME/KDE/wlr backends | Allow coexistence; rely on upstream selection configuration |
| PAM configuration breaks unlock | Low with testing | Critical | Console/VM authentication test and config validation | Ship Fedora-appropriate `%config(noreplace)` PAM file |
| systemd user unit starts at wrong session phase | Medium | Medium | User-session integration test | Use `%{_userunitdir}`, correct targets, and Fedora macros |
| Missing AppStream metadata | High | Low runtime, medium UX | Metadata scan and validator | Add reviewed downstream metadata and submit upstream |
| Desktop file invalid or points to missing binary | Medium | Medium | `desktop-file-validate` and install test | Fail CI on validation errors |
| SELinux denial | Low to medium | High for affected feature | Enforcing-mode VM tests and AVC review | Use standard paths; add policy only for reproduced denials |
| `cap_sys_nice` security/behavior tradeoff | Medium | Medium | Scheduling behavior and capability audit | Decide explicitly, minimize capability, document and test |
| Proprietary NVIDIA runtime differences | Medium | High for affected users | Hardware smoke-test matrix | No driver dependency; test supported NVIDIA path separately |
| Wayland/libinput protocol version drift | Medium | High | Rawhide and Fedora 44 build/integration tests | Gate updates on minimum availability and protocol tests |
| UWSM integration absent or mismatched | Medium | Medium | Session-entry install and login test | Package/require or disable the UWSM entry coherently |
| D-Bus activation file mismatch | Low | High for portal/polkit | D-Bus activation tests | Validate names, executable paths, and ownership |
| GPG key compromise | Low | Critical | Signing audit and key monitoring | Offline primary key, isolated subkey, rotation/revocation plan |
| Metadata signed but RPMs unsigned, or reverse | Low with checks | Critical | Clean-client signature verification | Require both package and `repomd.xml` verification |
| Repository rollback lacks old RPMs | Medium without retention | High | Rollback CI | Immutable retained snapshots plus DNF history |
| Untrusted PR reaches self-hosted runner or secrets | Low with controls | Critical | Workflow permission review | Hosted unprivileged PR jobs; protected ephemeral release runners |
| Maintainer bus factor | High historically | High | Ownership review and stale automation alerts | Multiple owners, CODEOWNERS, runbooks, automated update evidence |
| Fedora release transition causes spec divergence | Medium | Medium | Current+next Fedora CI matrix | Shared specs, minimal conditionals, release branch only when necessary |
| aarch64 compiles but is not runtime tested | Medium | Medium | Native hardware smoke test | Native release builders and architecture-specific validation |
| Archived upstream project causes dependency/file conflict | Medium | Medium | Upgrade test from qtutils/welcome packages | Package successor only with explicit transition metadata |

## ABI and dependency risk

### Shared libraries

Hypr libraries use independent semantic versions and SOVERSION counters.
Several remain below 1.0 and change SONAME frequently.

Mitigation:

- extract SONAME from built artifacts rather than infer it from `Version`;
- store the result in the compatibility manifest;
- query RPM-generated provides and requires;
- calculate reverse dependencies from both the declared graph and actual RPM
  metadata;
- rebuild every dependent package even when its upstream source did not
  change;
- publish one snapshot.

### Plugins

Hyprland installs large portions of its internal headers for plugin builds.
`hyprland-plugins` maps compositor commits to plugin commits.

Mitigation:

- exact source pins;
- exact RPM EVR requirement;
- same compiler and flags;
- LTO disabled on both sides;
- an actual load/unload smoke test in a nested session;
- no claim of compatibility based only on `0.55.x`.

## Fedora 44 compatibility

### C++26

Fedora 44 has a new enough toolchain to attempt current Hyprland, but the
source must still be compiled in Mock. The project must be prepared for
upstream to adopt a compiler feature faster than a stable Fedora release.

Mitigation:

- current and Rawhide scheduled builds;
- hold releases that cannot build with Fedora's supported compiler;
- avoid replacing the system compiler in ordinary package builds;
- add a package-local backport only when small, reviewed, and upstreamable.

### External libraries

Fast-moving minimums for Wayland, libinput, xkbcommon, Lua, Qt, and the Hypr
libraries can exceed stable Fedora.

Mitigation:

- maintain an exact Fedora dependency matrix;
- package missing prerequisites separately when licensing and maintenance are
  acceptable;
- avoid private vendoring;
- disable only genuinely optional features;
- do not publish a package whose documented feature set differs silently by
  architecture or buildroot.

## Wayland and desktop integration

### Portal

The portal may install successfully while screen sharing fails because the
wrong backend is selected or PipeWire negotiation is broken.

Mitigation:

- test with a real Hyprland session;
- verify `XDG_CURRENT_DESKTOP` and session desktop files;
- test screenshot, screencast, global shortcuts, and input capture where
  upstream advertises them;
- install alongside other common portal backends;
- do not add broad `Conflicts`.

### XWayland

Hyprland can run without XWayland, but many desktop applications still need
it.

Mitigation:

- build XWayland support;
- use a weak runtime dependency on the XWayland server if Fedora precedent
  supports optional operation;
- test both X11 and native Wayland clients;
- record the build option in package metadata.

### systemd user services

User services can start too early, remain active outside a graphical session,
or conflict with explicit Hyprland configuration.

Mitigation:

- preserve upstream unit semantics;
- use Fedora user-unit macros;
- do not enable units globally without a reviewed preset policy;
- test login, logout, restart, and multiple-session behavior.

## SELinux

The current package set consists mainly of user-session applications and
shared libraries in standard `/usr` paths. No custom SELinux policy is
justified by upstream metadata alone.

Policy:

- test on Fedora 44 with SELinux enforcing;
- inspect AVC denials;
- correct paths, permissions, D-Bus policy, or capabilities first;
- introduce a policy package only for a reproducible denial that cannot be
  solved through standard interfaces;
- never disable SELinux or recommend permissive mode.

## Graphics drivers

The packages link against Fedora's standard DRM, GBM, EGL, and GLES
interfaces. They do not package kernel modules or proprietary drivers.

Mesa is the baseline validation path. NVIDIA is a separate runtime
compatibility matrix, not an RPM dependency on RPM Fusion.

Tests should cover:

- Mesa AMD;
- Mesa Intel;
- a currently supported proprietary NVIDIA stack when hardware is available;
- multi-monitor, suspend/resume, direct scanout, screencast, and XWayland.

Secure Boot is not directly affected because this repository ships no kernel
module.

## Maintenance burden

Fedora and Gentoo both lost in-tree Hyprland packaging after ecosystem velocity
outpaced available maintainers. Automation reduces work but does not replace
ownership.

Required governance:

- at least two maintainers able to publish;
- package-level CODEOWNERS;
- documented key and release succession;
- automated stale-update and failed-nightly issues;
- a release-set review checklist;
- an explicit support window for Fedora releases;
- the ability to defer immature repositories without blocking the stable core.

The complete HyprWM organization is not the same as the supported stable
package set. Experimental untagged projects are admitted only when their
upstream install and version contracts become maintainable.
