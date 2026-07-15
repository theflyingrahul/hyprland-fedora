Name:           aquamarine
Version:        0.12.1
Release:        1%{?dist}
Summary:        Lightweight Linux rendering backend library

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/aquamarine
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-build-use-fedora-flags-and-fix-pkgconfig.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  cmake(hyprwayland-scanner) >= 0.4.0
BuildRequires:  gcc-c++
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(hyprutils) >= 0.8.0
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput) >= 1.26.0
BuildRequires:  pkgconfig(libseat) >= 0.8.0
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)

%description
Aquamarine provides DRM, KMS, Wayland, input, allocation, and output backend
abstractions used by Hyprland and Hypr toolkit applications.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config metadata for developing software against aquamarine.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%check
# The simpleWindow test requires a running Wayland compositor. The attachment
# test is hardware- and display-independent.
%ctest -R attachments

%files
%license LICENSE
%doc README.md docs/env.md
%{_libdir}/lib%{name}.so.11
%{_libdir}/lib%{name}.so.%{version}

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.12.1-1
- Update the retired official Fedora package to upstream 0.12.1
- Update the runtime file list for SOVERSION 11
- Fix public pkg-config dependencies
