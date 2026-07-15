# lua5.5

Parallel-installable Lua 5.5 compatibility package for Fedora 44.

Fedora 44 uses Lua 5.4 as the system ABI, while Hyprland 0.55.x searches for
Lua 5.5-specific pkg-config modules. This package deliberately avoids
replacing or conflicting with Fedora's `lua`, `lua-libs`, and `lua-devel`
packages.

## Installed namespace

- `/usr/bin/lua5.5`
- `/usr/bin/luac5.5`
- `/usr/lib64/liblua5.5.so.*`
- `/usr/include/lua5.5/`
- versioned pkg-config aliases including `lua55` and `lua5.5`
- `/usr/{lib64,share}/lua/5.5/`

## Source provenance

- Lua 5.5.0 and its tests come directly from `lua.org`.
- The two bug-fix patches come from immutable official Fedora Rawhide
  dist-git commit `e658e44a5ef9c611b9f4d006599a792874ab6555`.
- No COPR, personal mirror, or third-party packaging repository is used.
