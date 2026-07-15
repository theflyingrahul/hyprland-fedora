%global upstream_commit 8c163ce9b8a40f85babe4dd6e23a238787351164

Name:           hyprpicker
Version:        0.4.7
Release:        1%{?dist}
Summary:        Wayland color picker

# The bundled wlroots protocol XML files are HPND-sell-variant.
License:        BSD-3-Clause AND HPND-sell-variant
URL:            https://github.com/hyprwm/hyprpicker
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-cmake-use-release-vcs-metadata.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake >= 3.12
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(hyprutils) >= 0.2.0
BuildRequires:  pkgconfig(hyprwayland-scanner) >= 0.4.0
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)

Recommends:     wl-clipboard
Suggests:       libnotify

%description
Hyprpicker is a Wayland color picker supporting multiple color formats,
optional clipboard integration, notifications, zoom, and live preview.

%prep
%autosetup -p1

%build
%cmake \
    -DCMAKE_INSTALL_MANDIR=%{_mandir} \
    -DGIT_BRANCH=v%{version} \
    -DGIT_COMMIT_HASH=%{upstream_commit} \
    -DGIT_COMMIT_MESSAGE="Release v%{version}" \
    -DGIT_DIRTY=
%cmake_build

%install
%cmake_install

%check
test "$(%{_vpath_builddir}/hyprpicker --version)" = "hyprpicker v%{version}"

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.4.7-1
- Package the official 0.4.7 release
- Replace source-tree Git probing with immutable release metadata
