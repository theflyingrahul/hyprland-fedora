#!/usr/bin/bash
set -euo pipefail

dnf --assumeyes --setopt=install_weak_deps=False install \
    createrepo_c \
    curl \
    dnf5-plugins \
    git \
    make \
    mock \
    python3 \
    python3-jsonschema \
    rpm-build \
    rpmdevtools \
    rpmlint \
    zstd
