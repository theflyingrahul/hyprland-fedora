Name:           hyprtoolkit
Version:        0.5.4
Release:        1%{?dist}
Summary:        Modern C++ Wayland-native GUI toolkit

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprtoolkit
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-cmake-use-fedora-flags-and-system-dependencies.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  cmake(GTest)
BuildRequires:  cmake(hyprwayland-scanner) >= 0.4.0
BuildRequires:  gcc-c++
BuildRequires:  libglvnd-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(aquamarine) >= 0.10.0
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(hyprgraphics) >= 0.3.0
BuildRequires:  pkgconfig(hyprlang) >= 0.6.0
BuildRequires:  pkgconfig(hyprutils) >= 0.11.0
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)

Requires:       aquamarine%{?_isa} >= 0.10.0
Requires:       hyprgraphics%{?_isa} >= 0.3.0
Requires:       hyprlang%{?_isa} >= 0.6.0
Requires:       hyprutils%{?_isa} >= 0.11.0

%description
Hyprtoolkit is a modern C++ GUI toolkit for Wayland-native applications in
the Hypr ecosystem.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config metadata for developing software against hyprtoolkit.

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
%{_libdir}/lib%{name}.so.5
%{_libdir}/lib%{name}.so.%{version}

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.5.4-1
- Initial Fedora package
