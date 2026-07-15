%global upstream_commit 2ce8f3d174f2ae1c50c7dcc182d809a5ab33cad2

Name:           hyprpwcenter
Version:        0.1.2
Release:        1%{?dist}
Summary:        Graphical PipeWire control center for Hyprland

License:        BSD-3-Clause AND CC0-1.0
URL:            https://github.com/hyprwm/hyprpwcenter
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        com.github.hyprwm.%{name}.metainfo.xml
Patch0:         0001-cmake-preserve-distribution-compiler-flags.patch

ExcludeArch:    %{ix86}

BuildRequires:  appstream
BuildRequires:  cmake >= 3.19
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(aquamarine) >= 0.10.0
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(hyprgraphics) >= 0.3.0
BuildRequires:  pkgconfig(hyprtoolkit) >= 0.4.0
BuildRequires:  pkgconfig(hyprutils) >= 0.10.2
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(pixman-1)

Requires:       pipewire

%description
Hyprpwcenter is a graphical PipeWire control center for viewing and
adjusting devices, streams, volumes, and audio routing.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install
install -Dpm 0644 %{SOURCE1} \
    %{buildroot}%{_metainfodir}/com.github.hyprwm.%{name}.metainfo.xml

%check
desktop-file-validate \
    %{buildroot}%{_datadir}/applications/%{name}.desktop
appstreamcli validate --no-net \
    %{buildroot}%{_metainfodir}/com.github.hyprwm.%{name}.metainfo.xml

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_metainfodir}/com.github.hyprwm.%{name}.metainfo.xml

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.1.2-1
- Initial Fedora package for the official 0.1.2 release
- Add AppStream metadata and preserve Fedora compiler flags
