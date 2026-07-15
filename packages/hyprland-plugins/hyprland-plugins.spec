%global _lto_cflags %{nil}
%global commit 3aa21f2e0ca72412f1b434c3126f8f1fec3c716c
%global shortcommit 3aa21f2
%global hyprland_evr 0.55.4-3%{?dist}

Name:           hyprland-plugins
Version:        0.55.0^20260512git3aa21f2
Release:        1%{?dist}
Summary:        Official plugins for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-plugins
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
Patch0:         0001-cmake-use-gnu-install-dirs.patch

ExcludeArch:    %{ix86}

BuildRequires:  binutils
BuildRequires:  cmake >= 3.27
BuildRequires:  gcc-c++
BuildRequires:  glslang-devel
BuildRequires:  hyprland-devel%{?_isa} = %{hyprland_evr}
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(hyprland) = 0.55.4
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(xkbcommon)
Requires:       hyprland-plugin-borders-plus-plus%{?_isa} = %{version}-%{release}
Requires:       hyprland-plugin-csgo-vulkan-fix%{?_isa} = %{version}-%{release}
Requires:       hyprland-plugin-hyprbars%{?_isa} = %{version}-%{release}
Requires:       hyprland-plugin-hyprfocus%{?_isa} = %{version}-%{release}

%description
Installs every official plugin selected by upstream for the exact packaged
Hyprland 0.55.4 ABI.

%package -n hyprland-plugin-borders-plus-plus
Summary:        Additional window borders for Hyprland
Requires:       hyprland%{?_isa} = %{hyprland_evr}
Requires:       hyprland-plugin-api = %{hyprland_evr}

%description -n hyprland-plugin-borders-plus-plus
Adds configurable additional borders to Hyprland windows.

%package -n hyprland-plugin-csgo-vulkan-fix
Summary:        Vulkan mouse-offset correction plugin for Hyprland
Requires:       hyprland%{?_isa} = %{hyprland_evr}
Requires:       hyprland-plugin-api = %{hyprland_evr}

%description -n hyprland-plugin-csgo-vulkan-fix
Corrects mouse offsets for custom-resolution Vulkan applications in Hyprland.

%package -n hyprland-plugin-hyprbars
Summary:        Window title bars for Hyprland
Requires:       hyprland%{?_isa} = %{hyprland_evr}
Requires:       hyprland-plugin-api = %{hyprland_evr}

%description -n hyprland-plugin-hyprbars
Adds configurable title bars to Hyprland windows.

%package -n hyprland-plugin-hyprfocus
Summary:        Focus-change animation plugin for Hyprland
Requires:       hyprland%{?_isa} = %{hyprland_evr}
Requires:       hyprland-plugin-api = %{hyprland_evr}

%description -n hyprland-plugin-hyprfocus
Provides flash-focus visual feedback when Hyprland changes window focus.

%prep
%autosetup -n %{name}-%{commit}

%build
%cmake
%cmake_build

%install
%cmake_install
install -d %{buildroot}%{_libdir}/hyprland/plugins
for plugin in borders-plus-plus csgo-vulkan-fix hyprbars hyprfocus; do
    mv "%{buildroot}%{_libdir}/lib${plugin}.so" \
        "%{buildroot}%{_libdir}/hyprland/plugins/${plugin}.so"
done

%check
for plugin in %{buildroot}%{_libdir}/hyprland/plugins/*.so; do
    ! readelf -d "$plugin" | grep -q TEXTREL
    ! ldd "$plugin" | grep -q 'not found'
done

%files -n hyprland-plugin-borders-plus-plus
%license LICENSE
%doc borders-plus-plus/README.md
%{_libdir}/hyprland/plugins/borders-plus-plus.so

%files -n hyprland-plugin-csgo-vulkan-fix
%license LICENSE
%doc csgo-vulkan-fix/README.md
%{_libdir}/hyprland/plugins/csgo-vulkan-fix.so

%files -n hyprland-plugin-hyprbars
%license LICENSE
%doc hyprbars/README.md
%{_libdir}/hyprland/plugins/hyprbars.so

%files -n hyprland-plugin-hyprfocus
%license LICENSE
%doc hyprfocus/README.md
%{_libdir}/hyprland/plugins/hyprfocus.so

%files
%license LICENSE
%doc README.md

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.55.0^20260512git3aa21f2-1
- Package the exact official plugin commit selected for Hyprland 0.55.4
- Split each plugin and enforce exact compositor ABI requirements
