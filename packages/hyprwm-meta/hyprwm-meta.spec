Name:           hyprwm-meta
Version:        1
Release:        4%{?dist}
Summary:        Complete supported HyprWM package set

License:        MIT
Source0:        LICENSE
BuildArch:      noarch

Requires:       hyprwm-complete = %{version}-%{release}

%description
Convenience meta package that installs the complete supported HyprWM
application set.

%package -n hyprland-desktop
Summary:        Supported Hyprland desktop baseline
Requires:       hypridle = 0.1.7-1%{?dist}
Requires:       hyprland = 0.55.4-3%{?dist}
Requires:       hyprland-backgrounds = 0.55.4-3%{?dist}
Requires:       hyprlock = 0.9.5-1%{?dist}
Requires:       hyprpaper = 0.8.4-1%{?dist}
Requires:       hyprpolkitagent = 0.1.3-1%{?dist}
Requires:       hyprsunset = 0.4.0-1%{?dist}
Requires:       xdg-desktop-portal-hyprland = 1.3.12-1%{?dist}
Requires:       xorg-x11-server-Xwayland

%description -n hyprland-desktop
Installs the compositor, portal, wallpaper, idle and lock services, color
temperature control, authentication agent, backgrounds, and XWayland.

%package -n hyprwm-complete
Summary:        Complete stable HyprWM application set
Requires:       hyprland-desktop = %{version}-%{release}
Requires:       hyprland-guiutils = 0.2.1-1%{?dist}
Requires:       hyprland-qt-support = 0.1.0-2%{?dist}
Requires:       hyprlauncher = 0.1.6-1%{?dist}
Requires:       hyprpicker = 0.4.7-1%{?dist}
Requires:       hyprpwcenter = 0.1.2-1%{?dist}
Requires:       hyprqt6engine = 0.1.0-3%{?dist}
Requires:       hyprshutdown = 0.1.1-1%{?dist}
Requires:       hyprsysteminfo = 0.2.0-1%{?dist}

%description -n hyprwm-complete
Adds every stable optional HyprWM application to the supported Hyprland
desktop baseline.

%prep
%setup -q -c -T
cp -p %{SOURCE0} LICENSE

%build

%install

%files
%license LICENSE

%files -n hyprland-desktop
%license LICENSE

%files -n hyprwm-complete
%license LICENSE

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 1-4
- Update the locked Hyprland requirement to 0.55.4-3

* Wed Jul 15 2026 Rahul <rahul@localhost> - 1-3
- Update the locked hyprqt6engine requirement to 0.1.0-3

* Wed Jul 15 2026 Rahul <rahul@localhost> - 1-2
- Update the locked Hyprland requirement to 0.55.4-2

* Wed Jul 15 2026 Rahul <rahul@localhost> - 1-1
- Define the supported desktop and complete HyprWM installation sets
