# Contributing

## Development requirements

Use Fedora 44 with:

```text
mock
rpm-build
rpmdevtools
createrepo_c
curl
git
python3
python3-jsonschema
```

The user running builds must be a member of the `mock` group.

## Repository rules

- Keep one upstream source project per source package.
- Keep package patches and auxiliary files inside `packages/<source>/`.
- Pin every remote source by immutable tag or commit and SHA-256.
- Never fetch from the network during `%prep`, `%build`, `%install`, or
  `%check`.
- Do not add COPR repositories to build roots.
- Do not install package payloads under `/usr/local`.
- Update the release-set manifest whenever package version, release, source,
  dependency tier, or ABI metadata changes.
- Rebuild reverse dependencies when an internal library SONAME changes.
- Do not publish a partial release set.

## Common commands

```bash
make validate
make test-tooling
make check-docs
make fetch PACKAGE=hyprutils
make srpm PACKAGE=hyprutils
make build PACKAGE=hyprutils
make build-set
make resume-set
make repo
make audit
make snapshot
make check-updates
```

The authoritative build path is Mock. Host `rpmbuild` is not a release
builder. `resume-set` is for interrupted local development only; release jobs
perform clean full builds.

## Adding or updating a package

1. Update `manifests/release-set.json`.
2. Add or update `packages/<source>/<source>.spec`.
3. Add downstream patches under `packages/<source>/patches/`.
4. Add auxiliary source files under `packages/<source>/files/`.
5. Record every remote source URL, filename, and SHA-256 in the manifest.
6. Run `make validate`.
7. Build the package and its reverse dependency closure.
8. Review file ownership, generated dependencies, licenses, and ABI changes.

Package release counters are explicit integers in the manifest and spec.
Increment the counter for packaging-only changes and rebuilds. Reset it to
`1` when the upstream `Version` changes.
