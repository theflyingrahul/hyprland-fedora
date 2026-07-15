%global upstream_commit d75e93f8ee1721d70549d96f4d14bf2948aab70c

Name:           hyprlock
Version:        0.9.5
Release:        1%{?dist}
Summary:        GPU-accelerated screen locker for Hyprland

# The bundled wlr-screencopy protocol XML is HPND-sell-variant.
License:        BSD-3-Clause AND HPND-sell-variant
URL:            https://github.com/hyprwm/hyprlock
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-cmake-respect-fedora-optimization-flags.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake >= 3.27
BuildRequires:  cmake(hyprwayland-scanner) >= 0.4.4
BuildRequires:  date-devel
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hyprgraphics) >= 0.1.6
BuildRequires:  pkgconfig(hyprlang) >= 0.6.0
BuildRequires:  pkgconfig(hyprutils) >= 0.11.0
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(sdbus-c++) >= 2.0.0
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.35
BuildRequires:  pkgconfig(xkbcommon)

%description
Hyprlock is a GPU-accelerated Wayland screen locker for Hyprland with
configurable backgrounds, input fields, labels, images, and authentication.

%prep
%autosetup -p1

%build
%cmake \
    -DHYPRLOCK_COMMIT=%{upstream_commit} \
    -DHYPRLOCK_VERSION_COMMIT=%{upstream_commit}
%cmake_build

%install
%cmake_install

%check
test "$(%{_vpath_builddir}/hyprlock --version)" = "Hyprlock version v%{version}"

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%{_datadir}/hypr/hyprlock.conf

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.9.5-1
- Package the official 0.9.5 release
- Preserve Fedora flags and embed the immutable release commit
