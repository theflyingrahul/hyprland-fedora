#!/usr/bin/bash
set -euo pipefail

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
mock_config=${1:-"$root_dir/mock/fedora-44-x86_64.cfg"}
repository=${2:-"$root_dir/.work/repository"}

repository=$(realpath "$repository")
repo_url="file://$repository"

test_install() {
    local weak_deps=$1
    shift

    mock -r "$mock_config" --clean --quiet
    mock -r "$mock_config" --init --quiet
    mock -r "$mock_config" --addrepo "$repo_url" --dnf-cmd -- \
        --assumeyes \
        --setopt="install_weak_deps=$weak_deps" \
        install "$@"
}

test_install False hyprland
mock -r "$mock_config" --chroot -- rpm --query hyprland
mock -r "$mock_config" --chroot -- bash -lc \
    'runtime=$(mktemp -d); chmod 0700 "$runtime"; XDG_RUNTIME_DIR="$runtime" Hyprland --version-json; rm -rf "$runtime"'

test_install True hyprland-desktop
mock -r "$mock_config" --chroot -- rpm --query \
    hyprland \
    hypridle \
    hyprlock \
    hyprpaper \
    hyprpolkitagent \
    hyprsunset \
    xdg-desktop-portal-hyprland

test_install True hyprwm-complete
mock -r "$mock_config" --chroot -- rpm --query \
    cliphist \
    dolphin \
    fontawesome-6-free-fonts \
    google-noto-sans-fonts \
    grim \
    hyprland-plugins \
    kitty \
    lxappearance \
    mako \
    pipewire \
    qt5-qtwayland \
    qt6-qtwayland \
    slurp \
    waybar \
    wireplumber \
    wl-clipboard \
    xdg-desktop-portal-gtk
mock -r "$mock_config" --chroot -- bash -lc \
    "hyprland-welcome --check-app hyprpolkitagent &&
     hyprland-welcome --check-app xdg-desktop-portal-hyprland"
package_names=$(
    for rpm in "$repository"/Packages/*.rpm; do
        rpm -qp --qf '%{NAME}\n' "$rpm"
    done | sort -u | tr '\n' ' '
)
mock -r "$mock_config" --chroot -- bash -lc \
    "set -e; for package in $package_names; do if rpm -q \"\$package\" >/dev/null 2>&1; then rpm -V \"\$package\"; fi; done"
