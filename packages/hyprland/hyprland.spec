%global _lto_cflags %{nil}
%global upstream_commit a0136d8c04687bb36eb8a28eb9d1ff92aea99704

Name:           hyprland
Version:        0.55.4
Release:        3%{?dist}
Summary:        Dynamic tiling Wayland compositor

# The source archive's bundled udis86, Tracy, and hyprland-protocols trees are
# removed during prep and are not part of the binary build.
License:        BSD-3-Clause AND MIT AND LGPL-2.1-or-later AND HPND-sell-variant
URL:            https://github.com/hyprwm/Hyprland
Source0:        %{url}/releases/download/v%{version}/source-v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-build-require-system-dependencies.patch
Patch1:         0002-pkgconfig-export-lua-headers.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake >= 3.30
BuildRequires:  cmake(glaze) >= 7
BuildRequires:  cmake(hyprwayland-scanner) >= 0.3.10
BuildRequires:  cmake(hyprwire-scanner) >= 0.3.1
BuildRequires:  gcc-c++
BuildRequires:  glslang-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  ninja-build
BuildRequires:  python3
BuildRequires:  udis86-devel
BuildRequires:  pkgconfig(aquamarine) >= 0.9.3
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hyprcursor) >= 0.1.7
BuildRequires:  pkgconfig(hyprgraphics) >= 0.5.1
BuildRequires:  pkgconfig(hyprland-protocols) >= 0.6.4
BuildRequires:  pkgconfig(hyprlang) >= 0.6.7
BuildRequires:  pkgconfig(hyprutils) >= 0.13.1
BuildRequires:  pkgconfig(hyprwire) >= 0.3.1
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput) >= 1.28
BuildRequires:  pkgconfig(lua5.5) >= 5.5
BuildRequires:  pkgconfig(muparser)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(re2)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.47
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server) >= 1.22.91
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xkbcommon) >= 1.11

Requires:       aquamarine%{?_isa} >= 0.9.3
Requires:       hyprcursor%{?_isa} >= 0.1.7
Requires:       hyprgraphics%{?_isa} >= 0.5.1
Requires:       hyprlang%{?_isa} >= 0.6.7
Requires:       hyprutils%{?_isa} >= 0.13.1
Requires:       xdg-desktop-portal%{?_isa}
Requires:       xorg-x11-server-Xwayland%{?_isa}
Provides:       wayland-compositor
Provides:       hyprland-plugin-api = %{version}-%{release}
Recommends:     hyprland-backgrounds = %{version}-%{release}
Recommends:     hypridle
Recommends:     hyprlock
Recommends:     hyprpaper
Recommends:     hyprpolkitagent
Recommends:     hyprsunset
Recommends:     xdg-desktop-portal-hyprland
Suggests:       hyprland-guiutils
Suggests:       hyprland-qt-support
Suggests:       hyprlauncher
Suggests:       hyprpicker
Suggests:       hyprpm
Suggests:       hyprpwcenter
Suggests:       hyprqt6engine
Suggests:       hyprshutdown
Suggests:       hyprsysteminfo

%description
Hyprland is a dynamic tiling Wayland compositor with animated layouts,
extensive configuration, IPC, and a plugin interface.

%package devel
Summary:        Development files and plugin API for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       glslang-devel

%description devel
Headers, generated protocol bindings, and pkg-config metadata used to build
Hyprland plugins against this exact compositor release.

%package backgrounds
Summary:        Background images for %{name}
BuildArch:      noarch

%description backgrounds
Architecture-independent background and lock-screen images shipped by
Hyprland upstream.

%package -n hyprpm
Summary:        Local plugin build manager for Hyprland
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       cmake
Requires:       cpio
Requires:       gcc
Requires:       gcc-c++
Requires:       git-core
Requires:       make
Requires:       ninja-build
Requires:       pkgconf-pkg-config

%description -n hyprpm
Hyprpm clones and builds third-party Hyprland plugins locally. Packaged
official plugins remain the preferred reproducible installation path.

%prep
%autosetup -n hyprland-source -p1
rm -rf subprojects/hyprland-protocols subprojects/tracy subprojects/udis86

%build
%cmake \
    -DBUILD_TESTING=OFF \
    -DNO_UWSM=ON \
    -DUSE_TRACY=OFF \
    -DWITH_TESTS=OFF
%cmake_build

%install
%cmake_install

%check
install -d -m 0700 test-runtime
export XDG_RUNTIME_DIR="$PWD/test-runtime"
test "$(%{_vpath_builddir}/Hyprland --version-json | python3 -c \
    'import json,sys; print(json.load(sys.stdin)["commit"])')" = "%{upstream_commit}"

%files
%license LICENSE
%doc README.md
%{_bindir}/Hyprland
%{_bindir}/hyprland
%{_bindir}/hyprctl
%{_bindir}/start-hyprland
%dir %{_datadir}/hypr
%{_datadir}/hypr/hyprland.lua
%{_datadir}/hypr/stubs/
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
%{_mandir}/man1/Hyprland.1*
%{_mandir}/man1/hyprctl.1*
%{_datadir}/bash-completion/completions/hyprctl
%{_datadir}/fish/vendor_completions.d/hyprctl.fish
%{_datadir}/zsh/site-functions/_hyprctl

%files devel
%license LICENSE
%{_includedir}/hyprland/
%{_datadir}/pkgconfig/hyprland.pc

%files backgrounds
%license LICENSE
%{_datadir}/hypr/*.png

%files -n hyprpm
%license LICENSE
%{_bindir}/hyprpm
%{_datadir}/bash-completion/completions/hyprpm
%{_datadir}/fish/vendor_completions.d/hyprpm.fish
%{_datadir}/zsh/site-functions/_hyprpm

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.55.4-3
- Export the Lua 5.5 header dependency through hyprland.pc

* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.55.4-2
- Require glslang headers exposed by the installed plugin API

* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.55.4-1
- Update Hyprland to 0.55.4 and build against the Fedora 44 HyprWM stack
- Require system udis86, Glaze, Lua 5.5, protocols, and Hyprwire
- Split plugin headers, backgrounds, and hyprpm into dedicated packages
