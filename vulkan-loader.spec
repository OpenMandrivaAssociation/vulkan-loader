%define	oname	Vulkan-Loader

%define libname %mklibname vulkan 1
%define devname %mklibname vulkan -d

%ifarch %{ix86}
%global optflags %{optflags} -O3 -fno-integrated-as
%else
%global optflags %{optflags} -O3
%endif

Name:		vulkan-loader
Version:	1.2.140
Release:	1
Summary:	Vulkan ICD desktop loader
License:	ASL 2.0
URL:		https://github.com/KhronosGroup/Vulkan-Loader
Source0:	https://github.com/KhronosGroup/Vulkan-Loader/archive/v%{version}/%{oname}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(python3)
BuildRequires:	vulkan-headers >= %{version}
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-cursor)
BuildRequires:	pkgconfig(wayland-server)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xrandr)
Requires:	%{libname} = %{EVRD}

%description
This project provides the Khronos official Vulkan ICD desktop 
loader for Windows, Linux, and MacOS.

%package -n %{libname}
Summary:	Vulkan ICD loader library
Group:		System/Libraries
Requires:	%{name} = %{EVRD}

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

%prep
%autosetup -n %{oname}-%{version}

%build
%cmake \
	-GNinja
%ninja_build

%install
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
%{_libdir}/libvulkan.so.1*

%files -n %{devname}
%{_libdir}/pkgconfig/vulkan.pc
%{_libdir}/*.so
