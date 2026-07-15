# Local DNF repository design

## Goals

The generated repository must support:

- `dnf install hyprland`
- normal `dnf upgrade`
- Fedora 44 architecture separation
- optional package and repository metadata signatures
- immutable releases
- offline installation
- rollback to a known repository snapshot
- atomic publication of the complete HyprWM dependency set

## Repository model

Every publication is an immutable snapshot. A mutable `current` reference
points to one verified snapshot only after every package, signature, and
metadata check succeeds.

Proposed published layout:

```text
repo/
  public/
    RPM-GPG-KEY-hyprwm-fedora
    fedora/
      44/
        releases/
          2026.07.15-1/
            x86_64/
              Packages/
              repodata/
              SRPMS/
              manifest.json
            aarch64/
              Packages/
              repodata/
              SRPMS/
              manifest.json
        current -> releases/2026.07.15-1
```

Architecture-independent RPMs are copied or hard-linked into each
architecture repository so a normal DNF base URL is sufficient.

The working tree does not track generated RPMs, private keys, or complete
repository snapshots.

### Implemented commands

The mutable dependency repository used during builds is regenerated with:

```bash
make repo
```

The publication implementation is:

```bash
python3 tooling/hyprwm-packaging snapshot \
  --config-name fedora-44-x86_64 fedora-44-aarch64 \
  --output repo/public \
  --baseurl https://packages.example.invalid/hyprwm/fedora/44/current \
  --signing-key KEY_ID \
  --public-key /secure/path/RPM-GPG-KEY-hyprwm-fedora
```

The command refuses partial architecture or package sets, stages output under
a temporary directory, signs and verifies RPM, repomd, and manifest content,
then renames the inactive immutable snapshot. Release automation tests that
candidate through DNF and activates it separately. It points `--output` at
persistent mounted publication storage; an ephemeral runner workspace is
never treated as publication.

## Bootstrap configuration

The noarch `hyprwm-fedora-release-local` RPM is the unsigned local filesystem
bootstrap. It owns:

- `/etc/yum.repos.d/hyprwm-fedora.repo`

It points at `/srv/hyprwm-fedora/fedora/44/current/$basearch/` and disables
signature checks explicitly because it is for an unsigned private development
repository.

Signed public snapshots instead contain:

- `hyprwm-fedora.repo` with `pkg_gpgcheck=1` and `repo_gpgcheck=1`;
- `RPM-GPG-KEY-hyprwm-fedora`;
- signed RPMs and `repomd.xml.asc`.

The public bootstrap flow is:

1. Obtain the snapshot repository file and public key from the signed release
   bundle.
2. Verify the bundle checksum and release provenance.
3. Install the key and repository file through the operator's normal
   configuration-management or bootstrap-RPM process.
4. Run `dnf install hyprland`.

No workflow writes compositor payloads into `/usr/local` or copies package
files outside RPM ownership. Repository configuration is either owned by the
local release RPM or deployed as ordinary signed-release system
configuration.

## Metadata generation

`createrepo_c` is the metadata generator.

Publication requirements:

- unique metadata filenames;
- an explicit snapshot revision;
- deterministic timestamps tied to the release timestamp;
- package checksums;
- filelists and other metadata required by DNF;
- update information when security or important bug-fix classification is
  available;
- optional comps/group metadata for a future `Hyprland Desktop` group;
- a machine-readable manifest containing source commits, source checksums,
  RPM NEVRAs, architectures, and repository checksums.

Incremental `--update` generation may be used in a staging directory, but the
public snapshot is never modified in place.

## Atomic publication

1. Create a new staging snapshot.
2. Copy only artifacts from successful, trusted release jobs.
3. Generate repository metadata.
4. Run DNF dependency-resolution tests against the staging base URL.
5. Sign RPMs and metadata if signing is enabled.
6. Verify every signature and checksum from a clean client environment.
7. Move the completed directory into `releases/`.
8. Atomically change `current`.

If any package in the locked release set fails, `current` remains unchanged.
Publishing only the successful subset is forbidden.

## GPG signing

Signing is optional for private development repositories and required for
public release snapshots.

Two independent signatures are needed:

1. RPM package signatures.
2. A detached signature for `repodata/repomd.xml`.

The public key is tracked and distributed. The private key is never committed
to Git, embedded in an image, exposed to pull-request jobs, or passed to
untrusted build steps.

Recommended key handling:

- an offline primary certification key;
- a dedicated package-signing subkey;
- a noninteractive signing service or isolated agent made available only to
  the protected release job;
- a documented rotation and revocation process;
- signing only after unsigned artifacts have passed all build and QA checks;
- an isolated protected publish job or external signing service;
- archived signed manifests for every snapshot.

## DNF5 configuration

DNF5 distinguishes package and metadata signature checking. A release repo
must explicitly enable both; `gpgcheck=1` alone can retain legacy semantics
that check packages but not repository metadata.

The generated configuration will express the equivalent of:

```ini
[hyprwm-fedora]
name=HyprWM Fedora 44
baseurl=file:///srv/hyprwm-fedora/fedora/44/current/$basearch/
enabled=1
pkg_gpgcheck=1
repo_gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-hyprwm-fedora
metadata_expire=1h
skip_if_unavailable=0
```

An HTTPS base URL can replace `file://` without changing package layout.

The repo file must not disable signature checks globally or set unrelated DNF
options.

## Local and offline use

### Filesystem repository

For one machine, the published snapshot can reside under `/srv` or removable
storage and use a `file://` base URL.

### Static HTTP repository

For a LAN, serve the same immutable directory tree with any static HTTPS
server. No custom package service is required.

### Offline bundle

Each release can produce:

```text
hyprwm-fedora-44-2026.07.15-1/
  RPM-GPG-KEY-hyprwm-fedora
  hyprwm-fedora.repo
  x86_64/
    Packages/
    repodata/
    manifest.json
```

The bundle is suitable for copying to removable media. Offline instructions
must disable unrelated repositories explicitly when a fully disconnected
installation is required.

## Updates

Normal updates use:

```text
dnf upgrade
```

This works because:

- package names remain stable;
- RPM EVRs increase normally;
- repository `current` points to the new complete snapshot;
- old and new internal library dependencies are represented by RPM SONAME
  requirements;
- plugin packages use exact Hyprland coupling;
- no files are managed outside RPM.

The release RPM can update repository URLs or keys through an ordinary RPM
transaction.

## Rollback

Rollback has two layers.

### Repository rollback

Keep a configured number of immutable prior snapshots. To roll the repository
back, atomically repoint `current` to a previous snapshot. This restores
availability of the exact old NEVRAs and metadata.

The implemented operation is:

```bash
make rollback \
  REVISION=2026.07.15-1 \
  PUBLIC_KEY=/secure/path/RPM-GPG-TRUSTED-KEYS
```

Before changing `current`, it verifies all RPM signatures and the detached
signatures for `repomd.xml` and `manifest.json` on both supported
architectures. It also requires exact manifest inventory, hashes, sizes,
architecture, revision, SRPM relationships, and `repomd.xml` checksum
correspondence. The protected `rollback.yml` workflow preflights dependency
closure for both architectures before performing the same signature
verification again and changing `current`. It uses the independently
protected `RPM_GPG_TRUSTED_PUBLIC_KEYS` keyring and never trusts a key stored
inside the snapshot being rolled back to.

### Client rollback

DNF5 history supports transaction inspection, undo, redo, rollback, store,
and replay. A rollback succeeds only if the required old packages are still
available, which is why server-side snapshot retention is mandatory.

For a controlled rollback:

1. Point the client at the intended immutable snapshot.
2. Refresh metadata.
3. Use DNF history rollback or an explicit versioned downgrade.
4. Store the transaction record for fleet reproduction.

Do not describe DNF history as a substitute for retaining old packages.

## Retention

Default proposed policy:

- keep the current and previous three stable snapshots online;
- keep all signed release manifests and SRPMs permanently;
- keep nightly snapshots for 14 days;
- keep failed staging repositories only long enough for diagnosis;
- never reuse a snapshot identifier.

Retention values are operational policy and can change without changing RPM
package semantics.

## Repository QA

Before publication, test from a clean Fedora 44 environment:

- repository metadata and signature verification;
- `dnf repoquery --requires --resolve` for every package;
- `dnf install hyprland`;
- minimal installation with weak dependencies disabled;
- full recommended installation;
- upgrade from the previous snapshot;
- downgrade/rollback to the previous snapshot;
- removal and reinstall;
- offline installation from the bundle;
- no unresolved or duplicate file ownership;
- no dependencies on COPR, `/usr/local`, or build paths.

The repository is complete only when these operations succeed against its own
published content plus standard Fedora repositories.
