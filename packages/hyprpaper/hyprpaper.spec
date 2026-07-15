%global upstream_commit 20fc0fa6c2056c388a4cd69cb394a9f989dd27c0

Name:           hyprpaper
Version:        0.8.4
Release:        1%{?dist}
Summary:        Wallpaper utility for Hyprland with IPC controls

# The bundled wlr-layer-shell protocol XML is HPND-sell-variant.
License:        BSD-3-Clause AND HPND-sell-variant
URL:            https://github.com/hyprwm/hyprpaper
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-cmake-use-release-vcs-metadata.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake >= 3.12
BuildRequires:  cmake(hyprwayland-scanner) >= 0.4.0
BuildRequires:  cmake(hyprwire-scanner)
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hyprlang) >= 0.6.0
BuildRequires:  pkgconfig(hyprtoolkit) >= 0.4.1
BuildRequires:  pkgconfig(hyprutils) >= 0.2.4
BuildRequires:  pkgconfig(hyprwire)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libmagic)
BuildRequires:  pkgconfig(opengl)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)

%description
Hyprpaper is a fast Wayland wallpaper utility for Hyprland. It supports
runtime wallpaper changes through its IPC interface.

%prep
%autosetup -p1

%build
%cmake \
    -DGIT_BRANCH=v%{version} \
    -DGIT_COMMIT_HASH=%{upstream_commit} \
    -DGIT_COMMIT_MESSAGE="Release v%{version}" \
    -DGIT_DIRTY=
%cmake_build

%install
%cmake_install

%check
test "$(%{_vpath_builddir}/hyprpaper --version)" = "hyprpaper v%{version}"
grep -aqF '%{upstream_commit}' %{_vpath_builddir}/hyprpaper

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun_with_restart %{name}.service

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_userunitdir}/%{name}.service

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.8.4-1
- Package the official 0.8.4 release with reproducible VCS metadata
- Install and manage the upstream systemd user service
