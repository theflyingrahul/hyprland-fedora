%global upstream_commit e8a694d5fc7813cf477f426dce731967e4cf670b

Name:           hyprqt6engine
Version:        0.1.0
Release:        3%{?dist}
Summary:        Hyprland Qt 6 platform theme and widget style

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprqt6engine
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-cmake-use-complete-system-Qt-and-KF6-dependencies.patch
Patch1:         0002-cmake-find-Qt-private-packages.patch
Patch2:         0003-cmake-version-common-library.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake >= 3.16
BuildRequires:  cmake(KF6ColorScheme)
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6IconThemes)
BuildRequires:  cmake(Qt6BuildInternals) >= 6.9
BuildRequires:  cmake(Qt6GuiPrivate) >= 6.9
BuildRequires:  cmake(Qt6QuickControls2) >= 6.9
BuildRequires:  cmake(Qt6Widgets) >= 6.9
BuildRequires:  cmake(Qt6WidgetsPrivate) >= 6.9
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)

Requires:       qt6-qtbase-gui%{?_isa} = %{_qt6_evr}

%description
Hyprqt6engine provides a Qt 6 platform theme and widget style that follow
Hyprland configuration, colors, fonts, and icon settings.

%prep
%autosetup -p1

%build
%cmake \
    -DPLUGINDIR=%{_qt6_plugindir}
%cmake_build

%install
%cmake_install
rm %{buildroot}%{_libdir}/libhyprqt6engine-common.so

%check
test -f %{buildroot}%{_qt6_plugindir}/platformthemes/libhyprqt6engine.so
test -f %{buildroot}%{_qt6_plugindir}/styles/libhypr-style.so
test -f %{buildroot}%{_libdir}/libhyprqt6engine-common.so.0

%files
%license LICENSE
%doc README.md
%{_libdir}/libhyprqt6engine-common.so.0
%{_libdir}/libhyprqt6engine-common.so.%{version}
%{_qt6_plugindir}/platformthemes/libhyprqt6engine.so
%{_qt6_plugindir}/styles/libhypr-style.so

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.1.0-3
- Require the exact Qt runtime used by private Qt headers

* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.1.0-2
- Give the common runtime library a versioned SONAME

* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.1.0-1
- Initial Fedora package for the official 0.1.0 release
- Enable complete system Qt 6 and KDE Frameworks integration
