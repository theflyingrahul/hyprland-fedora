Name:           hyprwayland-scanner
Version:        0.4.6
Release:        1%{?dist}
Summary:        C++ Wayland protocol scanner for the Hypr ecosystem

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprwayland-scanner
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-cmake-use-fedora-optimization-flags.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(pugixml)

%description
Hyprwayland-scanner generates modern C++ client and server bindings from
Wayland protocol XML.

%package devel
Summary:        Hypr Wayland protocol scanner and build-system metadata

%description devel
This package contains the scanner executable, pkg-config metadata, and CMake
package used while building Hyprland and other Hypr projects.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%check
test "$(%{_vpath_builddir}/%{name} --version)" = "%{version}"

%files devel
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.4.6-1
- Update the official Fedora package to upstream 0.4.6
- Use Fedora optimization flags
