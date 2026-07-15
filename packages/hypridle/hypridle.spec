Name:           hypridle
Version:        0.1.7
Release:        1%{?dist}
Summary:        Idle management daemon for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hypridle
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-cmake-respect-fedora-optimization-flags.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake >= 3.19
BuildRequires:  cmake(hyprwayland-scanner) >= 0.4.4
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(hyprland-protocols) >= 0.6.0
BuildRequires:  pkgconfig(hyprlang) >= 0.6.0
BuildRequires:  pkgconfig(hyprutils) >= 0.2.0
BuildRequires:  pkgconfig(sdbus-c++) >= 0.2.0
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)

Recommends:     hyprlock

%description
Hypridle is Hyprland's idle management daemon. It runs configured commands on
idle, resume, and lock events and implements the session D-Bus screensaver
inhibition interface.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%check
test "$(%{_vpath_builddir}/hypridle --version)" = "hypridle v%{version}"

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun_with_restart %{name}.service

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/hypr/hypridle.conf
%{_userunitdir}/%{name}.service

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.1.7-1
- Package the official 0.1.7 release
- Preserve Fedora optimization flags and install the upstream user service
