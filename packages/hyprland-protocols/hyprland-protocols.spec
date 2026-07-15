Name:           hyprland-protocols
Version:        0.7.0
Release:        1%{?dist}
Summary:        Wayland protocol extensions for Hyprland
BuildArch:      noarch

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-protocols
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  libxml2
BuildRequires:  meson

%description
Hyprland-specific Wayland protocol XML definitions.

%package devel
Summary:        Build-time Hyprland protocol definitions

%description devel
Protocol XML and pkg-config metadata used to generate Hyprland protocol
bindings while building compositors and clients.

%prep
%autosetup

%build
%meson
%meson_build

%install
%meson_install

%check
for protocol in protocols/*.xml; do
    xmllint --noout "${protocol}"
done
test "$(PKG_CONFIG_PATH=%{_vpath_builddir} \
    pkg-config --modversion %{name})" = "%{version}"

%files devel
%license LICENSE
%doc README.md
%{_datadir}/pkgconfig/%{name}.pc
%{_datadir}/%{name}/

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.7.0-1
- Update the official Fedora package to upstream 0.7.0
- Validate every protocol XML file during the build
