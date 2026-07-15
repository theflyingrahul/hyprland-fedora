%global upstream_commit 7e4054410f6d6331b239fea1c659ad6a917fbf6a

Name:           hyprpolkitagent
Version:        0.1.3
Release:        1%{?dist}
Summary:        Polkit authentication agent for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprpolkitagent
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

ExcludeArch:    %{ix86}

BuildRequires:  cmake >= 3.16
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  systemd-rpm-macros
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6QuickControls2)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(polkit-qt6-1)

Requires:       hyprland-qt-support%{?_isa} >= 0.1.0
Requires:       polkit
Requires:       qt6-qtwayland%{?_isa}
Requires:       qt6qml(QtQuick)
Requires:       qt6qml(QtQuick.Controls)
Requires:       qt6qml(QtQuick.Layouts)
Recommends:     qt6-qtsvg%{?_isa}

%description
Hyprpolkitagent is the Hyprland project's Qt and QML authentication agent
for PolicyKit. It supports D-Bus activation and a systemd user service.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%check
test -x %{buildroot}%{_libexecdir}/%{name}
grep -Fx 'ExecStart=%{_libexecdir}/%{name}' \
    %{buildroot}%{_userunitdir}/%{name}.service
grep -Fx 'Exec=%{_libexecdir}/%{name}' \
    %{buildroot}%{_datadir}/dbus-1/services/org.hyprland.%{name}.service

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun_with_restart %{name}.service

%files
%license LICENSE
%doc README.md
%{_libexecdir}/%{name}
%{_userunitdir}/%{name}.service
%{_datadir}/dbus-1/services/org.hyprland.%{name}.service

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.1.3-1
- Initial Fedora package for the official 0.1.3 release
