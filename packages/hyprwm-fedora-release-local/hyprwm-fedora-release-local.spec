Name:           hyprwm-fedora-release-local
Version:        44
Release:        2%{?dist}
Summary:        Local HyprWM Fedora repository configuration

License:        MIT
Source0:        LICENSE
Source1:        hyprwm-fedora.repo
BuildArch:      noarch

%description
Installs the DNF configuration for an unsigned local HyprWM Fedora 44
repository published below the system service-data directory. Signed public
snapshots distribute a separate generated configuration with signature
verification enabled.

%prep
%setup -q -c -T
cp -p %{SOURCE0} LICENSE

%build

%install
install -Dpm 0644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/yum.repos.d/hyprwm-fedora.repo

%check
grep -Fx 'baseurl=file:///srv/hyprwm-fedora/fedora/44/current/$basearch/' \
    %{buildroot}%{_sysconfdir}/yum.repos.d/hyprwm-fedora.repo

%files
%license LICENSE
%config(noreplace) %{_sysconfdir}/yum.repos.d/hyprwm-fedora.repo

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 44-2
- Validate the installed repository configuration during the build

* Wed Jul 15 2026 Rahul <rahul@localhost> - 44-1
- Add the Fedora 44 local repository bootstrap configuration
