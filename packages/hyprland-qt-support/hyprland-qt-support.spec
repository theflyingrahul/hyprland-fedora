%global upstream_commit 9d4437011b4f02e60e98a3e36c7fa14bb053b502

Name:           hyprland-qt-support
Version:        0.1.0
Release:        2%{?dist}
Summary:        Hyprland Qt Quick Controls style provider

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-qt-support
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-cmake-install-runtime-libraries-in-libdir.patch
Patch1:         0002-cmake-version-qml-backing-libraries.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake >= 3.20
BuildRequires:  cmake(Qt6Qml) >= 6.6
BuildRequires:  cmake(Qt6Quick) >= 6.6
BuildRequires:  cmake(Qt6QuickControls2) >= 6.6
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(hyprlang) >= 0.6.0

Requires:       qt6qml(QtQuick)
Requires:       qt6qml(QtQuick.Controls.Basic)

%description
Hyprland-qt-support provides the org.hyprland.style Qt Quick Controls style
and its implementation module for Hyprland Qt and QML applications.

%prep
%autosetup -p1

%build
%cmake \
    -DBUILD_TESTER=ON \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DINSTALL_QMLDIR=%{_qt6_qmldir}
%cmake_build

%install
%cmake_install
rm %{buildroot}%{_libdir}/libhyprland-quick-style.so
rm %{buildroot}%{_libdir}/libhyprland-quick-style-impl.so

%check
test -x %{_vpath_builddir}/src/style/test/style-test
test -f %{buildroot}%{_qt6_qmldir}/org/hyprland/style/qmldir
test -f %{buildroot}%{_qt6_qmldir}/org/hyprland/style/impl/qmldir

%files
%license LICENSE
%doc README.md
%{_libdir}/libhyprland-quick-style.so.0
%{_libdir}/libhyprland-quick-style.so.%{version}
%{_libdir}/libhyprland-quick-style-impl.so.0
%{_libdir}/libhyprland-quick-style-impl.so.%{version}
%{_qt6_qmldir}/org/hyprland/style/

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.1.0-2
- Install QML backing libraries in the Fedora libdir with versioned SONAMEs

* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.1.0-1
- Initial Fedora package for the official 0.1.0 release
- Install the complete QML style and implementation modules
