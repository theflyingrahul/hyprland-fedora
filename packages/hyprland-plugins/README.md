# hyprland-plugins

Official Hyprland plugins built from upstream commit
`3aa21f2e0ca72412f1b434c3126f8f1fec3c716c`. Upstream's `hyprpm.toml`
maps that exact plugin commit to Hyprland `v0.55.4` commit
`a0136d8c04687bb36eb8a28eb9d1ff92aea99704`.

The plugins are installed below `%{_libdir}/hyprland/plugins` rather than as
generic shared libraries. Every binary package requires the exact Hyprland
EVR and `hyprland-plugin-api` capability used for its build. LTO is disabled
for both sides of the plugin ABI.
