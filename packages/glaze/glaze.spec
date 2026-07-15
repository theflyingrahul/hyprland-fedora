%global debug_package %{nil}

Name:           glaze
Version:        7.2.0
Release:        1%{?dist}
Summary:        High-performance JSON and data serialization library for C++

License:        MIT
URL:            https://github.com/stephenberry/glaze
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build

%description
Glaze is a high-performance, standards-focused C++ library for JSON and
related data formats.

%package devel
Summary:        Header files and CMake metadata for Glaze
BuildArch:      noarch
Provides:       %{name} = %{version}-%{release}

%description devel
This package contains the header-only Glaze library and its CMake package
configuration.

%prep
%autosetup

%build
%cmake \
    -Dglaze_DEVELOPER_MODE=OFF \
    -Dglaze_ENABLE_FUZZING=OFF \
    -Dglaze_BUILD_EXAMPLES=OFF \
    -DBUILD_TESTING=OFF \
    -Dglaze_INSTALL_CMAKEDIR=%{_datadir}/cmake/glaze
%cmake_build

%install
%cmake_install

%check
cat > %{_vpath_builddir}/include-test.cpp <<'EOF'
#include <glaze/glaze.hpp>

int main() {
    return 0;
}
EOF
%{__cxx} %{build_cxxflags} -std=c++23 -Iinclude \
    %{_vpath_builddir}/include-test.cpp -o %{_vpath_builddir}/include-test
%{_vpath_builddir}/include-test

%files devel
%license LICENSE
%doc README.md
%{_includedir}/glaze/
%{_datadir}/cmake/glaze/

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 7.2.0-1
- Initial Fedora 44 package
