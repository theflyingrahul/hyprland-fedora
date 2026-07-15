# Generated repository workspace

`repo/public/` is generated and ignored by Git.

Stable publication uses immutable snapshot directories. The build tool first
creates a staging repository under `.work/repository`, verifies it, and only
then copies it to the publication target.

Private signing keys must never be stored below this directory or anywhere in
the Git repository.

## Commands

The mutable build repository is `.work/repository`:

```bash
make repo
```

Immutable snapshots are generated below `repo/public/fedora/44/releases/`:

```bash
make snapshot
```

For a signed public snapshot, invoke the underlying command with
`--signing-key`, `--public-key`, and an HTTPS `--baseurl`. Both copied RPMs and
`repomd.xml` are signed and verified before `current` is changed.

`repo/comps/hyprwm.xml` defines the `Hyprland Desktop` and complete HyprWM DNF
groups. `repo/config/hyprwm-fedora.repo.in` is rendered with signature policy
appropriate to the snapshot.
