Name:           xdg-desktop-portal-hyprland
Version:        1.3.12
Release:        1%{?dist}
Summary:        XDG desktop portal backend for Hyprland

# The bundled wlroots protocol XML files are HPND-sell-variant.
License:        BSD-3-Clause AND HPND-sell-variant
URL:            https://github.com/hyprwm/xdg-desktop-portal-hyprland
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-cmake-require-system-dependencies-and-fedora-flags.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake >= 3.19
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(hyprland-protocols) >= 0.6.4
BuildRequires:  pkgconfig(hyprlang) >= 0.2.0
BuildRequires:  pkgconfig(hyprutils) >= 0.2.6
BuildRequires:  pkgconfig(hyprwayland-scanner) >= 0.4.2
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3) >= 1.1.82
BuildRequires:  pkgconfig(sdbus-c++) >= 2.0.0
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)

Requires:       grim
Requires:       qt6-qtwayland
Requires:       xdg-desktop-portal
Recommends:     hyprpicker
Recommends:     slurp
Supplements:    (hyprland and xdg-desktop-portal)

%description
XDG Desktop Portal Hyprland provides screenshot, screen-cast, and global
shortcut portal interfaces for Hyprland. It includes a Qt screen-sharing
selection helper and D-Bus-activated user service.

%prep
%autosetup -p1
rm -rf subprojects/sdbus-cpp subprojects/hyprland-protocols

%build
%cmake -DSYSTEMD_SERVICES=ON
%cmake_build

%install
%cmake_install

%check
test "$(%{_vpath_builddir}/xdg-desktop-portal-hyprland --version)" = \
    "xdg-desktop-portal-hyprland v%{version}"
grep -q '^DBusName=org\.freedesktop\.impl\.portal\.desktop\.hyprland$' \
    %{buildroot}%{_datadir}/xdg-desktop-portal/portals/hyprland.portal
grep -q '^SystemdService=xdg-desktop-portal-hyprland\.service$' \
    %{buildroot}%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.hyprland.service
grep -q '^BusName=org\.freedesktop\.impl\.portal\.desktop\.hyprland$' \
    %{buildroot}%{_userunitdir}/xdg-desktop-portal-hyprland.service

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun_with_restart %{name}.service

%files
%license LICENSE
%doc README.md contrib/config.sample
%{_bindir}/hyprland-share-picker
%{_libexecdir}/%{name}
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.hyprland.service
%{_datadir}/xdg-desktop-portal/portals/hyprland.portal
%{_userunitdir}/%{name}.service

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 1.3.12-1
- Package the official 1.3.12 release
- Require system sdbus-cpp and hyprland-protocols with no fallbacks
- Install the portal, D-Bus, systemd, and Qt share-picker integration
