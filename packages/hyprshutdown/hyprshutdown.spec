%global upstream_commit db1f38b03b173984ae9ed3abeb9750583c9bbd91

Name:           hyprshutdown
Version:        0.1.1
Release:        1%{?dist}
Summary:        Graceful shutdown utility for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprshutdown
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-cmake-require-system-glaze-and-preserve-flags.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake >= 3.19
BuildRequires:  cmake(glaze) >= 6.1.0
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(aquamarine) >= 0.10.0
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(hyprgraphics) >= 0.3.0
BuildRequires:  pkgconfig(hyprtoolkit) >= 0.4.0
BuildRequires:  pkgconfig(hyprutils) >= 0.11.0
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pixman-1)

Requires:       hyprland
Suggests:       kbd
Suggests:       sudo

%description
Hyprshutdown presents a native shutdown progress interface, closes client
applications, and exits Hyprland gracefully.

%prep
%autosetup -p1

%build
%cmake \
    -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
    -DFETCHCONTENT_UPDATES_DISCONNECTED=ON
%cmake_build

%install
%cmake_install

%check
%{_vpath_builddir}/%{name} --help | \
    grep -F "hyprshutdown v%{version}"

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.1.1-1
- Initial Fedora package for the official 0.1.1 release
- Require packaged Glaze and preserve Fedora compiler flags
