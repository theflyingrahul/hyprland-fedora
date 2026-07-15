%global upstream_commit 6f68a726531b53d87c6dd6ce474face27dde02ff

Name:           hyprsysteminfo
Version:        0.2.0
Release:        1%{?dist}
Summary:        Graphical system information utility for Hyprland

License:        BSD-3-Clause AND CC0-1.0
URL:            https://github.com/hyprwm/hyprsysteminfo
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        com.github.hyprwm.%{name}.metainfo.xml
Patch0:         0001-cmake-use-system-glaze-flags-and-desktop-metadata.patch

ExcludeArch:    %{ix86}

BuildRequires:  appstream
BuildRequires:  cmake >= 3.19
BuildRequires:  cmake(glaze) >= 6.1.0
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(aquamarine) >= 0.10.0
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(hyprgraphics) >= 0.3.0
BuildRequires:  pkgconfig(hyprtoolkit) >= 0.4.0
BuildRequires:  pkgconfig(hyprutils) >= 0.10.2
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpci)
BuildRequires:  pkgconfig(pixman-1)

Recommends:     hyprland
Recommends:     wl-clipboard

%description
Hyprsysteminfo displays operating-system, hardware, graphics, desktop, and
running Hyprland details in a native graphical interface.

%prep
%autosetup -p1

%build
%cmake \
    -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
    -DFETCHCONTENT_UPDATES_DISCONNECTED=ON
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
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.2.0-1
- Initial Fedora package for the official 0.2.0 release
- Add AppStream and desktop metadata and require packaged Glaze
