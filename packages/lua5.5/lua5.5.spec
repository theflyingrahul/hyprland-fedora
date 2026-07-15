%global lua_version 5.5
%global lua_soversion 5.5

Name:           lua5.5
Version:        5.5.0
Release:        1%{?dist}
Summary:        Parallel-installable Lua 5.5 interpreter and libraries

License:        MIT
URL:            https://www.lua.org/
Source0:        https://www.lua.org/ftp/lua-%{version}.tar.gz
Source1:        https://www.lua.org/tests/lua-%{version}-tests.tar.gz
Source2:        mit.txt
Patch0:         https://src.fedoraproject.org/rpms/lua/raw/e658e44a5ef9c611b9f4d006599a792874ab6555/f/lua-5.5.0-bug1.patch
Patch1:         https://src.fedoraproject.org/rpms/lua/raw/e658e44a5ef9c611b9f4d006599a792874ab6555/f/lua-5.5.0-bug2.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  readline-devel

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
Lua is a powerful, efficient, lightweight, embeddable scripting language.
This package provides Lua 5.5 in versioned paths so it can coexist with
Fedora 44's system Lua 5.4.

%package libs
Summary:        Runtime library for Lua 5.5
Provides:       lua(abi) = %{lua_version}

%description libs
This package contains the shared Lua 5.5 runtime library and versioned module
directories.

%package devel
Summary:        Development files for Lua 5.5
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains Lua 5.5 headers, the development linker file, and
versioned pkg-config modules. It is parallel-installable with Fedora's
lua-devel package.

%package doc
Summary:        Documentation for Lua 5.5
BuildArch:      noarch

%description doc
This package contains the Lua 5.5 reference manual and supporting
documentation.

%prep
%autosetup -p1 -a1 -n lua-%{version}
cp -p %{SOURCE2} mit.txt

# Use Fedora paths while retaining versioned, parallel-installable module
# directories. LUA_IDSIZE matches Fedora's Lua packaging.
sed -i \
    -e 's|#define LUA_ROOT[[:space:]].*|#define LUA_ROOT "%{_prefix}/"|' \
    -e 's|#define LUA_CDIR[[:space:]].*|#define LUA_CDIR "%{_libdir}/lua/" LUA_VDIR "/"|' \
    -e 's|#define LUA_IDSIZE[[:space:]]*60|#define LUA_IDSIZE 512|' \
    src/luaconf.h

%build
%set_build_flags
%make_build -C src all \
    CC="%{__cc} -std=gnu99" \
    AR="gcc-ar rcs" \
    RANLIB=gcc-ranlib \
    CFLAGS="%{build_cflags} -fPIC -DLUA_USE_LINUX" \
    LDFLAGS="%{build_ldflags}" \
    LIBS="-lm -ldl"

objects="$(%{__ar} t src/liblua.a | sed 's|^|src/|')"
%{__cc} %{build_cflags} %{build_ldflags} -shared \
    -Wl,-soname,liblua%{lua_version}.so.%{lua_soversion} \
    -o src/liblua%{lua_version}.so.%{version} ${objects} -lm -ldl
ln -s liblua%{lua_version}.so.%{version} \
    src/liblua%{lua_version}.so.%{lua_soversion}
ln -s liblua%{lua_version}.so.%{lua_soversion} \
    src/liblua%{lua_version}.so

# Only the interactive interpreter needs readline support.
rm -f src/lua.o
%{__cc} -std=gnu99 %{build_cflags} -fPIC \
    -DLUA_USE_LINUX -DLUA_USE_READLINE \
    -c src/lua.c -o src/lua.o
%{__cc} %{build_cflags} %{build_ldflags} \
    -o src/lua%{lua_version} src/lua.o -Lsrc -Wl,--no-as-needed \
    -llua%{lua_version} -lreadline -lncurses -lm -ldl
%{__cc} %{build_cflags} %{build_ldflags} \
    -o src/luac%{lua_version} src/luac.o src/liblua.a -lm -ldl

%install
install -Dpm0755 src/lua%{lua_version} \
    %{buildroot}%{_bindir}/lua%{lua_version}
install -Dpm0755 src/luac%{lua_version} \
    %{buildroot}%{_bindir}/luac%{lua_version}

install -d %{buildroot}%{_libdir}
install -pm0755 src/liblua%{lua_version}.so.%{version} \
    %{buildroot}%{_libdir}/
ln -s liblua%{lua_version}.so.%{version} \
    %{buildroot}%{_libdir}/liblua%{lua_version}.so.%{lua_soversion}
ln -s liblua%{lua_version}.so.%{lua_soversion} \
    %{buildroot}%{_libdir}/liblua%{lua_version}.so

install -d %{buildroot}%{_includedir}/lua%{lua_version}
install -pm0644 src/lua.h src/luaconf.h src/lualib.h src/lauxlib.h src/lua.hpp \
    %{buildroot}%{_includedir}/lua%{lua_version}/

install -d %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/lua%{lua_version}.pc <<EOF
prefix=%{_prefix}
exec_prefix=\${prefix}
libdir=%{_libdir}
includedir=%{_includedir}/lua%{lua_version}

Name: Lua
Description: Lua 5.5 programming language
Version: %{version}
Libs: -L\${libdir} -llua%{lua_version}
Libs.private: -lm -ldl
Cflags: -I\${includedir}
EOF
ln -s lua%{lua_version}.pc %{buildroot}%{_libdir}/pkgconfig/lua55.pc
ln -s lua%{lua_version}.pc %{buildroot}%{_libdir}/pkgconfig/lua-55.pc
ln -s lua%{lua_version}.pc %{buildroot}%{_libdir}/pkgconfig/lua-5.5.pc

install -d %{buildroot}%{_mandir}/man1
install -pm0644 doc/lua.1 %{buildroot}%{_mandir}/man1/lua%{lua_version}.1
install -pm0644 doc/luac.1 %{buildroot}%{_mandir}/man1/luac%{lua_version}.1

install -d %{buildroot}%{_libdir}/lua/%{lua_version}
install -d %{buildroot}%{_datadir}/lua/%{lua_version}

%check
LD_LIBRARY_PATH="$PWD/src" src/lua%{lua_version} -e \
    'assert(_VERSION == "Lua 5.5")'

# Match the official Fedora Lua test policy for tests that are unsuitable in
# Mock while running the portable user-facing suite.
sed -i -e '/db.lua/d' -e '/errors.lua/d' lua-%{version}-tests/all.lua
pushd lua-%{version}-tests
LD_LIBRARY_PATH="$OLDPWD/src" "$OLDPWD/src/lua%{lua_version}" \
    -e '_U=true' all.lua
popd

PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig \
    pkg-config --exact-version=%{version} lua55

%files
%doc README
%{_bindir}/lua%{lua_version}
%{_bindir}/luac%{lua_version}
%{_mandir}/man1/lua%{lua_version}.1*
%{_mandir}/man1/luac%{lua_version}.1*

%files libs
%license mit.txt
%{_libdir}/liblua%{lua_version}.so.%{lua_soversion}
%{_libdir}/liblua%{lua_version}.so.%{version}
%dir %{_libdir}/lua
%dir %{_libdir}/lua/%{lua_version}
%dir %{_datadir}/lua
%dir %{_datadir}/lua/%{lua_version}

%files devel
%doc README
%{_includedir}/lua%{lua_version}/
%{_libdir}/liblua%{lua_version}.so
%{_libdir}/pkgconfig/lua%{lua_version}.pc
%{_libdir}/pkgconfig/lua55.pc
%{_libdir}/pkgconfig/lua-55.pc
%{_libdir}/pkgconfig/lua-5.5.pc

%files doc
%license mit.txt
%doc doc/*.html doc/*.css doc/*.png

%changelog
* Wed Jul 15 2026 Rahul <rahul@localhost> - 5.5.0-1
- Initial parallel-installable Fedora 44 compatibility package
- Apply Lua 5.5 fixes from official Fedora dist-git
