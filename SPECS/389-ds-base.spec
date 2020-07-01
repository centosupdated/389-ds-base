
%global pkgname   dirsrv
%global srcname   389-ds-base

# Exclude i686 bit arches
ExcludeArch: i686

# for a pre-release, define the prerel field e.g. .a1 .rc2 - comment out for official release
# also remove the space between % and global - this space is needed because
# fedpkg verrel stupidly ignores comment lines
#% global prerel .rc3
# also need the relprefix field for a pre-release e.g. .0 - also comment out for official release
#% global relprefix 0.

# If perl-Socket-2.000 or newer is available, set 0 to use_Socket6.
%global use_Socket6 0

%global use_asan 0
%global use_rust 0
%global use_legacy 1
%global bundle_jemalloc 1
%if %{use_asan}
%global bundle_jemalloc 0
%endif

%if %{bundle_jemalloc}
%global jemalloc_name jemalloc
%global jemalloc_ver 5.2.1
%global __provides_exclude ^libjemalloc\\.so.*$
%endif

# Use Clang instead of GCC
%global use_clang 0

# fedora 15 and later uses tmpfiles.d
# otherwise, comment this out
%{!?with_tmpfiles_d: %global with_tmpfiles_d %{_sysconfdir}/tmpfiles.d}

# systemd support
%global groupname %{pkgname}.target

# set PIE flag
%global _hardened_build 1

Summary:          389 Directory Server (base)
Name:             389-ds-base
Version:          1.4.3.8
Release:          %{?relprefix}2%{?prerel}%{?dist}
License:          GPLv3+
URL:              https://www.port389.org
Group:            System Environment/Daemons
Conflicts:        selinux-policy-base < 3.9.8
Conflicts:        freeipa-server < 4.0.3
Obsoletes:        %{name} <= 1.4.0.9
Provides:         ldif2ldbm >= 0

BuildRequires:    nspr-devel
BuildRequires:    nss-devel >= 3.34
BuildRequires:    perl-generators
BuildRequires:    openldap-devel
BuildRequires:    libdb-devel
BuildRequires:    cyrus-sasl-devel
BuildRequires:    icu
BuildRequires:    libicu-devel
BuildRequires:    pcre-devel
BuildRequires:    cracklib-devel
%if %{use_clang}
BuildRequires:    libatomic
BuildRequires:    clang
%else
BuildRequires:    gcc
BuildRequires:    gcc-c++
%endif
# The following are needed to build the snmp ldap-agent
BuildRequires:    net-snmp-devel
BuildRequires:    lm_sensors-devel
BuildRequires:    bzip2-devel
BuildRequires:    zlib-devel
BuildRequires:    openssl-devel
# the following is for the pam passthru auth plug-in
BuildRequires:    pam-devel
BuildRequires:    systemd-units
BuildRequires:    systemd-devel
%if %{use_asan}
BuildRequires:    libasan
%endif
# If rust is enabled
%if %{use_rust}
BuildRequires: cargo
BuildRequires: rust
%endif
BuildRequires:    pkgconfig
BuildRequires:    pkgconfig(systemd)
BuildRequires:    pkgconfig(krb5)

# Needed to support regeneration of the autotool artifacts.
BuildRequires:    autoconf
BuildRequires:    automake
BuildRequires:    libtool
# For our documentation
BuildRequires:    doxygen
# For tests!
BuildRequires:    libcmocka-devel
BuildRequires:    libevent-devel
# For lib389 and related components
BuildRequires:    python%{python3_pkgversion}
BuildRequires:    python%{python3_pkgversion}-devel
BuildRequires:    python%{python3_pkgversion}-setuptools
BuildRequires:    python%{python3_pkgversion}-ldap
BuildRequires:    python%{python3_pkgversion}-six
BuildRequires:    python%{python3_pkgversion}-pyasn1
BuildRequires:    python%{python3_pkgversion}-pyasn1-modules
BuildRequires:    python%{python3_pkgversion}-dateutil
BuildRequires:    python%{python3_pkgversion}-argcomplete
BuildRequires:    python%{python3_pkgversion}-argparse-manpage
BuildRequires:    python%{python3_pkgversion}-policycoreutils
BuildRequires:    python%{python3_pkgversion}-libselinux

# For cockpit
BuildRequires:    rsync

Requires:         %{name}-libs = %{version}-%{release}
Requires:         python%{python3_pkgversion}-lib389 = %{version}-%{release}

# this is needed for using semanage from our setup scripts
Requires:         policycoreutils-python-utils
Requires:         /usr/sbin/semanage
Requires:         libsemanage-python%{python3_pkgversion}

Requires:         selinux-policy >= 3.14.1-29

# the following are needed for some of our scripts
Requires:         openldap-clients
Requires:         openssl-perl
Requires:         python%{python3_pkgversion}-ldap

# this is needed to setup SSL if you are not using the
# administration server package
Requires:         nss-tools
Requires:         nss >= 3.34

# these are not found by the auto-dependency method
# they are required to support the mandatory LDAP SASL mechs
Requires:         cyrus-sasl-gssapi
Requires:         cyrus-sasl-md5
Requires:         cyrus-sasl-plain

# this is needed for verify-db.pl
Requires:         libdb-utils

# Needed for password dictionary checks
Requires:         cracklib-dicts

# This picks up libperl.so as a Requires, so we add this versioned one
Requires:         perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:         perl-Errno >= 1.23-360

# Needed by logconv.pl
Requires:         perl-DB_File
Requires:         perl-Archive-Tar

# Needed for password dictionary checks
Requires:         cracklib-dicts

# Picks up our systemd deps.
%{?systemd_requires}

Obsoletes:        %{name} <= 1.3.5.4

Source0:          https://releases.pagure.org/389-ds-base/%{name}-%{version}.tar.bz2
# 389-ds-git.sh should be used to generate the source tarball from git
Source1:          %{name}-git.sh
Source2:          %{name}-devel.README
%if %{bundle_jemalloc}
Source3:          https://github.com/jemalloc/%{jemalloc_name}/releases/download/%{jemalloc_ver}/%{jemalloc_name}-%{jemalloc_ver}.tar.bz2
%endif

%description
389 Directory Server is an LDAPv3 compliant server.  The base package includes
the LDAP server and command line utilities for server administration.
%if %{use_asan}
WARNING! This build is linked to Address Sanitisation libraries. This probably
isn't what you want. Please contact support immediately.
Please see http://seclists.org/oss-sec/2016/q1/363 for more information.
%endif

%package          libs
Summary:          Core libraries for 389 Directory Server
Group:            System Environment/Daemons
BuildRequires:    nspr-devel
BuildRequires:    nss-devel >= 3.34
BuildRequires:    openldap-devel
BuildRequires:    libdb-devel
BuildRequires:    cyrus-sasl-devel
BuildRequires:    libicu-devel
BuildRequires:    pcre-devel
BuildRequires:    libtalloc-devel
BuildRequires:    libevent-devel
BuildRequires:    libtevent-devel
Requires:         krb5-libs
Requires:         libevent
BuildRequires:    systemd-devel
Provides:         svrcore = 4.1.4
Conflicts:        svrcore
Obsoletes:        svrcore <= 4.1.3

%description      libs
Core libraries for the 389 Directory Server base package.  These libraries
are used by the main package and the -devel package.  This allows the -devel
package to be installed with just the -libs package and without the main package.

%if %{use_legacy}
%package          legacy-tools
Summary:          Legacy utilities for 389 Directory Server
Group:            System Environment/Daemons
Obsoletes:        %{name} <= 1.4.0.9
Requires:         %{name}-libs = %{version}-%{release}
# for setup-ds.pl to support ipv6
%if %{use_Socket6}
Requires:         perl-Socket6
%else
Requires:         perl-Socket
%endif
Requires:         perl-NetAddr-IP
# use_openldap assumes perl-Mozilla-LDAP is built with openldap support
Requires:         perl-Mozilla-LDAP
# for setup-ds.pl
Requires:         bind-utils
%global __provides_exclude_from %{_libdir}/%{pkgname}/perl
%global __requires_exclude perl\\((DSCreate|DSMigration|DSUpdate|DSUtil|Dialog|DialogManager|FileConn|Inf|Migration|Resource|Setup|SetupLog)
%{?perl_default_filter}

%description      legacy-tools
Legacy (and deprecated) utilities for 389 Directory Server. This includes
the old account management and task scripts. These are deprecated in favour of
the dscreate, dsctl, dsconf and dsidm tools.
%endif

%package          devel
Summary:          Development libraries for 389 Directory Server
Group:            Development/Libraries
Requires:         %{name}-libs = %{version}-%{release}
Requires:         pkgconfig
Requires:         nspr-devel
Requires:         nss-devel >= 3.34
Requires:         openldap-devel
Requires:         libtalloc
Requires:         libevent
Requires:         libtevent
Requires:         systemd-libs
Provides:         svrcore-devel = 4.1.4
Conflicts:        svrcore-devel
Obsoletes:        svrcore-devel <= 4.1.3

%description      devel
Development Libraries and headers for the 389 Directory Server base package.

%package          snmp
Summary:          SNMP Agent for 389 Directory Server
Group:            System Environment/Daemons
Requires:         %{name} = %{version}-%{release}

Obsoletes:        %{name} <= 1.4.0.0

%description      snmp
SNMP Agent for the 389 Directory Server base package.

%package -n python%{python3_pkgversion}-lib389
Summary:  A library for accessing, testing, and configuring the 389 Directory Server
BuildArch:        noarch
Group:            Development/Libraries
Requires: openssl
Requires: iproute
Requires: platform-python
Recommends: bash-completion
Requires: python%{python3_pkgversion}-ldap
Requires: python%{python3_pkgversion}-six
Requires: python%{python3_pkgversion}-pyasn1
Requires: python%{python3_pkgversion}-pyasn1-modules
Requires: python%{python3_pkgversion}-dateutil
Requires: python%{python3_pkgversion}-argcomplete
Requires: python%{python3_pkgversion}-libselinux
Requires: python%{python3_pkgversion}-setuptools
Requires: python%{python3_pkgversion}-distro
%{?python_provide:%python_provide python%{python3_pkgversion}-lib389}

%description -n python%{python3_pkgversion}-lib389
This module contains tools and libraries for accessing, testing,
 and configuring the 389 Directory Server.

%package -n cockpit-389-ds
Summary:          Cockpit UI Plugin for configuring and administering the 389 Directory Server
BuildArch:        noarch
Requires:         cockpit
Requires:         platform-python
Requires:         python%{python3_pkgversion}-lib389

%description -n cockpit-389-ds
A cockpit UI Plugin for configuring and administering the 389 Directory Server

%prep
%autosetup -p1 -v -n %{name}-%{version}%{?prerel}
%if %{bundle_jemalloc}
%setup -q -n %{name}-%{version}%{?prerel} -T -D -b 3
%endif
cp %{SOURCE2} README.devel

%build

OPENLDAP_FLAG="--with-openldap"
%{?with_tmpfiles_d: TMPFILES_FLAG="--with-tmpfiles-d=%{with_tmpfiles_d}"}
# hack hack hack https://bugzilla.redhat.com/show_bug.cgi?id=833529
NSSARGS="--with-nss-lib=%{_libdir} --with-nss-inc=%{_includedir}/nss3"

%if %{use_asan}
ASAN_FLAGS="--enable-asan --enable-debug"
%endif

%if %{use_rust}
RUST_FLAGS="--enable-rust"
%endif

%if %{use_legacy}
LEGACY_FLAGS="--enable-legacy --enable-perl"
%else
LEGACY_FLAGS="--disable-legacy --disable-perl"
%endif

%if %{use_clang}
export CC=clang
export CXX=clang++
CLANG_FLAGS="--enable-clang"
%endif

%if %{bundle_jemalloc}
# Override page size, bz #1545539
# 4K
%ifarch %ix86 %arm x86_64 s390x
%define lg_page --with-lg-page=12
%endif

# 64K
%ifarch ppc64 ppc64le aarch64
%define lg_page --with-lg-page=16
%endif

# Override huge page size on aarch64
# 2M instead of 512M
%ifarch aarch64
%define lg_hugepage --with-lg-hugepage=21
%endif

# Build jemalloc
pushd ../%{jemalloc_name}-%{jemalloc_ver}
%configure \
        --libdir=%{_libdir}/%{pkgname}/lib \
        --bindir=%{_libdir}/%{pkgname}/bin \
        --enable-prof
make %{?_smp_mflags}        
popd
%endif


# Enforce strict linking
%define _strict_symbol_defs_build 1

# Rebuild the autotool artifacts now.
autoreconf -fiv

%configure --enable-autobind --with-selinux $OPENLDAP_FLAG $TMPFILES_FLAG \
           --with-systemd \
           --with-systemdsystemunitdir=%{_unitdir} \
           --with-systemdsystemconfdir=%{_sysconfdir}/systemd/system \
           --with-systemdgroupname=%{groupname}  \
           --libexecdir=%{_libexecdir}/%{pkgname} \
           $NSSARGS $ASAN_FLAGS $RUST_FLAGS $LEGACY_FLAGS $CLANG_FLAGS \
           --enable-cmocka 

# lib389
pushd ./src/lib389
%py3_build
popd
# argparse-manpage dynamic man pages have hardcoded man v1 in header,
# need to change it to v8
sed -i  "1s/\"1\"/\"8\"/" %{_builddir}/%{name}-%{version}%{?prerel}/src/lib389/man/dsconf.8
sed -i  "1s/\"1\"/\"8\"/" %{_builddir}/%{name}-%{version}%{?prerel}/src/lib389/man/dsctl.8
sed -i  "1s/\"1\"/\"8\"/" %{_builddir}/%{name}-%{version}%{?prerel}/src/lib389/man/dsidm.8
sed -i  "1s/\"1\"/\"8\"/" %{_builddir}/%{name}-%{version}%{?prerel}/src/lib389/man/dscreate.8

# Generate symbolic info for debuggers
export XCFLAGS=$RPM_OPT_FLAGS

#make %{?_smp_mflags}
make

%install

mkdir -p %{buildroot}%{_datadir}/gdb/auto-load%{_sbindir}
mkdir -p %{buildroot}%{_datadir}/cockpit
make DESTDIR="$RPM_BUILD_ROOT" install

# Cockpit file list
find %{buildroot}%{_datadir}/cockpit/389-console -type d | sed -e "s@%{buildroot}@@" | sed -e 's/^/\%dir /' > cockpit.list
find %{buildroot}%{_datadir}/cockpit/389-console -type f | sed -e "s@%{buildroot}@@" >> cockpit.list

# Copy in our docs from doxygen.
cp -r %{_builddir}/%{name}-%{version}%{?prerel}/man/man3 $RPM_BUILD_ROOT/%{_mandir}/man3

# lib389
pushd src/lib389
%py3_install
popd

mkdir -p $RPM_BUILD_ROOT/var/log/%{pkgname}
mkdir -p $RPM_BUILD_ROOT/var/lib/%{pkgname}
mkdir -p $RPM_BUILD_ROOT/var/lock/%{pkgname}

# for systemd
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/%{groupname}.wants

#remove libtool archives and static libs
find %{buildroot} -type f -name "*.la" -delete
find %{buildroot} -type f -name "*.a" -delete

%if %{use_legacy}
# make sure perl scripts have a proper shebang
sed -i -e 's|#{{PERL-EXEC}}|#!/usr/bin/perl|' $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/script-templates/template-*.pl
%endif

%if %{bundle_jemalloc}
pushd ../%{jemalloc_name}-%{jemalloc_ver}
make DESTDIR="$RPM_BUILD_ROOT" install_lib install_bin
cp -pa COPYING ../%{name}-%{version}%{?prerel}/COPYING.jemalloc
cp -pa README ../%{name}-%{version}%{?prerel}/README.jemalloc
popd
%endif

%check
# This checks the code, if it fails it prints why, then re-raises the fail to shortcircuit the rpm build.
if ! make DESTDIR="$RPM_BUILD_ROOT" check; then cat ./test-suite.log && false; fi

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -n "$DEBUGPOSTTRANS" ] ; then
    output=$DEBUGPOSTTRANS
    output2=${DEBUGPOSTTRANS}.upgrade
else
    output=/dev/null
    output2=/dev/null
fi

# reload to pick up any changes to systemd files
/bin/systemctl daemon-reload >$output 2>&1 || :

# https://fedoraproject.org/wiki/Packaging:UsersAndGroups#Soft_static_allocation
# Soft static allocation for UID and GID
USERNAME="dirsrv"
ALLOCATED_UID=389
GROUPNAME="dirsrv"
ALLOCATED_GID=389
HOMEDIR="/usr/share/dirsrv"

getent group $GROUPNAME >/dev/null || /usr/sbin/groupadd -f -g $ALLOCATED_GID -r $GROUPNAME
if ! getent passwd $USERNAME >/dev/null ; then
    if ! getent passwd $ALLOCATED_UID >/dev/null ; then
      /usr/sbin/useradd -r -u $ALLOCATED_UID -g $GROUPNAME -d $HOMEDIR -s /sbin/nologin -c "user for 389-ds-base" $USERNAME
    else
      /usr/sbin/useradd -r -g $GROUPNAME -d $HOMEDIR -s /sbin/nologin -c "user for 389-ds-base" $USERNAME
    fi
fi

# Reload our sysctl before we restart (if we can)
sysctl --system &> $output; true

%preun
if [ $1 -eq 0 ]; then # Final removal
    # remove instance specific service files/links
    rm -rf %{_sysconfdir}/systemd/system/%{groupname}.wants/* > /dev/null 2>&1 || :
fi

%postun
if [ $1 = 0 ]; then # Final removal
    rm -rf /var/run/%{pkgname}
fi

%post snmp
%systemd_post %{pkgname}-snmp.service

%preun snmp
%systemd_preun %{pkgname}-snmp.service %{groupname}

%postun snmp
%systemd_postun_with_restart %{pkgname}-snmp.service

%if %{use_legacy}
%post legacy-tools

# START UPGRADE SCRIPT

if [ -n "$DEBUGPOSTTRANS" ] ; then
    output=$DEBUGPOSTTRANS
    output2=${DEBUGPOSTTRANS}.upgrade
else
    output=/dev/null
    output2=/dev/null
fi

# find all instances
instances="" # instances that require a restart after upgrade
ninst=0 # number of instances found in total

echo looking for instances in %{_sysconfdir}/%{pkgname} > $output 2>&1 || :
instbase="%{_sysconfdir}/%{pkgname}"
for dir in $instbase/slapd-* ; do
    echo dir = $dir >> $output 2>&1 || :
    if [ ! -d "$dir" ] ; then continue ; fi
    case "$dir" in *.removed) continue ;; esac
    basename=`basename $dir`
    inst="%{pkgname}@`echo $basename | sed -e 's/slapd-//g'`"
    echo found instance $inst - getting status  >> $output 2>&1 || :
    if /bin/systemctl -q is-active $inst ; then
       echo instance $inst is running >> $output 2>&1 || :
       instances="$instances $inst"
    else
       echo instance $inst is not running >> $output 2>&1 || :
    fi
    ninst=`expr $ninst + 1`
done
if [ $ninst -eq 0 ] ; then
    echo no instances to upgrade >> $output 2>&1 || :
    exit 0 # have no instances to upgrade - just skip the rest
fi
# shutdown all instances
echo shutting down all instances . . . >> $output 2>&1 || :
for inst in $instances ; do
    echo stopping instance $inst >> $output 2>&1 || :
    /bin/systemctl stop $inst >> $output 2>&1 || :
done
echo remove pid files . . . >> $output 2>&1 || :
/bin/rm -f /var/run/%{pkgname}*.pid /var/run/%{pkgname}*.startpid
# do the upgrade
echo upgrading instances . . . >> $output 2>&1 || :
DEBUGPOSTSETUPOPT=`/usr/bin/echo $DEBUGPOSTSETUP | /usr/bin/sed -e "s/[^d]//g"`
if [ -n "$DEBUGPOSTSETUPOPT" ] ; then
    %{_sbindir}/setup-ds.pl -$DEBUGPOSTSETUPOPT -u -s General.UpdateMode=offline >> $output 2>&1 || :
else
    %{_sbindir}/setup-ds.pl -u -s General.UpdateMode=offline >> $output 2>&1 || :
fi

# restart instances that require it
for inst in $instances ; do
    echo restarting instance $inst >> $output 2>&1 || :
    /bin/systemctl start $inst >> $output 2>&1 || :
done
#END UPGRADE
%endif

exit 0


%files
%if %{bundle_jemalloc}
%doc LICENSE LICENSE.GPLv3+ LICENSE.openssl README.jemalloc
%license COPYING.jemalloc
%else
%doc LICENSE LICENSE.GPLv3+ LICENSE.openssl
%endif
%dir %{_sysconfdir}/%{pkgname}
%dir %{_sysconfdir}/%{pkgname}/schema
%config(noreplace)%{_sysconfdir}/%{pkgname}/schema/*.ldif
%dir %{_sysconfdir}/%{pkgname}/config
%dir %{_sysconfdir}/systemd/system/%{groupname}.wants
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/slapd-collations.conf
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/certmap.conf
%{_datadir}/%{pkgname}
%{_datadir}/gdb/auto-load/*
%{_unitdir}
%{_bindir}/dbscan
%{_mandir}/man1/dbscan.1.gz
%{_bindir}/ds-replcheck
%{_mandir}/man1/ds-replcheck.1.gz
%{_bindir}/ds-logpipe.py
%{_mandir}/man1/ds-logpipe.py.1.gz
%{_bindir}/ldclt
%{_mandir}/man1/ldclt.1.gz
%{_sbindir}/ldif2ldap
%{_mandir}/man8/ldif2ldap.8.gz
%{_bindir}/logconv.pl
%{_mandir}/man1/logconv.pl.1.gz
%{_bindir}/pwdhash
%{_mandir}/man1/pwdhash.1.gz
%{_bindir}/readnsstate
%{_mandir}/man1/readnsstate.1.gz
# Remove for now: %caps(CAP_NET_BIND_SERVICE=pe) {_sbindir}/ns-slapd
%{_sbindir}/ns-slapd
%{_mandir}/man8/ns-slapd.8.gz
%{_libexecdir}/%{pkgname}/ds_systemd_ask_password_acl
%{_mandir}/man5/99user.ldif.5.gz
%{_mandir}/man5/certmap.conf.5.gz
%{_mandir}/man5/slapd-collations.conf.5.gz
%{_mandir}/man5/dirsrv.5.gz
%{_mandir}/man5/dirsrv.systemd.5.gz
%{_libdir}/%{pkgname}/python
%dir %{_libdir}/%{pkgname}/plugins
%{_libdir}/%{pkgname}/plugins/*.so
# This has to be hardcoded to /lib - $libdir changes between lib/lib64, but
# sysctl.d is always in /lib.
%{_prefix}/lib/sysctl.d/*
%dir %{_localstatedir}/lib/%{pkgname}
%dir %{_localstatedir}/log/%{pkgname}
%ghost %dir %{_localstatedir}/lock/%{pkgname}
%exclude %{_sbindir}/ldap-agent*
%exclude %{_mandir}/man1/ldap-agent.1.gz
%exclude %{_unitdir}/%{pkgname}-snmp.service
%if %{bundle_jemalloc}
%{_libdir}/%{pkgname}/lib/
%{_libdir}/%{pkgname}/bin/
%exclude %{_libdir}/%{pkgname}/bin/jemalloc-config
%exclude %{_libdir}/%{pkgname}/bin/jemalloc.sh
%exclude %{_libdir}/%{pkgname}/lib/libjemalloc.a
%exclude %{_libdir}/%{pkgname}/lib/libjemalloc.so
%exclude %{_libdir}/%{pkgname}/lib/libjemalloc_pic.a
%exclude %{_libdir}/%{pkgname}/lib/pkgconfig
%endif

%files devel
%doc LICENSE LICENSE.GPLv3+ LICENSE.openssl README.devel
%{_mandir}/man3/*
%{_includedir}/svrcore.h
%{_includedir}/%{pkgname}
%{_libdir}/libsvrcore.so
%{_libdir}/%{pkgname}/libslapd.so
%{_libdir}/%{pkgname}/libns-dshttpd.so
%{_libdir}/%{pkgname}/libsds.so
%{_libdir}/%{pkgname}/libldaputil.so
%{_libdir}/pkgconfig/svrcore.pc
%{_libdir}/pkgconfig/dirsrv.pc
%{_libdir}/pkgconfig/libsds.pc

%files libs
%doc LICENSE LICENSE.GPLv3+ LICENSE.openssl README.devel
%dir %{_libdir}/%{pkgname}
%{_libdir}/libsvrcore.so.*
%{_libdir}/%{pkgname}/libslapd.so.*
%{_libdir}/%{pkgname}/libns-dshttpd-*.so
%{_libdir}/%{pkgname}/libsds.so.*
%{_libdir}/%{pkgname}/libldaputil.so.*
%{_libdir}/%{pkgname}/librewriters.so*
%if %{bundle_jemalloc}
%{_libdir}/%{pkgname}/lib/libjemalloc.so.2
%endif
%if %{use_rust}
%{_libdir}/%{pkgname}/librsds.so
%endif

%if %{use_legacy}
%files legacy-tools
%doc LICENSE LICENSE.GPLv3+ LICENSE.openssl README.devel
%{_bindir}/infadd
%{_mandir}/man1/infadd.1.gz
%{_bindir}/ldif
%{_mandir}/man1/ldif.1.gz
%{_bindir}/migratecred
%{_mandir}/man1/migratecred.1.gz
%{_bindir}/mmldif
%{_mandir}/man1/mmldif.1.gz
%{_bindir}/rsearch
%{_mandir}/man1/rsearch.1.gz
%{_libexecdir}/%{pkgname}/ds_selinux_enabled
%{_libexecdir}/%{pkgname}/ds_selinux_port_query
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/template-initconfig
%{_mandir}/man5/template-initconfig.5.gz
%{_datadir}/%{pkgname}/properties/*.res
%{_datadir}/%{pkgname}/script-templates
%{_datadir}/%{pkgname}/updates
%{_sbindir}/ldif2ldap
%{_mandir}/man8/ldif2ldap.8.gz
%{_sbindir}/bak2db
%{_mandir}/man8/bak2db.8.gz
%{_sbindir}/db2bak
%{_mandir}/man8/db2bak.8.gz
%{_sbindir}/db2index
%{_mandir}/man8/db2index.8.gz
%{_sbindir}/db2ldif
%{_mandir}/man8/db2ldif.8.gz
%{_sbindir}/dbverify
%{_mandir}/man8/dbverify.8.gz
%{_sbindir}/ldif2db
%{_mandir}/man8/ldif2db.8.gz
%{_sbindir}/restart-dirsrv
%{_mandir}/man8/restart-dirsrv.8.gz
%{_sbindir}/start-dirsrv
%{_mandir}/man8/start-dirsrv.8.gz
%{_sbindir}/status-dirsrv
%{_mandir}/man8/status-dirsrv.8.gz
%{_sbindir}/stop-dirsrv
%{_mandir}/man8/stop-dirsrv.8.gz
%{_sbindir}/upgradedb
%{_mandir}/man8/upgradedb.8.gz
%{_sbindir}/vlvindex
%{_mandir}/man8/vlvindex.8.gz
%{_sbindir}/monitor
%{_mandir}/man8/monitor.8.gz
%{_sbindir}/dbmon.sh
%{_mandir}/man8/dbmon.sh.8.gz
%{_sbindir}/dn2rdn
%{_mandir}/man8/dn2rdn.8.gz
%{_sbindir}/restoreconfig
%{_mandir}/man8/restoreconfig.8.gz
%{_sbindir}/saveconfig
%{_mandir}/man8/saveconfig.8.gz
%{_sbindir}/suffix2instance
%{_mandir}/man8/suffix2instance.8.gz
%{_sbindir}/upgradednformat
%{_mandir}/man8/upgradednformat.8.gz
%{_mandir}/man1/dbgen.pl.1.gz
%{_bindir}/repl-monitor
%{_mandir}/man1/repl-monitor.1.gz
%{_bindir}/repl-monitor.pl
%{_mandir}/man1/repl-monitor.pl.1.gz
%{_bindir}/cl-dump
%{_mandir}/man1/cl-dump.1.gz
%{_bindir}/cl-dump.pl
%{_mandir}/man1/cl-dump.pl.1.gz
%{_bindir}/dbgen.pl
%{_mandir}/man8/bak2db.pl.8.gz
%{_sbindir}/bak2db.pl
%{_sbindir}/cleanallruv.pl
%{_mandir}/man8/cleanallruv.pl.8.gz
%{_sbindir}/db2bak.pl
%{_mandir}/man8/db2bak.pl.8.gz
%{_sbindir}/db2index.pl
%{_mandir}/man8/db2index.pl.8.gz
%{_sbindir}/db2ldif.pl
%{_mandir}/man8/db2ldif.pl.8.gz
%{_sbindir}/fixup-linkedattrs.pl
%{_mandir}/man8/fixup-linkedattrs.pl.8.gz
%{_sbindir}/fixup-memberof.pl
%{_mandir}/man8/fixup-memberof.pl.8.gz
%{_sbindir}/ldif2db.pl
%{_mandir}/man8/ldif2db.pl.8.gz
%{_sbindir}/migrate-ds.pl
%{_mandir}/man8/migrate-ds.pl.8.gz
%{_sbindir}/ns-accountstatus.pl
%{_mandir}/man8/ns-accountstatus.pl.8.gz
%{_sbindir}/ns-activate.pl
%{_mandir}/man8/ns-activate.pl.8.gz
%{_sbindir}/ns-inactivate.pl
%{_mandir}/man8/ns-inactivate.pl.8.gz
%{_sbindir}/ns-newpwpolicy.pl
%{_mandir}/man8/ns-newpwpolicy.pl.8.gz
%{_sbindir}/remove-ds.pl
%{_mandir}/man8/remove-ds.pl.8.gz
%{_sbindir}/schema-reload.pl
%{_mandir}/man8/schema-reload.pl.8.gz
%{_sbindir}/setup-ds.pl
%{_mandir}/man8/setup-ds.pl.8.gz
%{_sbindir}/syntax-validate.pl
%{_mandir}/man8/syntax-validate.pl.8.gz
%{_sbindir}/usn-tombstone-cleanup.pl
%{_mandir}/man8/usn-tombstone-cleanup.pl.8.gz
%{_sbindir}/verify-db.pl
%{_mandir}/man8/verify-db.pl.8.gz
%{_libdir}/%{pkgname}/perl
%endif

%files snmp
%doc LICENSE LICENSE.GPLv3+ LICENSE.openssl README.devel
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/ldap-agent.conf
%{_sbindir}/ldap-agent*
%{_mandir}/man1/ldap-agent.1.gz
%{_unitdir}/%{pkgname}-snmp.service

%files -n python%{python3_pkgversion}-lib389
%doc LICENSE LICENSE.GPLv3+
%{python3_sitelib}/lib389*
%{_sbindir}/dsconf
%{_mandir}/man8/dsconf.8.gz
%{_sbindir}/dscreate
%{_mandir}/man8/dscreate.8.gz
%{_sbindir}/dsctl
%{_mandir}/man8/dsctl.8.gz
%{_sbindir}/dsidm
%{_mandir}/man8/dsidm.8.gz
%{_libexecdir}/%{pkgname}/dscontainer

%files -n cockpit-389-ds -f cockpit.list
%{_datarootdir}/metainfo/389-console/org.port389.cockpit_console.metainfo.xml
%doc README.md

%changelog
* Mon May 11 2020 Mark Reynolds <mreynolds@redhat.com> - 1.4.3.8-2
- Bump version to 1.4.3.8-2
- Resolves: Bug 1833350 - Remove cockpit dependancies that are breaking builds

* Mon May 11 2020 Mark Reynolds <mreynolds@redhat.com> - 1.4.3.8-1
- Bump version to 1.4.3.8-1
- Resolves: Bug 1833350 - Rebase 389-ds-base for RHEL 8.3
- Resolves: Bug 1728943 - [RFE] Advance options in RHDS Disk Monitoring Framework
- Resolves: Bug 1775285 - [RFE] Implement the Password Policy attribute "pwdReset"
- Resolves: Bug 1638875 - [RFE] extract key/certs pem file into a private namespace
- Resolves: Bug 1758478 - AddressSanitizer: heap-buffer-overflow in ldap_utf8prev
- Resolves: Bug 1795943 - Port dbmon.sh from legacy tools package
- Resolves: Bug 1798394 - Port dbgen from legacy tools package
- Resolves: Bug 1800529 - Memory leaks in disk monitoring
- Resolves: Bug 1807419 - Unable to create a suffix with countryName either via dscreate or the admin console
- Resolves: Bug 1816848 - Database links: get_monitor() takes 1 positional argument but 2 were given
- Resolves: Bug 1816854 - Setting nsslapd-allowed-sasl-mechanisms truncates the value
- Resolves: Bug 1816857 - Searches on cn=config takes values with spaces and makes multiple attributes out of them
- Resolves: Bug 1816859 - lib389 - Replace exec() with setattr()
- Resolves: Bug 1816862 - Memory leak in indirect COS
- Resolves: Bug 1829071 - Installation of RHDS 11 fails on RHEL8 server with IPv6 disabled
- Resolves: Bug 1833515 - set 'nsslapd-enable-upgrade-hash: off' as this raises warnings in IPA
- Resolves: Bug 1790986 - cenotaph errors on modrdn operations
- Resolves: Bug 1769734 - Heavy StartTLS connection load can randomly fail with err=1
- Resolves: Bug 1758501 - LeakSanitizer: detected memory leaks in changelog5_init and perfctrs_init

* Fri May 8 2020 Mark Reynolds <mreynolds@redhat.com> - 1.4.3.8-0
- Bump version to 1.4.3.8-0
- Issue 51078 - Add nsslapd-enable-upgrade-hash to the schema
- Issue 51054 - Revise ACI target syntax checking
- Issue 51068 - deadlock when updating the schema
- Issue 51060 - unable to set sslVersionMin to TLS1.0
- Issue 51064 - Unable to install server where IPv6 is disabled
- Issue 51051 - CLI fix consistency issues with confirmations
- Issue 49731 - undo db_home_dir under /dev/shm/dirsrv for now
- Issue 51054 - AddressSanitizer: heap-buffer-overflow in ldap_utf8prev
- Issue 51047 - React deprecating ComponentWillMount
- Issue 50499 - fix npm audit issues
- Issue 50545 - Port dbgen.pl to dsctl

* Wed Apr 22 2020 Mark Reynolds <mreynolds@redhat.com> - 1.4.3.7-1
- Bump version to 1.4.3.7
- Issue 51024 - syncrepl_entry callback does not contain attributes added by postoperation plugins
- Issue 51035 - Heavy StartTLS connection load can randomly fail with err=1
- Issue 49731 - undo db_home_dir under /dev/shm/dirsrv for now
- Issue 51031 - UI - transition between two instances needs improvement

* Thu Apr 16 2020 Mark Reynolds <mreynolds@redhat.com> - 1.4.3.6-1
- Bump version to 1.4.3.6
- Issue 50933 - 10rfc2307compat.ldif is not ready to set used by default
- Issue 50931 - RFE AD filter rewriter for ObjectCategory
- Issue 51016 - Fix memory leaks in changelog5_init and perfctrs_init
- Issue 50980 - RFE extend usability for slapi_compute_add_search_rewriter and slapi_compute_add_evaluator
- Issue 51008 - dbhome in containers
- Issue 50875 - Refactor passwordUserAttributes's and passwordBadWords's code
- Issue 51014 - slapi_pal.c possible static buffer overflow
- Issue 50545 - remove dbmon "incr" option from arg parser
- Issue 50545 - Port dbmon.sh to dsconf
- Issue 51005 - AttributeUniqueness plugin's DN parameter should not have a default value
- Issue 49731 - Fix additional issues with setting db home directory by default
- Issue 50337 - Replace exec() with setattr()
- Issue 50905 - intermittent SSL hang with rhds
- Issue 50952 - SSCA lacks basicConstraint:CA
- Issue 50640 - Database links: get_monitor() takes 1 positional argument but 2 were given
- Issue 50869 - Setting nsslapd-allowed-sasl-mechanisms truncates the value

* Wed Apr 1 2020 Mark Reynolds <mreynolds@redhat.com> - 1.4.3.5-1
- Bump version to 1.4.3.5
- Issue 50994 - Fix latest UI bugs found by QE
- Issue 50933 - rfc2307compat.ldif
- Issue 50337 - Replace exec() with setattr()
- Issue 50984 - Memory leaks in disk monitoring
- Issue 50984 - Memory leaks in disk monitoring
- Issue 49731 - dscreate fails in silent mode because of db_home_dir
- Issue 50975 - Revise UI branding with new minimized build
- Issue 49437 - Fix memory leak with indirect COS
- Issue 49731 - Do not add db_home_dir to template-dse.ldif
- Issue 49731 - set and use db_home_directory by default
- Issue 50971 - fix BSD_SOURCE
- Issue 50744 - -n option of dbverify does not work
- Issue 50952 - SSCA lacks basicConstraint:CA
- Issue 50976 - Clean up Web UI source directory from unused files
- Issue 50955 - Fix memory leaks in chaining plugin(part 2)
- Issue 50966 - UI - Database indexes not using typeAhead correctly
- Issue 50974 - UI - wrong title in "Delete Suffix" popup
- Issue 50972 - Fix cockpit plugin build
- Issue 49761 - Fix CI test suite issues
- Issue 50971 - Support building on FreeBSD.
- Issue 50960 - [RFE] Advance options in RHDS Disk Monitoring Framework
- Issue 50800 - wildcards in rootdn-allow-ip attribute are not accepted
- Issue 50963 - We should bundle *.min.js files of Console
- Issue 50860 - Port Password Policy test cases from TET to python3 Password grace limit section.
- Issue 50860 - Port Password Policy test cases from TET to python3 series of bugs Port final
- Issue 50954 - buildnum.py - fix date formatting issue

* Mon Mar 16 2020 Mark Reynolds <mreynolds@redhat.com> - 1.4.3.4-1
- Bump version to 1.4.3.4
- Issue 50954 - Port buildnum.pl to python(part 2)
- Issue 50955 - Fix memory leaks in chaining plugin
- Issue 50954 - Port buildnum.pl to python
- Issue 50947 - change 00core.ldif objectClasses for openldap migration
- Issue 50755 - setting nsslapd-db-home-directory is overriding db_directory
- Issue 50937 - Update CLI for new backend split configuration
- Issue 50860 - Port Password Policy test cases from TET to python3 pwp.sh
- Issue 50945 - givenname alias of gn from openldap
- Issue 50935 - systemd override in lib389 for dscontainer
- Issue 50499 - Fix npm audit issues
- Issue 49761 - Fix CI test suite issues
- Issue 50618 - clean compiler warning and log level
- Issue 50889 - fix compiler issues
- Issue 50884 - Health check tool DSEldif check fails
- Issue 50926 - Remove dual spinner and other UI fixes
- Issue 50928 - Unable to create a suffix with countryName
- Issue 50758 - Only Recommend bash-completion, not Require
- Issue 50923 - Fix a test regression
- Issue 50904 - Connect All React Components And Refactor the Main Navigation Tab Code
- Issue 50920 - cl-dump exit code is 0 even if command fails with invalid arguments
- Issue 50923 - Add test - dsctl fails to remove instances with dashes in the name
- Issue 50919 - Backend delete fails using dsconf
- Issue 50872 - dsconf can't create GSSAPI replication agreements
- Issue 50912 - RFE - add password policy attribute pwdReset
- Issue 50914 - No error returned when adding an entry matching filters for a non existing automember group
- Issue 50889 - Extract pem files into a private namespace
- Issue 50909 - nsDS5ReplicaId cant be set to the old value it had before
- Issue 50686 - Port fractional replication test cases from TET to python3 final
- Issue 49845 - Remove pkgconfig check for libasan
- Issue:50860 - Port Password Policy test cases from TET to python3 bug624080
- Issue:50860 - Port Password Policy test cases from TET to python3 series of bugs
- Issue 50786 - connection table freelist
- Issue 50618 - support cgroupv2
- Issue 50900 - Fix cargo offline build
- Issue 50898 - ldclt core dumped when run with -e genldif option

* Mon Feb 17 2020 Matus Honek <mhonek@redhat.com> - 1.4.3.3-3
- Bring back the necessary c_rehash util (#1803370)

* Fri Feb 14 2020 Mark Reynolds <mreynolds@redhat.com> - 1.4.3.3-2
- Bump version to 1.4.3.3-2
- Remove unneeded perl dependencies
- Change bash-completion to "Recommends" instead of "Requires"

* Thu Feb 13 2020 Mark Reynolds <mreynolds@redhat.com> - 1.4.3.3-1
- Bump version to 1.4.3.3
- Issue 50855 - remove unused file from UI
- Issue 50855 - UI: Port Server Tab to React
- Issue 49845 - README does not contain complete information on building
- Issue 50686 - Port fractional replication test cases from TET to python3 part 1
- Issue 49623 - cont cenotaph errors on modrdn operations
- Issue 50882 - Fix healthcheck errors for instances that do not have TLS enabled
- Issue 50886 - Typo in the replication debug message
- Issue 50873 - Fix healthcheck and virtual attr check
- Issue 50873 - Fix issues with healthcheck tool
- Issue 50028 - Add a new CI test case
- Issue 49946 - Add a new CI test case
- Issue 50117 - Add a new CI test case
- Issue 50787 - fix implementation of attr unique
- Issue 50859 - support running only with ldaps socket
- Issue 50823 - dsctl doesn't work with 'slapd-' in the instance name
- Issue 49624 - cont - DB Deadlock on modrdn appears to corrupt database and entry cache
- Issue 50867 - Fix minor buildsys issues
- Issue 50737 - Allow building with rust online without vendoring
- Issue 50831 - add cargo.lock to allow offline builds
- Issue 50694 - import PEM certs on startup
- Issue 50857 - Memory leak in ACI using IP subject
- Issue 49761 - Fix CI test suite issues
- Issue 50853 - Fix NULL pointer deref in config setting
- Issue 50850 - Fix dsctl healthcheck for python36
- Issue 49990 - Need to enforce a hard maximum limit for file descriptors
- Issue 48707 - ldapssotoken for authentication

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Mark Reynolds <mreynolds@redhat.com> - 1.4.3.2-1
- Bump version to 1.4.3.2
- Issue 49254 - Fix compiler failures and warnings
- Issue 50741 - cont bdb_start - Detected Disorderly Shutdown
- Issue 50836 - Port Schema UI tab to React
- Issue 50842 - Decrease 389-console Cockpit component size
- Issue 50790 - Add result text when filter is invalid
- Issue 50627 - Add ASAN logs to HTML report
- Issue 50834 - Incorrectly setting the NSS default SSL version max
- Issue 50829 - Disk monitoring rotated log cleanup causes heap-use-after-free
- Issue 50709 - (cont) Several memory leaks reported by Valgrind for 389-ds 1.3.9.1-10
- Issue 50784 - performance testing scripts
- Issue 50599 - Fix memory leak when removing db region files
- Issue 49395 - Set the default TLS version min to TLS1.2
- Issue 50818 - dsconf pwdpolicy get error
- Issue 50824 - dsctl remove fails with "name 'ensure_str' is not defined"
- Issue 50599 - Remove db region files prior to db recovery
- Issue 50812 - dscontainer executable should be placed under /usr/libexec/dirsrv/
- Issue 50816 - dsconf allows the root password to be set to nothing
- Issue 50798 - incorrect bytes in format string(fix import issue)

* Thu Jan 16 2020 Adam Williamson <awilliam@redhat.com> - 1.4.3.1-3
- Backport two more import/missing function fixes

* Wed Jan 15 2020 Adam Williamson <awilliam@redhat.com> - 1.4.3.1-2
- Backport 828aad0 to fix missing imports from 1.4.3.1

* Mon Jan 13 2020 Mark Reynolds <mreynolds@redhat.com> - 1.4.3.1-1
- Bump version to 1.4.3.1
- Issue 50798 - incorrect bytes in format string
- Issue 50545 - Add the new replication monitor functionality to UI
- Issue 50806 - Fix minor issues in lib389 health checks
- Issue 50690 - Port Password Storage test cases from TET to python3 part 1
- Issue 49761 - Fix CI test suite issues
- Issue 49761 - Fix CI test suite issues
- Issue 50754 - Add Restore Change Log option to CLI
- Issue 48055 - CI test - automember_plugin(part2)
- Issue 50667 - dsctl -l did not respect PREFIX
- Issue 50780 - More CLI fixes
- Issue 50649 - lib389 without defaults.inf
- Issue 50780 - Fix UI issues
- Issue 50727 - correct mistaken options in filter validation patch
- Issue 50779 - lib389 - conflict compare fails for DN's with spaces
- Set branch version to 1.4.3.0
