%global upstream_commit c682906a0836447c27c8d974f35493d3baa79d64

Name:           hyprlauncher
Version:        0.1.6
Release:        1%{?dist}
Summary:        Multipurpose launcher and picker for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprlauncher
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-cmake-preserve-distribution-compiler-flags.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake >= 3.19
BuildRequires:  cmake(hyprwayland-scanner) >= 0.4.0
BuildRequires:  cmake(hyprwire-scanner) >= 0.3.1
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(aquamarine) >= 0.10.0
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(hyprgraphics) >= 0.3.0
BuildRequires:  pkgconfig(hyprlang) >= 0.6.0
BuildRequires:  pkgconfig(hyprtoolkit) >= 0.4.0
BuildRequires:  pkgconfig(hyprutils) >= 0.10.2
BuildRequires:  pkgconfig(hyprwire) >= 0.3.1
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libqalculate)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)

%description
Hyprlauncher is a native Hyprland launcher and picker with desktop
application, font, Unicode, calculator, and explicit-option finders.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%check
test "$(%{_vpath_builddir}/%{name} --version)" = \
    "Hyprlauncher v%{version}"

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.1.6-1
- Initial Fedora package for the official 0.1.6 release
- Preserve Fedora compiler optimization and hardening flags
