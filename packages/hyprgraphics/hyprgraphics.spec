Name:           hyprgraphics
Version:        0.5.1
Release:        1%{?dist}
Summary:        Graphics and resource utility library for the Hypr ecosystem

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprgraphics
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         https://github.com/hyprwm/hyprgraphics/commit/3b41722bc01e7b56b0c2bda5f9f819793bdf1596.patch
Patch1:         https://github.com/hyprwm/hyprgraphics/commit/090db94649f25b476918f8afcfd443c02cc0a4b9.patch
Patch2:         0001-cmake-use-fedora-flags-and-require-codecs.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libheif)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libjxl)
BuildRequires:  pkgconfig(libjxl_cms)
BuildRequires:  pkgconfig(libjxl_threads)
BuildRequires:  pkgconfig(libmagic)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)

%description
Hyprgraphics provides graphics, image decoding, color, and asynchronous
resource helpers shared by Hypr ecosystem applications.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config metadata for developing software against hyprgraphics.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc README.md
%{_libdir}/lib%{name}.so.4
%{_libdir}/lib%{name}.so.%{version}

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 0.5.1-1
- Update the official Fedora package to upstream 0.5.1
- Backport upstream pkg-config dependency fixes
- Build deterministic JPEG XL and HEIF/AVIF support
