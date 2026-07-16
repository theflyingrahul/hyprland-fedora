Name:           hyprwm-meta
Version:        1
Release:        5%{?dist}
Summary:        Complete supported HyprWM package set

License:        MIT
Source0:        LICENSE
BuildArch:      noarch

Requires:       hyprwm-complete = %{version}-%{release}

%description
Convenience meta package that installs the maximal supported Hyprland
environment.

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
Summary:        Maximal ready-to-use Hyprland environment
Requires:       hyprland-desktop = %{version}-%{release}
Requires:       hyprland-guiutils = 0.2.1-2%{?dist}
Requires:       hyprland-qt-support = 0.1.0-2%{?dist}
Requires:       hyprland-plugins = 0.55.0^20260512git3aa21f2-1%{?dist}
Requires:       hyprlauncher = 0.1.6-1%{?dist}
Requires:       hyprpicker = 0.4.7-1%{?dist}
Requires:       hyprpwcenter = 0.1.2-1%{?dist}
Requires:       hyprqt6engine = 0.1.0-3%{?dist}
Requires:       hyprshutdown = 0.1.1-1%{?dist}
Requires:       hyprsysteminfo = 0.2.0-1%{?dist}
Requires:       cliphist
Requires:       dolphin
Requires:       fontawesome-6-free-fonts
Requires:       google-noto-sans-fonts
Requires:       grim
Requires:       kitty
Requires:       lxappearance
Requires:       mako
Requires:       pipewire
Requires:       qt5-qtwayland
Requires:       qt6-qtwayland
Requires:       slurp
Requires:       waybar
Requires:       wireplumber
Requires:       wl-clipboard
Requires:       xdg-desktop-portal-gtk

%description -n hyprwm-complete
Installs the maximal supported Hyprland environment: every stable HyprWM
application, the exact official plugin set, and concrete Fedora desktop
utilities for terminal, files, notifications, status bar, media, native
Wayland toolkits, fonts, GTK theme configuration, screenshots, clipboard, and
fallback portal interfaces.

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
* Thu Jul 16 2026 Rahul <rahul@localhost> - 1-5
- Make the complete set a ready-to-use maximal Hyprland environment
- Add official plugins and Fedora desktop utilities required by the welcome app
- Include wiki-recommended Wayland, font, screenshot, clipboard, and theme tools

* Wed Jul 15 2026 Rahul <rahul@localhost> - 1-4
- Update the locked Hyprland requirement to 0.55.4-3

* Wed Jul 15 2026 Rahul <rahul@localhost> - 1-3
- Update the locked hyprqt6engine requirement to 0.1.0-3

* Wed Jul 15 2026 Rahul <rahul@localhost> - 1-2
- Update the locked Hyprland requirement to 0.55.4-2

* Wed Jul 15 2026 Rahul <rahul@localhost> - 1-1
- Define the supported desktop and complete HyprWM installation sets
