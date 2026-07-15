Name:           hyprcursor
Version:        0.1.13
Release:        1%{?dist}
Summary:        Hypr cursor format library and utilities

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprcursor
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        HyprBibataModernClassicSVG.tar.gz
Patch0:         0001-cmake-use-fedora-flags-and-fix-pkgconfig.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(hyprlang) >= 0.4.2
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(tomlplusplus)

%description
Hyprcursor provides the Hypr cursor format runtime library and a conversion
utility.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config metadata for developing software against hyprcursor.

%prep
%autosetup -p1 -a1
mkdir -p "$HOME/.icons"
mv HyprBibataModernClassicSVG "$HOME/.icons/"

%build
%cmake -DINSTALL_TESTS=OFF
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc README.md
%{_bindir}/hyprcursor-util
%{_libdir}/lib%{name}.so.0
%{_libdir}/lib%{name}.so.%{version}

%files devel
%{_includedir}/hyprcursor.hpp
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.1.13-1
- Update the official Fedora package to upstream 0.1.13
- Use Fedora optimization flags and advertise Cairo headers via pkg-config
