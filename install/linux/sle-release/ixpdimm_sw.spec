#
# spec file for package ixpdimm_sw
#
# Copyright (c) 2016 Intel Corporation
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define product_name ixpdimm_sw
%define product_base_name ixpdimm
%define build_version 99.99.99.9999
%define api_release 01
%define apibase %{product_base_name}
%define apiname lib%{apibase}%{api_release}
%define cliname %{product_base_name}-cli
%define clilibname lib%{cliname}%{api_release}
%define monitorname %{product_base_name}-monitor
%define cimlibs lib%{product_base_name}-cim%{api_release}
%define dname %{product_base_name}-devel
%define srcname %{product_name}-%{build_version}
#define _unpackaged_files_terminate_build 0

Name:           %{product_name}
Version:        %{build_version}
Release:        1
Summary:        API for development of IXPDIMM management utilities
License:        BSD-3-Clause
Group:          System/Daemons
Url:            https://01.org/ixpdimm-sw
Source:         https://github.com/01org/%{product_name}/archive/ixpdimm_sw-%{build_version}.tar.gz
BuildRequires:  distribution-release
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libkmod)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(libndctl)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  libnuma-devel
BuildRequires:  sblim-cmpi-devel
BuildRequires:  python
BuildRequires:  cmake
BuildRequires:  gettext
BuildRequires:  groff

ExclusiveArch: x86_64

%description
An application program interface (API) for configuring and managing
%{product_name}. Including basic inventory, capacity provisioning,
health monitoring, and troubleshooting.

%package -n %{apiname}
Summary:        API for development of %{product_name} management utilities
Group:          System/Libraries
Requires:       %{apibase}-data
Requires:       libndctl6 >= 58.2
Requires:	invm-frameworks >= %{version}-%{release}

%description -n %{apiname}
An application program interface (API) for configuring and managing
%{product_name}. Including basic inventory, capacity provisioning,
health monitoring, and troubleshooting.

%package -n %{apibase}-data
Summary:        Data files for %{apibase}
Group:          System/Libraries

%description -n %{apibase}-data
An application program interface (API) for configuring and managing
%{product_name}. Including basic inventory, capacity provisioning,
health monitoring, and troubleshooting.

%package -n %{dname}
Summary:        Development files for %{name}
Group:          Development/Libraries/C and C++
Requires:       %{apiname} = %{version}-%{release}

%description -n %{dname}
The %{name}-devel package contains header files for
developing applications that use %{name}.

%package -n %{cimlibs}
Summary:        CIM provider for %{name}
Group:          System/Libraries
Requires:		%{apiname}
Requires:       pywbem
Requires(post): pywbem
Requires(pre):  pywbem

%description -n %{cimlibs}
%{cimlibs} is a common information model (CIM) provider that exposes
%{product_name} as standard CIM objects in order to plug-in to various
common information model object managers (CIMOMS).

%package -n %{monitorname}
Summary:        Daemon for monitoring the status of %{product_name}
Group:          System/Monitoring
BuildRequires:  systemd-rpm-macros
%{?systemd_requires}
Requires:       %{cimlibs} = %{version}-%{release}

%description -n %{monitorname}
A daemon for monitoring the health and status of %{product_name}

%package -n %{cliname}
Summary:        CLI for managment of %{product_name}
Group:          System/Management
Requires:       %{clilibname} = %{version}-%{release}

%description -n %{cliname}
A command line interface (CLI) application for configuring and
managing %{product_name}. Including commands for basic inventory,
capacity provisioning, health monitoring, and troubleshooting.

%package -n %{clilibname}
Summary:        CLI for managment of %{product_name}
Group:          System/Management
Requires:       %{cimlibs}

%description -n %{clilibname}
A command line interface (CLI) application for configuring and
managing %{product_name}. Including commands for basic inventory,
capacity provisioning, health monitoring, and troubleshooting.

%package -n invm-frameworks
Summary:        Library files for invm-frameworks
Group:          Development/Libraries
#The following packages are deprecated and now provided by invm-frameworks
Conflicts:      libinvm-cim
Conflicts:      libinvm-cli
Conflicts:      libinvm-i18n

%description -n invm-frameworks
Framework library supporting a subset of Internationalization (I18N)
functionality, storage command line interface (CLI) applications, storage
common information model (CIM) providers.

%package -n invm-frameworks-devel
Summary:        Development files for invm-frameworks-devel
Group:          Development/Libraries
Requires:       invm-frameworks%{?_isa} = %{version}-%{release}
#The following packages are deprecated and now provided by invm-frameworks-devel
Conflicts:      libinvm-cim-devel
Conflicts:      libinvm-cli-devel
Conflicts:      libinvm-i18n-devel

%description -n invm-frameworks-devel
The invm-frameworks-devel package contains header files for
developing applications that use invm-frameworks.

%prep
%setup -q -n %{srcname}

%build
%cmake -DBUILDNUM=%{version} -DCMAKE_INSTALL_PREFIX=/usr -DRELEASE=ON \
    -DRPM_BUILD=ON -DLINUX_PRODUCT_NAME=%{name} -DRPM_ROOT=%{buildroot} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
    -DCMAKE_INSTALL_BINDIR=%{_bindir} \
    -DCMAKE_INSTALL_DATAROOTDIR=%{_datadir} \
    -DCMAKE_INSTALL_MANDIR=%{_mandir} \
    -DCMAKE_INSTALL_FULL_LOCALSTATEDIR=%{_localstatedir} \
    -DINSTALL_UNITDIR=%{_unitdir} \
    -DCFLAGS_EXTERNAL="%{?optflags}"
make -f Makefile %{?_smp_mflags}

%install
%{!?_cmake_version: cd build}
make -f Makefile install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_prefix}/sbin
ln -sf service %{buildroot}%{_sbindir}/rc%{monitorname}

%pre -n %{monitorname}
%service_add_pre ixpdimm-monitor.service

%post -n %{apiname} -p /sbin/ldconfig
%post -n %{clilibname} -p /sbin/ldconfig
%post -n %{cimlibs} -p /sbin/ldconfig
%post -n invm-frameworks -p /sbin/ldconfig


if [ -x %{_sbindir}/cimserver ]
then
    cimserver --status &> /dev/null
    if [ $? -eq 0 ]
    then
    CIMMOF=cimmof
    else
    for repo in %{_localstatedir}/lib/Pegasus %{_localstatedir}/lib/pegasus %{_prefix}/local%{_localstatedir}/lib/pegasus %{_localstatedir}/local/lib/pegasus %{_localstatedir}/opt/tog-pegasus /opt/ibm/icc/cimom
    do
        if [ -d $repo/repository ]
        then
            CIMMOF="cimmofl -R $repo"
        fi
    done
    fi
    for ns in interop root/interop root/PG_Interop;
    do
        $CIMMOF -E -n$ns %{_datadir}/%{product_name}/Pegasus/mof/pegasus_register.mof &> /dev/null
        if [ $? -eq 0 ]
        then
            $CIMMOF -uc -n$ns %{_datadir}/%{product_name}/Pegasus/mof/pegasus_register.mof &> /dev/null
            $CIMMOF -uc -n$ns %{_datadir}/%{product_name}/Pegasus/mof/profile_registration.mof &> /dev/null
            break
        fi
    done
    $CIMMOF -aE -uc -n root/intelwbem %{_datadir}/%{product_name}/Pegasus/mof/intelwbem.mof &> /dev/null
fi
if [ -x %{_sbindir}/sfcbd ]
then
    RESTART=0
    systemctl is-active sblim-sfcb.service &> /dev/null
    if [ $? -eq 0 ]
    then
        RESTART=1
        systemctl stop sblim-sfcb.service &> /dev/null
    fi

    sfcbstage -n root/intelwbem -r %{_datadir}/%{product_name}/sfcb/INTEL_NVDIMM.reg %{_datadir}/%{product_name}/sfcb/sfcb_intelwbem.mof
    sfcbrepos -f

    if [[ $RESTART -gt 0 ]]
    then
        systemctl start sblim-sfcb.service &> /dev/null
    fi
fi

%post -n %{monitorname}
%service_add_post ixpdimm-monitor.service

%postun -n %{apiname} -p /sbin/ldconfig
%postun -n %{cimlibs} -p /sbin/ldconfig
%postun -n %{clilibname} -p /sbin/ldconfig
%postun -n invm-frameworks -p /sbin/ldconfig

# If upgrading, deregister old version
if [ "$1" -gt 1 ]; then
    RESTART=0
    if [ -x %{_sbindir}/cimserver ]
    then
        cimserver --status &> /dev/null
        if [ $? -gt 0 ]
        then
            RESTART=1
            cimserver enableHttpConnection=false enableHttpsConnection=false enableRemotePrivilegedUserAccess=false slp=false &> /dev/null
        fi
        cimprovider -d -m intelwbemprovider &> /dev/null
        cimprovider -r -m intelwbemprovider &> /dev/null
        mofcomp -v -r -n root/intelwbem %{_datadir}/%{product_name}/Pegasus/mof/intelwbem.mof &> /dev/null
        mofcomp -v -r -n root/intelwbem %{_datadir}/%{product_name}/Pegasus/mof/profile_registration.mof &> /dev/null
        if [[ $RESTART -gt 0 ]]
        then
            cimserver -s &> /dev/null
        fi
    fi
fi

%preun -n %{cimlibs}
RESTART=0
if [ -x %{_sbindir}/cimserver ]
then
    cimserver --status &> /dev/null
    if [ $? -gt 0 ]
    then
        RESTART=1
        cimserver enableHttpConnection=false enableHttpsConnection=false enableRemotePrivilegedUserAccess=false slp=false &> /dev/null
    fi
    cimprovider -d -m intelwbemprovider &> /dev/null
    cimprovider -r -m intelwbemprovider &> /dev/null
    mofcomp -r -n root/intelwbem %{_datadir}/%{product_name}/Pegasus/mof/intelwbem.mof &> /dev/null
    mofcomp -v -r -n root/intelwbem %{_datadir}/%{product_name}/Pegasus/mof/profile_registration.mof &> /dev/null
    if [[ $RESTART -gt 0 ]]
    then
        cimserver -s &> /dev/null
    fi
fi

if [ -x %{_sbindir}/sfcbd ]
then
    RESTART=0
    systemctl is-active sblim-sfcb.service &> /dev/null
    if [ $? -eq 0 ]
    then
        RESTART=1
        systemctl stop sblim-sfcb.service &> /dev/null
    fi

    sfcbunstage -n root/intelwbem -r INTEL_NVDIMM.reg sfcb_intelwbem.mof
    sfcbrepos -f

    if [[ $RESTART -gt 0 ]]
    then
        systemctl start sblim-sfcb.service &> /dev/null
    fi
fi

%preun -n %{monitorname}
%service_del_preun ixpdimm-monitor.service

%postun -n %{monitorname}
%service_del_postun ixpdimm-monitor.service

%files -n %{apiname}
%defattr(-,root,root)
%{_libdir}/libixpdimm.so.*
%{_libdir}/libixpdimm-core.so.*
%{_libdir}/libixpdimm-common.so.*
%doc LICENSE

%files -n %{apibase}-data
%defattr(644,root,root)
%dir %{_localstatedir}/lib/%{product_name}
%{_localstatedir}/lib/%{product_name}/*.pem*
%{_localstatedir}/lib/%{product_name}/*.dat*

%files -n %{dname}
%defattr(-,root,root)
%{_libdir}/libixpdimm.so
%{_libdir}/libixpdimm-core.so
%{_libdir}/libixpdimm-common.so
%{_libdir}/libixpdimm-cli.so
%{_libdir}/libixpdimm-cim.so
%attr(644,root,root) %{_includedir}/nvm_types.h
%attr(644,root,root) %{_includedir}/nvm_management.h
%attr(644,root,root) %{_includedir}/export_api.h
%doc LICENSE

%files -n %{cimlibs}
%defattr(-,root,root)
%{_libdir}/libixpdimm-cim.so.*
%dir %{_datadir}/%{product_name}
%dir %{_datadir}/%{product_name}/Pegasus
%dir %{_datadir}/%{product_name}/Pegasus/mof
%dir %{_datadir}/%{product_name}/sfcb
%attr(644,root,root) %{_datadir}/%{product_name}/sfcb/*.reg
%attr(644,root,root) %{_datadir}/%{product_name}/sfcb/*.mof
%attr(644,root,root) %{_datadir}/%{product_name}/Pegasus/mof/*.mof
%doc LICENSE

%files -n %{monitorname}
%defattr(-,root,root)
%{_bindir}/ixpdimm-monitor
%{_sbindir}/rcixpdimm-monitor
%{_unitdir}/ixpdimm-monitor.service
%attr(644,root,root) %{_mandir}/man8/ixpdimm-monitor*
%doc LICENSE

%files -n %{cliname}
%defattr(-,root,root)
%{_bindir}/ixpdimm-cli
%attr(644,root,root) %{_mandir}/man8/ixpdimm-cli*
%doc LICENSE

%files -n %{clilibname}
%defattr(-,root,root)
%{_libdir}/libixpdimm-cli.so.*

%files -n invm-frameworks
%defattr(-,root,root)
%{_libdir}/libinvm-i18n.so.*
%{_libdir}/libinvm-cli.so.*
%{_libdir}/libinvm-cim.so.*
%doc README.md
%doc LICENSE

%files -n invm-frameworks-devel
%defattr(-,root,root)
%{_libdir}/libinvm-i18n.so
%{_libdir}/libinvm-cli.so
%{_libdir}/libinvm-cim.so
%dir %{_includedir}/libinvm-i18n
%dir %{_includedir}/libinvm-cli
%dir %{_includedir}/libinvm-cim
%attr(644,root,root) %{_includedir}/libinvm-i18n/*.h
%attr(644,root,root) %{_includedir}/libinvm-cli/*.h
%attr(644,root,root) %{_includedir}/libinvm-cim/*.h
%doc README.md
%doc LICENSE

%changelog
