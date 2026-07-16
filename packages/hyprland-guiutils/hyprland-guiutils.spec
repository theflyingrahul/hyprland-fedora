%global upstream_commit c2e906261142f5dd1ee0bfc44abba23e2754c660

Name:           hyprland-guiutils
Version:        0.2.1
Release:        2%{?dist}
Summary:        Native graphical utilities for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-guiutils
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-cmake-accept-release-metadata-without-git.patch
Patch1:         0002-welcome-detect-libexec-components.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake >= 3.12
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(aquamarine) >= 0.10.0
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(hyprgraphics) >= 0.3.0
BuildRequires:  pkgconfig(hyprlang) >= 0.6.0
BuildRequires:  pkgconfig(hyprtoolkit) >= 0.4.0
BuildRequires:  pkgconfig(hyprutils) >= 0.10.2
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(xkbcommon)

Requires:       xdg-utils

%description
Hyprland-guiutils supplies the Hyprland dialog, run prompt, update screen,
donation screen, and first-run welcome application.

%prep
%autosetup -p1

%build
%cmake \
    -DGIT_COMMIT_HASH=%{upstream_commit} \
    -DGIT_BRANCH=v%{version} \
    -DGIT_COMMIT_MESSAGE="Release v%{version}" \
    -DGIT_DIRTY=
%cmake_build

%install
%cmake_install

%check
for executable in \
    hyprland-dialog \
    hyprland-donate-screen \
    hyprland-run \
    hyprland-update-screen \
    hyprland-welcome
do
    test -x "%{_vpath_builddir}/utils/${executable#hyprland-}/$executable" || \
        find %{_vpath_builddir} -type f -name "$executable" -perm /111 | grep -q .
done
grep -aFq '%{_libexecdir}' \
    %{_vpath_builddir}/utils/welcome/hyprland-welcome
%{_vpath_builddir}/utils/welcome/hyprland-welcome --check-app cmake

%files
%license LICENSE
%doc README.md
%{_bindir}/hyprland-dialog
%{_bindir}/hyprland-donate-screen
%{_bindir}/hyprland-run
%{_bindir}/hyprland-update-screen
%{_bindir}/hyprland-welcome

%changelog
* Thu Jul 16 2026 Rahul <rahul@localhost> - 0.2.1-2
- Detect packaged portal and polkit components installed in Fedora libexec

* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.2.1-1
- Initial Fedora package for the official 0.2.1 release
- Embed deterministic official tag metadata in release-archive builds
