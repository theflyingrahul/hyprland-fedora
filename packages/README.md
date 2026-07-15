# Package sources

Each directory under `packages/` represents one RPM source package and owns:

```text
packages/<source>/
  <source>.spec
  patches/
  files/
  README.md
```

Remote source archives are not committed. Their immutable URLs, filenames,
and SHA-256 checksums are recorded in `manifests/release-set.json` and cached
under `.cache/sources/`.

Metadata-only and repository-configuration source packages may have no remote
archive. Their manifest `sources` array is empty and every local input is
stored under `files/`.

The build tool copies cached remote sources, package-local patches, and
package-local files into a clean Mock source directory before creating the
SRPM.
