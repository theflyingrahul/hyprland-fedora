Name:           hyprutils
Version:        0.13.1
Release:        1%{?dist}
Summary:        Utility library shared by Hypr ecosystem projects

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprutils
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-cmake-respect-fedora-flags-and-test-selection.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  cmake(GTest)
BuildRequires:  gcc-c++
BuildRequires:  libasan
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(pixman-1)

%description
Hyprutils provides common C++ utility types and helpers used across the Hypr
ecosystem.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config metadata for developing software against hyprutils.

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
%{_libdir}/lib%{name}.so.12
%{_libdir}/lib%{name}.so.%{version}

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.13.1-1
- Update the official Fedora package to upstream 0.13.1
- Preserve Fedora build flags and run the upstream test suite
