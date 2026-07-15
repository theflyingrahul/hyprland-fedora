# hyprgraphics

Rebase of the official Fedora source package to upstream tag `v0.5.1`.

Two later official upstream commits are backported to advertise public and
private pkg-config dependencies correctly. The Fedora patch removes
hard-coded `-O3` and requires JPEG XL plus HEIF/AVIF support, preventing the
library feature set from changing with incidental buildroot contents.
