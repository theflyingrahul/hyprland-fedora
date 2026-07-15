Name:           hyprlang
Version:        0.6.8
Release:        1%{?dist}
Summary:        Official parser for the Hypr configuration language

License:        LGPL-3.0-only
URL:            https://github.com/hyprwm/hyprlang
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-cmake-use-fedora-optimization-flags.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(hyprutils) >= 0.7.1

%description
Hyprlang implements the configuration language used by Hyprland and other
Hypr ecosystem projects.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header and pkg-config metadata for developing software against hyprlang.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE COPYRIGHT
%doc README.md
%{_libdir}/lib%{name}.so.2
%{_libdir}/lib%{name}.so.%{version}

%files devel
%{_includedir}/hyprlang.hpp
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.6.8-1
- Update the official Fedora package to upstream 0.6.8
- Use Fedora optimization flags
