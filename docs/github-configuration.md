# GitHub repository configuration

The source tree and workflows are committed locally. Publishing the repository
is an operator action because repository ownership, visibility, storage
location, signing keys, and reviewer identities are deployment credentials,
not source-code defaults.

## Create and push the repository

Create the GitHub repository with the intended visibility, then add its remote:

```bash
git remote add origin git@github.com:OWNER/hyprland-fedora.git
git push --set-upstream origin main
```

Do not push generated `results/`, `.cache/`, `.work/`, `repo/public/`, RPMs,
private keys, or signing-agent state. They are ignored by Git.

## Default branch protection

Set `main` as the default branch and require:

- pull requests for changes;
- the validation and x86_64 build/install CI checks;
- resolved review conversations;
- no force pushes or branch deletion;
- signed commits where organization policy supports them;
- CODEOWNER review for packaging, workflow, signing, and publication changes.

Restrict creation and deletion of `release-*` tags to release maintainers.
Release tags must be annotated and signed by a key present in the trusted
release-tag keyring.

## Actions and runners

The workflows use only GitHub-owned actions pinned to full commits.

Configure ephemeral native Fedora 44 runners with these labels:

| Architecture | Required labels |
|---|---|
| x86_64 | `self-hosted`, `linux`, `x64`, `fedora-44`, `ephemeral` |
| aarch64 | `self-hosted`, `linux`, `ARM64`, `fedora-44`, `ephemeral` |

Release runners must be recreated after every job. Fork pull requests never
run on them. The x86_64 publication runner additionally needs write access to
the persistent repository root.

## Protected release environment

Create a GitHub environment named `release` with required reviewers and
restricted deployment branches. Store these secrets there:

| Secret | Purpose |
|---|---|
| `RPM_GPG_PRIVATE_KEY` | Armored private package-signing subkey |
| `RPM_GPG_PUBLIC_KEY` | Current armored public RPM key |
| `RPM_GPG_KEY_ID` | Fingerprint or signing identity used by RPM and GPG |
| `RPM_GPG_TRUSTED_PUBLIC_KEYS` | Independently maintained historical public keyring used for rollback |

Store `RELEASE_TAG_TRUSTED_KEYS` as a repository or organization secret
available to the hosted tag-verification job. It contains only the public keys
authorized to sign `release-*` tags.

Configure these repository or environment variables:

| Variable | Purpose |
|---|---|
| `REPOSITORY_PUBLISH_ROOT` | Persistent mounted filesystem root containing `fedora/44/releases/` and `current` |
| `REPOSITORY_BASEURL` | HTTPS base URL corresponding to `fedora/44/current` |

The storage account should prevent unrelated jobs from modifying finalized
snapshots. The tooling also seals snapshot files read-only, rejects reused
revision directories, and re-verifies all signed contents immediately before
activation.

## Request a release

The release workflow is a `repository_dispatch` workflow so GitHub always
loads its orchestration from the protected default branch. Request a release
after pushing the reviewed signed tag:

```bash
gh api --method POST repos/OWNER/hyprland-fedora/dispatches \
  -f event_type=release \
  -F 'client_payload[tag]=release-2026.07.15-1'
```

The hosted verification job resolves and verifies the tag before any
self-hosted runner checks out candidate code.

## Request a rollback

Retained snapshots are immutable. Request rollback by revision:

```bash
gh api --method POST repos/OWNER/hyprland-fedora/dispatches \
  -f event_type=rollback \
  -F 'client_payload[revision]=2026.07.15-1'
```

The rollback workflow uses the protected historical keyring, verifies every
RPM plus signed metadata and manifests for both architectures, checks
dependency closure, and only then changes `current`.

## Required release checks

Before approving publication, confirm:

- native x86_64 and aarch64 builds completed;
- signed-tag verification passed;
- package audit has zero errors;
- signed minimal install passed;
- previous-to-current upgrade and current-to-previous downgrade passed;
- the hardware smoke-test plan is complete;
- the repository and GitHub release revision have never been used before.
