%global optflags %{optflags} -Wno-error=strict-aliasing
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define oname Vulkan-Loader
%define major 1
%define libname %mklibname vulkan %{major}
%define devname %mklibname vulkan -d
%define lib32name %mklib32name vulkan %{major}
%define dev32name %mklib32name vulkan -d

%ifarch %{ix86}
%global optflags %{optflags} -O3 -fno-integrated-as
%else
%global optflags %{optflags} -O3
%endif

Summary:	Vulkan ICD desktop loader
Name:		vulkan-loader
Version:	1.4.319
Release:	1
License:	ASL 2.0
URL:		https://github.com/KhronosGroup/Vulkan-Loader
Source0:	https://github.com/KhronosGroup/Vulkan-Loader/archive/v%{version}/%{oname}-%{version}.tar.gz
Patch0:		vulkan-loader-1.2.162-fix-pkgconfig-file.patch
# Don't add -I/usr/include -- harmful while crosscompiling
Patch1:		vulkan-loader-1.4.312-no-Iusrinclude.patch

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(python)
BuildRequires:	vulkan-headers >= %{version}
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-cursor)
BuildRequires:	pkgconfig(wayland-server)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(xcb)
Requires:	%{libname} = %{EVRD}
%if %{with compat32}
BuildRequires:	devel(libwayland-client)
BuildRequires:	devel(libwayland-cursor)
BuildRequires:	devel(libwayland-server)
BuildRequires:	devel(libwayland-egl)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libXrandr)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libxcb)
%endif

%description
This project provides the Khronos official Vulkan ICD desktop 
loader for Windows, Linux, and MacOS.

%package -n %{libname}
Summary:	Vulkan ICD loader library
Group:		System/Libraries
Requires:	%{name} >= %{EVRD}
Recommends:	dri-drivers

%description -n %{libname}
The Vulkan ICD loader library.

Vulkan is an explicit API, enabling direct control over how GPUs actually work.
As such, Vulkan supports systems that have multiple GPUs, each running with a
different driver, or ICD (Installable Client Driver).

Vulkan also supports multiple global contexts (instances, in Vulkan
terminology). The ICD loader is a library that is placed between a Vulkan
application and any number of Vulkan drivers, in order to support multiple
drivers and the instance-level functionality that works across these drivers.
Additionally, the loader manages inserting Vulkan layer libraries, such as
validation layers, between an application and the drivers.

%package -n %{devname}
Summary:	Development files for %{name}
Requires:	%{libname}%{?_isa} = %{version}-%{release}
Requires:	vulkan-headers >= %{version}
Provides:	vulkan-devel = %{EVRD}

%description -n %{devname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

Vulkan is an explicit API, enabling direct control over how GPUs actually work.
As such, Vulkan supports systems that have multiple GPUs, each running with a
different driver, or ICD (Installable Client Driver).

Vulkan also supports multiple global contexts (instances, in Vulkan
terminology). The ICD loader is a library that is placed between a Vulkan
application and any number of Vulkan drivers, in order to support multiple
drivers and the instance-level functionality that works across these drivers.
Additionally, the loader manages inserting Vulkan layer libraries, such as
validation layers, between an application and the drivers.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Vulkan ICD loader library (32-bit)
Group:		System/Libraries
Requires:	%{name} = %{EVRD}

%description -n %{lib32name}
The Vulkan ICD loader library.

Vulkan is an explicit API, enabling direct control over how GPUs actually work.
As such, Vulkan supports systems that have multiple GPUs, each running with a
different driver, or ICD (Installable Client Driver).

Vulkan also supports multiple global contexts (instances, in Vulkan
terminology). The ICD loader is a library that is placed between a Vulkan
application and any number of Vulkan drivers, in order to support multiple
drivers and the instance-level functionality that works across these drivers.
Additionally, the loader manages inserting Vulkan layer libraries, such as
validation layers, between an application and the drivers.

%package -n %{dev32name}
Summary:	Development files for %{name} (32-bit)
Requires:	%{libname}%{?_isa} = %{version}-%{release}
Requires:	%{lib32name}%{?_isa} = %{version}-%{release}
Requires:	vulkan-headers >= %{version}

%description -n %{dev32name}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

Vulkan is an explicit API, enabling direct control over how GPUs actually work.
As such, Vulkan supports systems that have multiple GPUs, each running with a
different driver, or ICD (Installable Client Driver).

Vulkan also supports multiple global contexts (instances, in Vulkan
terminology). The ICD loader is a library that is placed between a Vulkan
application and any number of Vulkan drivers, in order to support multiple
drivers and the instance-level functionality that works across these drivers.
Additionally, the loader manages inserting Vulkan layer libraries, such as
validation layers, between an application and the drivers.
%endif

%prep
%autosetup -n %{oname}-%{version} -p1

%build
%if %{with compat32}
%cmake32 \
	-DVULKAN_HEADERS_INSTALL_DIR=%{_prefix} \
	-G Ninja
%ninja_build
cd ..
%endif

%cmake \
	-DVULKAN_HEADERS_INSTALL_DIR=%{_prefix} \
	-GNinja
%if %{cross_compiling}
# FIXME instead of patching it out, we should figure out where
# it comes from and fix it properly there!
find . -name build.ninja |xargs sed -i -e 's,-isystem /usr/include$,,'
%endif
%ninja_build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%ninja_install -C build

# create the filesystem
mkdir -p %{buildroot}%{_sysconfdir}/vulkan/{explicit,implicit}_layer.d/ \
	%{buildroot}%{_datadir}/vulkan/{explicit,implicit}_layer.d/ \
	%{buildroot}{%{_sysconfdir},%{_datadir}}/vulkan/icd.d

%files
%license LICENSE.txt
%doc README.md CONTRIBUTING.md
%dir %{_sysconfdir}/vulkan/
%dir %{_sysconfdir}/vulkan/explicit_layer.d/
%dir %{_sysconfdir}/vulkan/icd.d/
%dir %{_sysconfdir}/vulkan/implicit_layer.d/
%dir %{_datadir}/vulkan/
%dir %{_datadir}/vulkan/explicit_layer.d/
%dir %{_datadir}/vulkan/icd.d/
%dir %{_datadir}/vulkan/implicit_layer.d/

%files -n %{libname}
%{_libdir}/libvulkan.so.%{major}*

%files -n %{devname}
%{_libdir}/pkgconfig/vulkan.pc
%{_libdir}/*.so
%{_libdir}/cmake/VulkanLoader/

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libvulkan.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/pkgconfig/vulkan.pc
%{_prefix}/lib/*.so
%{_prefix}/lib/cmake/VulkanLoader/
%endif
