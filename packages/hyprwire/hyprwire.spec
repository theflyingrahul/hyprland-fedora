Name:           hyprwire
Version:        0.3.1
Release:        1%{?dist}
Summary:        Fast wire protocol library for IPC

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprwire
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-build-use-fedora-flags-and-fix-metadata.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  cmake(GTest)
BuildRequires:  gcc-c++
BuildRequires:  libasan
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(hyprutils) >= 0.9.0
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(pugixml)

%description
Hyprwire provides a strict, fast wire protocol and C++ implementation for
inter-process communication.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config metadata for developing software against hyprwire.

%package scanner-devel
Summary:        Protocol code generator for %{name}

%description scanner-devel
Hyprwire Scanner generates C++ client and server bindings from hyprwire
protocol XML files. This package includes the executable plus pkg-config and
CMake build-system metadata.

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc README.md
%{_libdir}/lib%{name}.so.3
%{_libdir}/lib%{name}.so.%{version}

%files devel
%license LICENSE
%doc docs/WIRE.md
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files scanner-devel
%license LICENSE
%{_bindir}/%{name}-scanner
%{_libdir}/pkgconfig/%{name}-scanner.pc
%{_libdir}/cmake/%{name}-scanner/

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.3.1-1
- Initial Fedora package
