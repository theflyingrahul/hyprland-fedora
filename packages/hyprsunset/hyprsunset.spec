%global upstream_commit 25f704346ec22e7623b0873ef8c4573b57ca1512

Name:           hyprsunset
Version:        0.4.0
Release:        1%{?dist}
Summary:        Blue-light filter for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprsunset
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-cmake-use-release-vcs-metadata.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake >= 3.12
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(hyprland-protocols) >= 0.6.2
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils) >= 0.2.3
BuildRequires:  pkgconfig(hyprwayland-scanner) >= 0.4.0
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)

Supplements:    hyprland

%description
Hyprsunset controls Hyprland's color transformation matrix to adjust display
color temperature and gamma manually or on a configured schedule.

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
test "$(%{_vpath_builddir}/hyprsunset --version)" = "hyprsunset v%{version}"

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
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.4.0-1
- Package the official 0.4.0 release
- Install the systemd user service and deterministic release metadata
