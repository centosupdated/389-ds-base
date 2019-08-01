
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
%global use_perl 1
%global bundle_jemalloc 1
%if %{use_asan}
%global bundle_jemalloc 0
%endif

%if %{bundle_jemalloc}
%global jemalloc_name jemalloc
%global jemalloc_ver 5.1.0
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
Version:          1.4.1.3
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
BuildRequires:    npm
BuildRequires:    nodejs

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
Patch00:          0000-Issue-49602-Revise-replication-status-messages.patch

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

%package          legacy-tools
Summary:          Legacy utilities for 389 Directory Server (%{variant})
Group:            System Environment/Daemons
Obsoletes:        %{name} <= 1.4.0.9
Requires:         %{name} = %{version}-%{release}
%if %{use_perl}
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
%{?perl_default_filter}
%endif
# End use perl

%description      legacy-tools
Legacy (and deprecated) utilities for 389 Directory Server. This includes
the old account management and task scripts. These are deprecated in favour of
the dscreate, dsctl, dsconf and dsidm tools.

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
Requires: python%{python3_pkgversion}-ldap
Requires: python%{python3_pkgversion}-six
Requires: python%{python3_pkgversion}-pyasn1
Requires: python%{python3_pkgversion}-pyasn1-modules
Requires: python%{python3_pkgversion}-dateutil
Requires: python%{python3_pkgversion}-argcomplete
Requires: python%{python3_pkgversion}-libselinux
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

%if !%{use_perl}
PERL_FLAGS="--disable-perl"
%else
PERL_FLAGS="--enable-perl"
%endif

%if %{use_clang}
export CC=clang
export CXX=clang++
CLANG_FLAGS="--enable-clang"
%endif

%if %{bundle_jemalloc}
# Build jemalloc
pushd ../%{jemalloc_name}-%{jemalloc_ver}
%configure \
        --libdir=%{_libdir}/%{pkgname}/lib \
        --bindir=%{_libdir}/%{pkgname}/bin
make
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
           $NSSARGS $ASAN_FLAGS $RUST_FLAGS $PERL_FLAGS $CLANG_FLAGS \
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

# Cockpit branding, and directory and file list
mv -f %{buildroot}%{_datadir}/cockpit/389-console/rhds-banner.html %{buildroot}%{_datadir}/cockpit/389-console/banner.html
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

%if %{use_perl}
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

%post legacy-tools

%if %{use_perl}
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
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/template-initconfig
%{_datadir}/%{pkgname}
%exclude %{_datadir}/%{pkgname}/script-templates
%exclude %{_datadir}/%{pkgname}/updates
%exclude %{_datadir}/%{pkgname}/properties/*.res
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
%{_sbindir}/upgradedb
%{_mandir}/man8/upgradedb.8.gz
%{_sbindir}/vlvindex
%{_mandir}/man8/vlvindex.8.gz
%{_mandir}/man5/99user.ldif.5.gz
%{_mandir}/man5/certmap.conf.5.gz
%{_mandir}/man5/template-initconfig.5.gz
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
%{_libdir}/%{pkgname}/libnunc-stans.so
%{_libdir}/%{pkgname}/libsds.so
%{_libdir}/%{pkgname}/libldaputil.so
%{_libdir}/pkgconfig/svrcore.pc
%{_libdir}/pkgconfig/dirsrv.pc
%{_libdir}/pkgconfig/libsds.pc
%{_libdir}/pkgconfig/nunc-stans.pc

%files libs
%doc LICENSE LICENSE.GPLv3+ LICENSE.openssl README.devel
%dir %{_libdir}/%{pkgname}
%{_libdir}/libsvrcore.so.*
%{_libdir}/%{pkgname}/libslapd.so.*
%{_libdir}/%{pkgname}/libns-dshttpd-*.so
%{_libdir}/%{pkgname}/libnunc-stans.so.*
%{_libdir}/%{pkgname}/libsds.so.*
%{_libdir}/%{pkgname}/libldaputil.so.*
%if %{bundle_jemalloc}
%{_libdir}/%{pkgname}/lib/libjemalloc.so.2
%endif
%if %{use_rust}
%{_libdir}/%{pkgname}/librsds.so
%endif

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
%{_sbindir}/restart-dirsrv
%{_mandir}/man8/restart-dirsrv.8.gz
%{_sbindir}/start-dirsrv
%{_mandir}/man8/start-dirsrv.8.gz
%{_sbindir}/status-dirsrv
%{_mandir}/man8/status-dirsrv.8.gz
%{_sbindir}/stop-dirsrv
%{_mandir}/man8/stop-dirsrv.8.gz
%if %{use_perl}
%{_datadir}/%{pkgname}/properties/*.res
%{_datadir}/%{pkgname}/script-templates
%{_datadir}/%{pkgname}/updates
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
%{_libexecdir}/%{pkgname}/ds_selinux_enabled
%{_libexecdir}/%{pkgname}/ds_selinux_port_query
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
%{_sbindir}/dscontainer

%files -n cockpit-389-ds -f cockpit.list
%{_datarootdir}/metainfo/389-console/org.port389.cockpit_console.metainfo.xml
%doc README.md

%changelog
* Fri May 24 2019 Mark Reynolds <mreynolds@redhat.com> - 1.4.1.3-2
- Bump version to 1.4.1.3-2
- Resolves: Bug 1544973 - [RFE] IPA replica stuck at last update status: Error (18) Replication error acquiring replica: Incremental update transient error. 

* Fri May 24 2019 Mark Reynolds <mreynolds@redhat.com> - 1.4.1.3-1
- Bump version to 1.4.1.3-1
- Resolves: Bug 1633718 - 389-ds module: Switched Requires from "python3" to "platform-python"
- Resolves: Bug 1654059 - 389-ds-base: dscreate and dsconf print DM's password in verbose mode
- Resolves: Bug 1712467 - Rebase 389-ds-base on RHEL 8.1 

* Fri Feb 01 2019 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.20-7
- Bump version to 1.4.0.20-7
- Resolves: Bug 1671735 - dscreate interactive fails when the suffix contains spaces 
- Resolves: Bug 1654101 - Fix cherry-pick error in setup.py

* Thu Jan 31 2019 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.20-6
- Bump version to 1.4.0.20-6
- Resolves: Bug 1654101 - dscreate - suffix create root node option
- Resolves: Bug 1671505 - ns-slapd crashes with k5_mutex_lock: Assertion `r == 0' failed 

* Fri Jan 11 2019 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.20-5
- Bump version to 1.4.0.20-5
- Resolves: Bug 1654566 - dsctl db2ldif: Failing with error AttributeError: DirSrv has no attribute '_instance'

* Fri Jan 4 2019 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.20-4
- Bump version to 1.4.0.20-4
- Resolves: Bug 1654105 - fix source tar ball

* Fri Dec 21 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.20-3
- Bump version to 1.4.0.20-3 
- Resolves: Bug 1654105 - RHDS 11: dsconf related issues
- Resolves: Bug 1623634 - Add backend functionality to UI's Plugin Tab
- Resolves: Bug 1648971 - ssca needs to be removed after dirsrv instance is removed
- Resolves: Bug 1654430 - cockpit does not validate Directory Manager password change operation
- Resolves: Bug 1654241 - Add backend functionality to UI's Server Tab No. 2 (CLI and UI)
- Resolves: Bug 1658622 - Information disclosure while using WebUI

* Fri Dec 14 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.20-2
- Bump version to 1.4.0.20-2
- Resolves: Bug 1648937 - python3-lib389 pulls dependencies required only by tests

* Fri Dec 14 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.20-1
- Bump version to 1.4.0.20-1
- Resolves: Bug 1631461 - Python installer doesn't label ports with ldap_port_t
- Resolves: Bug 1653165 - certmap fails when Issuer DN has comma in name
- Resolves: Bug 1653469 - Customer requesting -y option for ds-replcheck
- Resolves: Bug 1654101 - dscreate related issues
- Resolves: Bug 1654116 - dsctl related issues
- Resolves: Bug 1654134 - 389 web UI gives error when try to do backup management
- Resolves: Bug 1654281 - RHDS webui console is not loading other instances apart
- Resolves: Bug 1654451 - dscreate permissions and SELinux labels "too relaxed/open", "incorrect" 
- Resolves: Bug 1654518 - While creating instance getting error "ERR - createprlistensockets - PR_Bind() on All Interfaces port 392 failed: Netscape Portable Runtime error -5966
- Resolves: Bug 1654566 - dsctl db2ldif: Failing with error AttributeError: DirSrv has no attribute '_instance'
- Resolves: Bug 1654577 - Cockpit create backup should perform backup name check
- Resolves: Bug 1654581 - dsidm: User creation failing with error AttributeError: module 'sys' has no attribute 'ext' 
- Resolves: Bug 1654693 - dsconfig doesn't have option to pass password as an argument
- Resolves: Bug 1658613 - Bind password change for replica agreement breaks replication

* Tue Nov 27 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.19-2
- Bump version to 1.4.0.19-2
- Resolves: Bug 1631461 - Python installer doesn't label ports with ldap_port_t

* Fri Nov 2 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.19-1
- Bump version to 1.4.0.19-1
- Resolves: Bug 1648924 - during MODRDN referential integrity can fail erronously while updating large groups
- Resolves: Bug 1631461 - Python installer doesn't label ports with ldap_port_t

* Fri Nov 2 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.18-3
- Bump version to 1.4.0.18-3
- Resolves: Bug 1618411 - Internal operation logging counts were off

* Mon Oct 15 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.18-2
- Bump version to 1.4.0.18-2
- Resolves: Bug 1633718 - Fix regression from previous patch

* Mon Oct 15 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.18-1
- Bump version to 1.4.0.18-1
- Resolves: Bug 1602439 - Please review important issues found by covscan in "389-ds-base-1.4.0.11-1.el8+7" package
- Resolves: Bug 1623631 - Add backend functionality to UI's Replication Tab
- Resolves: Bug 1623633 - Add backend functionality to UI's Schema Tab
- Resolves: Bug 1588057 - CVE-2018-10850 389-ds-base: race condition on reference counter leads to DoS using persistent search
- Resolves: Bug 1624420 - CVE-2018-14638 389-ds-base: Crash in delete_passwdPolicy when persistent search connections are terminated unexpectedly
- Resolves: Bug 1633718 - 389-ds module: Switched Requires from "python3" to "platform-python"

* Wed Oct 03 2018 Matus Honek <mhonek@redhat.com> - 1.4.0.17-3
- Bump version to 1.4.0.17-3
- Resolves: Bug 1635675 - Typo in SPEC file's 'Requires' breaks the latest compose

* Tue Sep 25 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.17-2
- Bump version to 1.4.0.17-2
- - Resolves: Bug 1623633 - Remove linux capabilities(Ticket 48432)

* Tue Sep 25 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.17-1
- Bump version to 1.4.0.17-1
- Resolves: Bug 1623633 - Add backend functionality to UI's Schema Tab
- Resolves: Bug 1602439 - Please review important issues found by covscan
- Resolves: Bug 1629676 - replica install fails on s390x arch

* Wed Sep 19 2018 Tomas Orsava <torsava@redhat.com> - 1.4.0.14-6
- Require the Python interpreter directly instead of using the package name
- Related: rhbz#1619153

* Wed Aug 29 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.14-5
- Bump version to 1.4.0.14-5
- Resolves: Bug 1591761 - Revert ticket 49372
- Resolves: Bug 1624196 - CVE-2018-14624 389-ds-base: Server crash through modify command with large DN

* Thu Aug 16 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.14-4
- Bump version to 1.4.0.14-4
- Resolves: Bug 1618411 - Internal operation logging causes crash

* Mon Aug 13 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.14-3
- Bump version to 1.4.0.14-3
- Resolves: Bug 1591761 - Fix typo in changelog date

* Mon Aug 13 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.14-2
- Bump version to 1.4.0.14-3
- Resolves: Bug 1591761 - Only ship libjemalloc.so.2

* Fri Aug 10 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.14-1
- Bump version to 1.4.0.14
- Resolves: Bug 1578773 - ipa-server-install fails on missing setup-ds.pl dependency
- Ticket 49891 - Use "__python3" macro for python scripts
- Ticket 49890 - ldapsearch with server side sort crashes the ldap server
- Ticket 49029 - RFE -improve internal operations logging
- Ticket 49893 - disable nunc-stans by default
- Ticket 48377 - Update file name for LD_PRELOAD
- Ticket 49884 - Improve nunc-stans test to detect socket errors sooner
- Ticket 49888 - Use perl filter in rpm specfile
- Ticket 49866 - Add password policy features to CLI/UI
- Ticket 49881 - Missing check for crack.h
- Ticket 48056 - Add more test cases to the basic suite
- Ticket 49761 - Fix replication test suite issues
- Ticket 49381 - Refactor the plugin test suite docstrings
- Ticket 49837 - Add new password policy attributes to UI
- Ticket 49794 - RFE - Add pam_pwquality features to password syntax checking
- Ticket 49867 - Fix CLI tools' double output

* Thu Aug 09 2018 Josef Ridky <jridky@redhat.com> - 1.4.0.13-2
- Rebuild for Net-SNMP 5.8

* Thu Jul 19 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.13-1
- Bump version to 1.4.0.13
- Ticket 49854 - ns-slapd should create run_dir and lock_dir directories at startup
- Ticket 49806 - Add SASL functionality to CLI/UI
- Ticket 49789 - backout original security fix as it caused a regression in FreeIPA
- Ticket 49857 - RPM scriptlet for 389-ds-base-legacy-tools throws an error

* Tue Jul 17 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.12-1
- Bump version to 1.4.0.12-1
- Ticket 48377 - Move jemalloc license to /usr/share/licences
- Ticket 49813 - Revised interactive installer
- Ticket 49789 - By default, do not manage unhashed password
- Ticket 49844 - lib389: don't set up logging at module scope
- Ticket 49546 - Fix issues with MIB file
- Ticket 49840 - ds-replcheck command returns traceback errors against ldif files having garbage content when run in offline mode
- Ticket 49640 - Cleanup plugin bootstrap logging
- Ticket 49835 - lib389: fix logging
- Ticket 48818 - For a replica bindDNGroup, should be fetched the first time it is used not when the replica is started
- Ticket 49780 - acl_copyEval_context double free
- Ticket 49830 - Import fails if backend name is "default"
- Ticket 49832 - remove tcmalloc references
- Ticket 49813 - dscreate - add interactive installer
- Ticket 49808 - Add option to add backend to dscreate
- Ticket 49811 - lib389 setup.py should install autogenerated man pages
- Ticket 49795 - UI - add "action" backend funtionality
- Ticket 49588 - Add py3 support for tickets : part-3
- Ticket 49820 - lib389 requires wrong python ldap library
- Ticket 49791 - Update docker file for new dscreate options
- Ticket 49761 - Fix more CI test issues
- Ticket 49811 - Update man pages
- Ticket 49783 - UI - add server configuration backend
- Ticket 49717 - Add conftest.py for tests
- Ticket 49588 - Add py3 support for tickets
- Ticket 49793 - Updated descriptions in dscreate example INF file
- Ticket 49471 - Rename dscreate options
- Ticket 49751 - passwordMustChange attribute is not honored by a RO consumer if using "Chain on Update"
- Ticket 49734 - Fix various issues with Disk Monitoring
- Update Source0 URL in rpm/389-ds-base.spec.in


* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0.11-2.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 1.4.0.11-2.4
- Rebuild for ICU 62

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 1.4.0.11-2.3
- Perl 5.28 rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1.4.0.11-2.2
- Rebuilt for Python 3.7

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.4.0.11-2.1
- Perl 5.28 rebuild

* Thu Jun 21 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.11-2
- Bump version to 1.4.0.11-2
- Add python3-lib389 requirement

* Tue Jun 19 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.11-1
- Bump version to 1.4.0.11
- Test for issue #49788
- Fixing 4-byte UTF-8 character validation
- Ticket 49777 - add config subcommand to dsconf
- Ticket 49712 - lib389 CLI tools should return a result code on failures
- Issue 49588 - Add py3 support for tickets : part-2
- Remove old RHEL/fedora version checking from upstream specfile
- Ticket 48204 - remove python2 from scripts
- Ticket 49576 - ds-replcheck: fix certificate directory verification
- Bug 1591761 - 389-ds-base: Remove jemalloc exports

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.4.0.10-2.1
- Rebuilt for Python 3.7

* Fri Jun 8 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.10-2
- Bump verision to 1.4.0.10-2
- Remove reference ro stop-dirsrv from legacy tools

* Fri Jun 8 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.10-1
- Bump verision to 1.4.0.10-1
- Ticket 49640 - Errors about PBKDF2 password storage plugin at server startup
- Ticket 49571 - perl subpackage and python installer by default
- Ticket 49740 - UI - Replication monitor color coding is not colorblind friendly
- Ticket 49741 - UI - View/Edit replication agreement hangs WebUI
- Ticket 49703 - UI - Set default values in create instance form
- Ticket 49742 - Fine grained password policy can impact search performance
- Ticket 49768 - Under network intensive load persistent search can erronously decrease connection refcnt
- Ticket 49765 - compiler warning
- Ticket 49689 - Cockpit subpackage does not build in PREFIX installations
- Ticket 49765 - Async operations can hang when the server is running nunc-stans
- Ticket 49745 - UI add filter options for error log severity levels
- Ticket 49761 - Fix test suite issues
- Ticket 49754 - instances created with dscreate can not be upgraded with setup-ds.pl
- Ticket 47902 - UI - add continuous refresh log feature
- Ticket 49381 - Add docstrings to plugin test suites - Part 1
- Ticket 49646 - Improve TLS cert processing in lib389 CLI
- Ticket 49748 - Passthru plugin startTLS option not working
- Ticket 49732 - Optimize resource limit checking for rootdn issued searches
- Ticket 48377 - Bundle jemalloc
- Ticket 49736 - Hardening of active connection list
- Ticket 48184 - clean up and delete connections at shutdown (3rd)
- Ticket 49675 - Revise coverity fix
- Ticket 49333 - Do not remove versioned man pages
- Ticket 49683 - Add support for JSON option in lib389 CLI tools
- Ticket 49704 - Error log from the installer is concatenating all lines into one
- Ticket 49726 - DS only accepts RSA and Fortezza cipher families
- Ticket 49722 - Errors log full of " WARN - keys2idl - recieved NULL idl from index_read_ext_allids, treating as empty set" messages
- Ticket 49582 - Add py3 support to memberof_plugin test suite
- Ticket 49675 - Fix coverity issues
- Ticket 49576 - Add support of ";deletedattribute" in ds-replcheck
- Ticket 49706 - Finish UI patternfly convertions
- Ticket 49684 - AC_PROG_CC clobbers CFLAGS set by --enable-debug
- Ticket 49678 - organiSational vs organiZational spelling in lib389
- Ticket 49689 - Fix local "make install" after adding cockpit subpackage
- Ticket 49689 - Move Cockpit UI plugin to a subpackage
- Ticket 49679 - Missing nunc-stans documentation and doxygen warnings
- Ticket 49588 - Add py3 support for tickets : part-1
- Ticket 49576 - Update ds-replcheck for new conflict entries
- Ticket 48184 - clean up and delete connections at shutdown (2nd try)
- Ticket 49698 - Remove unneeded patternfly files from Cockpit package
- Ticket 49581 - Fix dynamic plugins test suite
- Ticket 49665 - remove obsoleted upgrade scripts
- Ticket 49693 - A DB_DEADLOCK while adding a tombstone (RUV) leads to access of an already freed entry
- Ticket 49696 - replicated operations should be serialized
- Ticket 49669 - Invalid cachemem size can crash the server during a restore
- Ticket 49684 - AC_PROG_CC clobbers CFLAGS set by --enable-debug
- Ticket 49685 - make clean fails if cargo is not installed
- Ticket 49106 - Move ds_* scripts to libexec
- Ticket 49657 - Fix cascading replication scenario in lib389 API
- Ticket 49671 - Readonly replicas should not write internal ops to changelog
- Ticket 49673 - nsslapd-cachememsize can't be set to a value bigger than MAX_INT
- Ticket 49519 - Convert Cockpit UI to use strictly patternfly stylesheets
- Ticket 49665 - Upgrade script doesn't enable CRYPT password storage plug-in
- Ticket 49665 - Upgrade script doesn't enable PBKDF2 password storage plug-in

* Tue May 15 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.9-2
- Bump version to 1.4.0.9-2
- Add openssl-perl requirement for new python installer

* Tue May 8 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.9-1
- Bump version to 1.4.0.9
- Ticket 49661 - CVE-2018-1089 - Crash from long search filter
- Ticket 49652 - DENY aci's are not handled properly
- Ticket 49650 - lib389 enable_tls doesn't work on F28
- Ticket 49538 - replace cacertdir_rehash with openssl rehash
- Ticket 49406 - Port backend_test.py test to DSLdapObject implementation
- Ticket 49649 - Use reentrant crypt_r()
- Ticket 49642 - lib389 should generate a more complex password
- Ticket 49612 - lib389 remove_ds_instance() does not remove systemd units
- Ticket 49644 - crash in debug build

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 1.4.0.8-1.1
- Rebuild for ICU 61.1

* Thu Apr 19 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.8-1
- Bump version to 1.4.0.8-1
- Ticket 49639 - Crash when failing to read from SASL conn
- Ticket 49109 - nsDS5ReplicaTransportInfo should accept StartTLS as an option
- Ticket 49586 - Add py3 support to plugins test suite
- Ticket 49511 - memory leak in pwdhash

* Mon Apr 16 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.7-2
- Bump version to 1.4.0.7-2
- Fix the devel srvcore requirements

* Fri Apr 13 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.7-1
- Bump version to 1.4.0.7
- Ticket 49477 - Missing pbkdf python
- Ticket 49552 - Fix the last of the build issues on F28/29
- Ticket 49522 - Fix build issues on F28
- Ticket 49631 - same csn generated twice
- Ticket 49585 - Add py3 support to password test suite : part-3
- Ticket 49585 - Add py3 support to password test suite : part-2
- Ticket 48184 - revert previous patch around unuc-stans shutdown crash
- Ticket 49585 - Add py3 support to password test suite
- Ticket 46918 - Fix compiler warnings on arm
- Ticket 49601 - Replace HAVE_SYSTEMD define with WITH_SYSTEMD in svrcore
- Ticket 49619 - adjustment of csn_generator can fail so next generated csn can be equal to the most recent one received
- Ticket 49608 - Add support for gcc/clang sanitizers
- Ticket 49606 - Improve lib389 documentation
- Ticket 49552 - Fix build issues on F28
- Ticket 49603 - 389-ds-base package rebuilt on EPEL can't be installed due to missing dependencies
- Ticket 49593 - NDN cache stats should be under the global stats
- Ticket 49599 - Revise replication total init status messages
- Ticket 49596 - repl-monitor.pl fails to find db tombstone/RUV entry
- Ticket 49589 - merge svrcore into 389-ds-base
- Ticket 49560 - Add a test case for extract-pemfiles
- Ticket 49239 - Add a test suite for ds-replcheck tool RFE
- Ticket 49369 - merge svrcore into 389-ds-base

* Thu Mar 29 2018 Till Maas <opensource@till.name> - 1.4.0.6-3
- Remove BR on tcp_wrappers (https://bugzilla.redhat.com/show_bug.cgi?id=1518749)

* Tue Mar 6 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.6-1
- Bump version to 1.4.0.6
- Ticket 49545 - final substring extended filter search returns invalid result
- Ticket 49572 - ns_job_wait race on condvar
- Ticket 49584 - Fix Tickets with paged_results test suite
- Ticket 49161 - memberof fails if group is moved into scope
- Ticket 49447 - PBKDF2 on upgrade
- ticket 49551 - correctly handle subordinates and tombstone numsubordinates
- Ticket 49043 - Add replica conflict test suite
- Ticket 49296 - Fix race condition in connection code with  anonymous limits
- Ticket 49568 - Fix integer overflow on 32bit platforms
- Ticket 48085 - Add encryption cl5 test suite
- Ticket 49566 - ds-replcheck needs to work with hidden conflict entries
- Ticket 49519 - Add more Cockpit UI content
- Ticket 49551 - fix memory leak found by coverity
- Ticket 49551 - v3 - correct handling of numsubordinates for cenotaphs and tombstone delete
- Ticket 49278 - Add a new CI test case
- Ticket 49560 - nsslapd-extract-pemfiles should be enabled by default as openldap is moving to openssl
- Ticket 49557 - Add config option for checking CRL on outbound SSL Connections
- Ticket 49446 - Add CI test case
- Ticket 35 -    Description: Add support for managing automember to dsconf
- Ticket 49544 - cli release preperation
- Ticket 48006 - Add a new CI test case

* Mon Feb 19 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.5-1.7
- Add cyrus-sasl-plain requirement

* Thu Feb 15 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.5-1.6
- Fix python requirements for policycoreutils-python-utils

* Thu Feb 15 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.5-1.5
- Fix package requirements to use Python 3 packages for LDAP and SELinux

* Thu Feb 15 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.5-1.4
- Only exclude Ix86 arches

* Thu Feb 15 2018 Adam Williamson <awilliam@redhat.com> - 1.4.0.5-1.3
- Rebuild for libevent soname bump

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.0.5-1.2
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0.5-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.5-1
- Bump version to 1.4.0.5
- CVE-2017-15134 389-ds-base: Remote DoS via search filters in slapi_filter_sprintf
- Ticket 49546 - Fix broken snmp MIB file
- Ticket 49554 - update readme
- Ticket 49554 - Update Makefile for README.md
- Ticket 49400 - Make CLANG configurable
- Ticket 49530 - Add pseudolocalization option for dbgen
- Ticket 49523 - Fixed skipif marker, topology fixture and log message
- Ticket 49544 - Double check pw prompts
- Ticket 49548 - Cockpit UI - installer should also setup Cockpit

* Fri Jan 26 2018 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.4-1
- Bump version to 1.4.0.4
- Ticket 49540 - Indexing task is reported finished too early regarding the backend status
- Ticket 49534 - Fix coverity regression
- Ticket 49544 - cli release preperation, group improvements
- Ticket 49542 - Unpackaged files on el7 break rpm build
- Ticket 49541 - repl config should not allow rid 65535 for masters
- Ticket 49370 - Add all the password policy defaults to a new local policy
- Ticket 49425 - improve demo objects for install
- Ticket 49537 - allow asan to build with stable rustc
- Ticket 49526 - Improve create_test.py script
- Ticket 49516 - Add python 3 support for replication suite
- Ticket 49534 - Fix coverity issues and regression
- Ticket 49532 - coverity issues - fix compiler warnings & clang issues
- Ticket 49531 - coverity issues - fix memory leaks
- Ticket 49463 - After cleanALLruv, there is a flow of keep alive DEL
- Ticket 49529 - Fix Coverity warnings: invalid deferences
- Ticket 49509 - Indexing of internationalized matching rules is failing
- Ticket 49527 - Improve ds* cli tool testing
- Ticket 49474 - purge saslmaps before gssapi test
- Ticket 49413 - Changelog trimming ignores disabled replica-agreement
- Ticket 49446 - cleanallruv should ignore cleaned replica Id in processing changelog if in force mode
- Ticket 49278 - GetEffectiveRights gives false-negative
- Ticket 49508 - memory leak in cn=replica plugin setup
- Ticket 48118 - Add CI test case
- Ticket 49520 - Cockpit UI - Add database chaining HTML
- Ticket 49512 - Add ds-cockpit-setup to rpm spec file
- Ticket 49523 - Refactor CI test
- Ticket 49524 - Password policy: minimum token length fails  when the token length is equal to attribute length
- Ticket 49517 - Cockpit UI - Add correct png files
- Ticket 49517 - Cockput UI - revise config layout
- Ticket 49523 - memberof: schema violation error message is confusing as memberof will likely repair target entry
- Ticket 49312 - Added a new test case for "-D configdir"
- Ticket 49512 - remove backup directories from cockpit source
- Ticket 49512 - Add initial Cockpit UI Plugin
- Ticket 49515 - cannot link, missing -fPIC
- Ticket 49474 - Improve GSSAPI testing capability
- Ticket 49493 - heap use after free in csn_as_string
- Ticket 49379 - Add Python 3 support to CI test
- Ticket 49431 - Add CI test case
- Ticket 49495 - cos stress test and improvements.
- Ticket 49495 - Fix memory management is vattr.
- Ticket 49494 - python 2 bytes mode.
- Ticket 49471 - heap-buffer-overflow in ss_unescape
- Ticket 48184 - close connections at shutdown cleanly.
- Ticket 49218 - Certmap - support TLS tests
- Ticket 49470 - overflow in pblock_get
- Ticket 49443 - Add CI test case
- Ticket 49484 - Minor cli tool fixes.
- Ticket 49486 - change ns stress core to use absolute int width.
- Ticket 49445 - Improve regression test to detect memory leak.
- Ticket 49445 - Memory leak in ldif2db
- Ticket 49485 - Typo in gccsec_defs
- Ticket 49479 - Remove unused 'batch' argument from lib389
- Ticket 49480 - Improvements to support IPA install.
- Ticket 49474 - sasl allow mechs does not operate correctly
- Ticket 49449 - Load sysctl values on rpm upgrade.
- Ticket 49374 - Add CI test case
- Ticket 49325 - fix rust linking.
- Ticket 49475 - docker poc improvements.
- Ticket 49461 - Improve db2index handling for test 49290
- Ticket 47536 - Add Python 3 support and move test case to suites
- Ticket 49444 - huaf in task.c during high load import
- Ticket 49460 - replica_write_ruv log a failure even when it succeeds
- Ticket 49298 - Ticket with test case and remove-ds.pl
- Ticket 49408 - Add a test case for nsds5ReplicaId checks
- Ticket 3 lib389 - python 3 support for subset of pwd cases
- Ticket 35 lib389 - dsconf automember support

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.4.0.3-1.2
- Rebuilt for switch to libxcrypt

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 1.4.0.3-1.1
- Rebuild for ICU 60.1

* Mon Nov 20 2017 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.3-1
- Bump version to 1.4.0.3
- Ticket 49457 - Fix spal_meminfo_get function prototype
- Ticket 49455 - Add tests to monitor test suit.
- Ticket 49448 - dynamic default pw scheme based on environment.
- Ticket 49298 - fix complier warn
- Ticket 49298 - Correct error codes with config restore.
- Ticket 49454 - SSL Client Authentication breaks in FIPS mode
- Ticket 49453 - passwd.py to use pwdhash defaults.
- Ticket 49427 - whitespace in fedse.c
- Ticket 49410 - opened connection can remain no longer poll, like hanging
- Ticket 48118 - fix compiler warning for incorrect return type
- Ticket 49451 - Add environment markers to lib389 dependencies
- Ticket 49325 - Proof of concept rust tqueue in sds
- Ticket 49443 - scope one searches in 1.3.7 give incorrect results
- Ticket 48118 - At startup, changelog can be erronously rebuilt after a normal shutdown
- Ticket 49412 - SIGSEV when setting invalid changelog config value
- Ticket 49441 - Import crashes - oneline fix
- Ticket 49377 - Incoming BER too large with TLS on plain port
- Ticket 49441 - Import crashes with large indexed binary  attributes
- Ticket 49435 - Fix NS race condition on loaded test systems
- Ticket 77 - lib389 - Refactor docstrings in rST format - part 2
- Ticket 17 - lib389 - dsremove support
- Ticket 3 - lib389 - python 3 compat for paged results test
- Ticket 3 - lib389 - Python 3 support for memberof plugin test suit
- Ticket 3 - lib389 - config test
- Ticket 3 - lib389 - python 3 support ds_logs tests
- Ticket 3 - lib389 - python 3 support for betxn test

* Fri Nov 3 2017 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.2-2
- Bump version to 1.4.0.2-2
- Add python-lib389 build requirements

* Fri Nov 3 2017 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.2-1
- Bump version to 1.4.0.2-1
- Ticket 48393 - fix copy and paste error
- Ticket 49439 - cleanallruv is not logging information
- Ticket 48393 - Improve replication config validation
- Ticket lib389 3 - Python 3 support for ACL test suite
- Ticket 103 - sysconfig not found
- Ticket 49436 - double free in COS in some conditions
- Ticket 48007 - CI test to test changelog trimming interval
- Ticket 49424 - Resolve csiphash alignment issues
- Ticket lib389 3 - Python 3 support for pwdPolicy_controls_test.py
- Ticket 3 - python 3 support - filter test
- Ticket 49434 - RPM build errors
- Ticket 49432 - filter optimise crash
- Ticket 49432 - Add complex fliter CI test
- Ticket 48894 - harden valueset_array_to_sorted_quick valueset  access
- Ticket 49401 - Fix compiler incompatible-pointer-types warnings
- Ticket 48681 - Use of uninitialized value in string ne at /usr/bin/logconv.pl
- Ticket 49409 - Update lib389 requirements
- Ticket 49401 - improve valueset sorted performance on delete
- Ticket 49374 -  server fails to start because maxdisksize is recognized incorrectly
- Ticket 49408 - Server allows to set any nsds5replicaid in the existing replica entry
- Ticket 49407 - status-dirsrv shows ellipsed lines
- Ticket 48681 - Use of uninitialized value in string ne at /usr/bin/logconv.pl
- Ticket 49386 - Memberof should be ignore MODRDN when the pre/post entry are identical
- Ticket 48006 - Missing warning for invalid replica backoff  configuration
- Ticket 49064 - testcase hardening
- Ticket 49064 - RFE allow to enable MemberOf plugin in dedicated consumer
- Ticket lib389 3 - python 3 support
- Ticket 49402 - Adding a database entry with the same database name that was deleted hangs server at shutdown
- Ticket 48235 - remove memberof lock (cherry-pick error)
- Ticket 49394 - build warning
- Ticket 49381 - Refactor numerous suite docstrings - Part 2
- Ticket 49394 - slapi_pblock_get may leave unchanged the provided variable
- Ticket 49403 - tidy ns logging
- Ticket 49381 - Refactor filter test suite docstrings
- Ticket 48235 - Remove memberOf global lock
- Ticket 103 - Make sysconfig where it is expected to exist
- Ticket 49400 - Add clang support to rpm builds
- Ticket 49381 - Refactor ACL test suite docstrings
- Ticket 49363 - Merge lib389
- Ticket 101 - BaseException.message has been deprecated in Python3
- Ticket 102 - referral support
- Ticket 99 - Fix typo in create_topology
- Ticket #98 - Fix dbscan output
- Ticket #77 - Fix changelogdb param issue
- Ticket #77 - Refactor docstrings in rST format - part 1
- Ticket 96 - Change binaries' names
- Ticket 77 - Add sphinx documentation
- Ticket 43 - Add support for Referential Integrity plugin
- Ticket 45 - Add support for Rootdn Access Control plugin
- Ticket 46 - dsconf support for dynamic schema reload
- Ticket 74 - Advice users to set referint-update-delay to 0
- Ticket 92 - display_attr() should return str not bytes in py3
- Ticket 93 - Fix test cases in ctl_dbtasks_test.py
- Ticket 88 - python install and remove for tests
- Ticket 85 - Remove legacy replication attribute
- Ticket 91 - Fix replication topology
- Ticket 89 - Fix inconsistency with serverid
- Ticket 79 - Fix replica.py and add tests
- Ticket 86 - add build dir to gitignore
- Ticket 83 - Add an util for generating instance parameters
- Ticket 87 - Update accesslog regec for HR etimes
- Ticket 49 - Add support for whoami plugin
- Ticket 48 - Add support for USN plugin
- Ticket 78 - Add exists() method to DSLdapObject
- Ticket 31 - Allow complete removal of some memberOf attrs
- Ticket31 - Add memberOf fix-up task
- Ticket 67 - Add ensure_int function
- Ticket 59 - lib389 support for index management.
- Ticket 67 - get attr by type
- Ticket 70 - Improve repl tools
- Ticket 50 - typo in db2* in dsctl
- Ticket 31 - Add status command and SkipNested support for MemberOf
- Ticket 31 - Add functional tests for MemberOf plugin
- Ticket 66 - expand healthcheck for Directory Server
- Ticket 69 - add specfile requires
- Ticket 31 - Initial MemberOf plugin support
- Ticket 50 - Add db2* tasks to dsctl
- Ticket 65 - Add m2c2 topology
- Ticket 63 - part 2, agreement test
- Ticket 63 - lib389 python 3 fix
- Ticket 62 - dirsrv offline log
- Ticket 60 - add dsrc to dsconf and dsidm
- Ticket 32 - Add TLS external bind support for testing
- Ticket 27 - Fix get function in tests
- Ticket 28 - userAccount for older versions without nsmemberof
- Ticket 27 - Improve dseldif API
- Ticket 30 - Add initial support for account lock and unlock.
- Ticket 29 - fix incorrect format in tools
- Ticket 28 - Change default objectClasses for users and groups
- Ticket 1 - Fix missing dn / rdn on config.
- Ticket 27 - Add a module for working with dse.ldif file
- Ticket 1 - cn=config comparison
- Ticket 21 - Missing serverid in dirsrv_test due to incorrect allocation
- Ticket 26 - improve lib389 sasl support
- Ticket 24 - Join paths using os.path.join instead of string concatenation
- Ticket 25 - Fix RUV __repr__ function
- Ticket 23 - Use DirSrv.exists() instead of manually checking for instance's existence
- Ticket 1 - cn=config comparison
- Ticket 22 - Specify a basedn parameter for IDM modules
- Ticket 19 - missing readme.md in python3
- Ticket 20 - Use the DN_DM constant instead of hard coding its value
- Ticket 19 - Missing file and improve make
- Ticket 14 - Remane dsadm to dsctl
- Ticket 16 - Reset InstScriptsEnabled argument during the init
- Ticket 14 - Remane dsadm to dsctl
- Ticket 13 - Add init function to create new domain entries
- Ticket 15 - Improve instance configuration ability
- Ticket 10 - Improve command line tool arguments
- Ticket 9 - Convert readme to MD
- Ticket 7 - Add pause and resume methods to topology fixtures
- Ticket 49172 - Allow lib389 to read system schema and instance
- Ticket 49172 - Allow lib389 to read system schema and instance
- Ticket 6 - Bump lib389 version 1.0.4
- Ticket 5 - Fix container build on fedora
- Ticket 4 - Cert detection breaks some tests
- Ticket 49137 - Add sasl plain tests, lib389 support
- Ticket 2 - pytest mark with version relies on root
- Ticket 49126 - DIT management tool
- Ticket 49101 - Python 2 generate example entries
- Ticket 49103 - python 2 support for installer
- Ticket 47747 - Add topology_i2 and topology_i3
- Ticket 49087 - lib389 resolve jenkins issues
- Ticket 48413 - Improvements to lib389 for rest
- Ticket 49083 - Support prefix for discovery of the defaults.inf file.
- Ticket 49055 - Fix debugging mode issue
- Ticket 49060 - Increase number of masters, hubs and consumers in topology
- Ticket 47747 - Add more topology fixtures
- Ticket 47840 - Add InstScriptsEnabled argument
- Ticket 47747 - Add topology fixtures module
- Ticket 48707 - Implement draft-wibrown-ldapssotoken-01
- Ticket 49022 - Lib389, py3 installer cannot create entries in backend
- Ticket 49024 - Fix paths to the dbdir parent
- Ticket 49024 - Fix db_dir paths
- Ticket 49024 - Fix paths in tools module
- Ticket 48961 - Fix lib389 minor issues shown by 48961 test
- Ticket 49010 - Lib389 fails to start with systemctl changes
- Ticket 49007 - lib389 fixes for paths to use online values
- Ticket 49005 - Update lib389 to work in containers correctly.
- Ticket 48991 - Fix lib389 spec for python2 and python3
- Ticket 48984 - Add lib389 paths module
- Ticket 48951 - dsadm dsconfig status and plugin
- Ticket 47957 - Update the replication "idle" status string
- Ticket 48951 - dsadm and dsconf base files
- Ticket 48952 - Restart command needs a sleep
- Ticket 48949 - Fix ups for style and correctness
- Ticket 48949 - added copying slapd-collations.conf
- Ticket 48949 - change default file path generation - use os.path.join
- Ticket 48949 - os.makedirs() exist_ok not python2 compatible, added try/except
- Ticket 48949 - configparser fallback not python2 compatible
- Ticket 48946 - openConnection should not fully popluate DirSrv object
- Ticket 48832 - Add DirSrvTools.getLocalhost() function
- Ticket 48382 - Fix serverCmd to get sbin dir properly
- Bug 1347760 - Information disclosure via repeated use of LDAP ADD operation, etc.
- Ticket 48937 - Cleanup valgrind wrapper script
- Ticket 48923 - Fix additional issue with serverCmd
- Ticket 48923 - serverCmd timeout not working as expected
- Ticket 48917 - Attribute presence
- Ticket 48911 - Plugin improvements for lib389
- Ticket 48911 - Improve plugin support based on new mapped objects
- Ticket 48910 - Fixes for backend tests and lib389 reliability.
- Ticket 48860 - Add replication tools
- Ticket 48888 - Correction to create of dsldapobject
- Ticket 48886 - Fix NSS SSL library in lib389
- Ticket 48885 - Fix spec file requires
- Ticket 48884 - Bugfixes for mapped object and new connections
- Ticket 48878 - better style for backend in backend_test.py
- Ticket 48878 - pep8 fixes part 2
- Ticket 48878 - pep8 fixes and fix rpm to build
- Ticket 48853 - Prerelease installer
- Ticket 48820 - Begin to test compatability with py.test3, and the new orm
- Ticket 48434 - Fix for negative tz offsets
- Ticket 48857 - Remove python-krbV from lib389
- Ticket 48820 - Fix tests to ensure they work with the new object types
- Ticket 48820 - Move Encryption and RSA to the new object types
- Ticket 48820 - Proof of concept of orm style mapping of configs and objects
- Ticket 48820 - Clitool rename
- Ticket 48431 - lib389 integrate ldclt
- Ticket 48434 - lib389 logging tools
- Ticket 48796 - add function to remove logs
- Ticket 48771 - lib389 - get ns-slapd version
- Ticket 48830 - Convert lib389 to ip route tools
- Ticket 48763 - backup should run regardless of existing backups.
- Ticket 48434 - lib389 logging tools
- Ticket 48798 - EL6 compat for lib389 tests for DH params
- Ticket 48798 - lib389 add ability to create nss ca and certificate
- Ticket 48433 - Aci linting tools
- Ticket 48791 - format args in server tools
- Ticket 48399 - Helper makefile is missing mkdir dist
- Ticket 48399 - Helper makefile is missing mkdir dist
- Ticket 48794 - lib389 build requires are on a single line
- Ticket 48660 - Add function to convert binary values in an entry to base64
- Ticket 48764 - Fix mit krb password to be random.
- Ticket 48765 - Change default ports for standalone topology
- Ticket 48750 - Clean up logging to improve command experience
- Ticket 48751 - Improve lib389 ldapi support
- Ticket 48399 - Add helper makefile to lib389 to build and install
- Ticket 48661 - Agreement test suite fails at the test_changes case
- Ticket 48407 - Add test coverage module for lib389 repo
- Ticket 48357 - clitools should standarise their args
- Ticket 48560 - Make verbose handling consistent
- Ticket 48419 - getadminport() should not a be a static method
- Ticket 48408 - RFE escaped default suffix for tests
- Ticket 48401 - Revert typecheck
- Ticket 48401 - lib389 Entry hasAttr returs dict instead of false
- Ticket 48390 - RFE Improvements to lib389 monitor features for rest389
- Ticket 48358 - Add new spec file
- Ticket 48371 - weaker host check on localhost.localdomain
- Ticket 58358 - Update spec file with pre-release versioning
- Ticket 48358 - Make Fedora packaging changes to the spec file
- Ticket 48358 - Prepare lib389 for Fedora Packaging
- Ticket 48364 - Fix test failures
- Ticket 48360 - Refactor the delete agreement function
- Ticket 48361 - Expand 389ds monitoring capabilities
- Ticket 48246 - Adding license/copyright to lib389 files
- Ticket 48340 - Add basic monitor support to lib389 https://fedorahosted.org/389/ticket/48340
- Ticket 48353 - Add Replication REST support to lib389
- Ticket 47840 - Fix regression
- Ticket 48343 - lib389 krb5 realm management https://fedorahosted.org/389/ticket/48343
- Ticket 47840 - fix lib389 to use sbin scripts  https://fedorahosted.org/389/ticket/47840
- Ticket 48335 - Add SASL support to lib389
- Ticket 48329 - Fix case-senstive scyheam comparisions
- Ticket 48303 - Fix lib389 broken tests
- Ticket 48329 - add matching rule functions to schema module
- Ticket 48324 - fix boolean capitalisation (one line) https://fedorahosted.org/389/ticket/48324
- Ticket 48321 - Improve is_a_dn check to prevent mistakes with lib389 auth https://fedorahosted.org/389/ticket/48321
- Ticket 48322 - Allow reindex function to reindex all attributes
- Ticket 48319 - Fix ldap.LDAPError exception processing
- Ticket 48318 - Do not delete a changelog while disabling a replication by suffix
- Ticket 48308 - Add __eq__ and __ne__ to Entry to allow fast comparison https://fedorahosted.org/389/ticket/48308
- Ticket 48303 - Fix lib389 broken tests - backend_test
- Ticket 48309 - Fix lib389 lib imports
- Ticket 48303 - Fix lib389 broken tests - agreement_test
- Ticket 48303 - Fix lib389 broken tests - aci_parse_test
- Ticket 48301 - add tox support
- Ticket 48204 - update lib389 for python3
- Ticket 48273 - Improve valgrind functions
- Ticket 48271 - Fix for self.prefix being none when SER_DEPLOYED_DIR is none https://fedorahosted.org/389/ticket/48271
- Ticket 48259 - Add aci parsing utilities to lib389
- Ticket 48252 - (lib389) adding get_bin_dir and dbscan
- Ticket 48247 - Change the default user to 'dirsrv'
- Ticket 47848 - Add new function to create ldif files
- Ticket 48239 - Fix for prefix allocation of un-initialised dirsrv objects
- Ticket 48237 - Add lib389 helper to enable and disable logging services.
- Ticket 48236 - Add get effective rights helper to lib389
- Ticket 48238 - Add objectclass and attribute type query mechanisms
- Ticket 48029 - Add missing replication related functions
- Ticket 48028 - add valgrind wrapper for ns-slapd
- Ticket 48028 - lib389 - add valgrind functions
- Ticket 48022 - lib389 - Add all the server tasks
- Ticket 48023 - create function to test replication between servers
- Ticket 48020 - lib389 - need to reset args_instance with  every DirSrv init
- Ticket 48000 - Repl agmts need more time to stop
- Ticket 48004 - Fix various issues
- Ticket 48000 - replica agreement pause/resume should have a short sleep
- Ticket 47990 - Add check for ".removed" instances when doing an upgrade
- Ticket 47990 - Add "upgrade" function to lib389
- Ticket 47691 - using lib389 with RPMs
- Ticket 47848 - Add support for setuptools.
- Ticket 47855 - Add function to clear tmp directory
- Ticket 47851 - Need to retrieve tmp directory path
- Ticket 47845 - add stripcsn option to tombstone fixup task
- Ticket 47851 - Add function to retrieve dirsrvtests data directory
- Ticket 47845 - Add backup/restore/fixup tombstone tasks to lib389
- Ticket 47819 - Add the new precise tombstone purging config attribute
- Ticket 47695 - Add plugins/tasks/Index
- Ticket 47648 - lib389 - add schema classes, methods
- Ticket 47671 - CI lib389: allow to open a DirSrv without having to create the instance
- Ticket 47600 - Replica/Agreement/Changelog not conform to the design
- Ticket 47652 - replica add fails: MT.list return a list not an entry
- Ticket 47635 - MT/Backend/Suffix to be conform with the design
- Ticket 47625 - CI lib389: DirSrv not conform to the design
- Ticket 47595 - fail to detect/reinit already existing instance/backup
- Ticket 47590 - CI tests: add/split functions around replication
- Ticket 47584 - CI tests: add backup/restore of an instance
- Ticket 47578 - CI tests: removal of 'sudo' and absolute path in lib389
- Ticket 47568 - Rename DSAdmin class
- Ticket 47566 - Initial import of DSadmin into 389-test repos

* Mon Oct 16 2017 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.1-2
- Bump version to 1.4.0.1-2
- Ticket 49400 - Add clang support and libatomic

* Mon Oct 9 2017 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.1-1
- Bump version to 1.4.0.1-1
- Ticket 49038 - remove legacy replication - change cleanup script precedence
- Ticket 49392 - memavailable not available
- Ticket 49235 - pbkdf2 by default
- Ticket 49279 - remove dsktune
- Ticket 49372 - filter optimisation improvements for common queries
- Ticket 49320 - Activating already active role returns error 16
- Ticket 49389 - unable to retrieve specific cosAttribute when subtree password policy is configured
- Ticket 49092 - Add CI test for schema-reload
- Ticket 49388 - repl-monitor - matches null string many times in regex
- Ticket 49387 - pbkdf2 settings were too aggressive
- Ticket 49385 - Fix coverity warnings
- Ticket 49305 - Need to wrap atomic calls
- Ticket 48973 - Indexing a ExactIA5Match attribute with a IgnoreIA5Match matching rule triggers a warning
- Ticket 49378 - server init fails
- Ticket 49305 - Need to wrap atomic calls
- Ticket 49180 - add CI test
- Ticket 49180 - errors log filled with attrlist_replace - attr_replace

* Fri Sep 22 2017 Mark Reynolds <mreynolds@redhat.com> - 1.4.0.0-1
- Bump version to 1.4.0.0-1

* Wed Sep 6 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.7.4-1
- Bump version to 1.3.7.4
- Ticket 49371 - Cleanup update script
- Ticket 48831 - Autotune dncache with entry cache.
- Ticket 49312 - pwdhash -D used default hash algo
- Ticket 49043 - make replication conflicts transparent to clients
- Ticket 49371 - Fix rpm build
- Ticket 49371 - Template dse.ldif did not contain all needed plugins
- Ticket 49295 - Fix CI Tests
- Ticket 49050 - make objectclass ldapsubentry effective immediately

* Fri Sep 1 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.7.3-1
- Bump version to 1.3.7.3
- Ticket 49354 - fix regression in total init due to mistake in range fetch
- Ticket 49370 - local password policies should use the same defaults as the global policy
- Ticket 48989 - Delete slow lib389 test
- Ticket 49367 - missing braces in idsktune
- Ticket 49364 - incorrect function declaration.
- Ticket 49275 - fix tls auth regression
- Ticket 49038 - Revise creation of cn=replication,cn=config
- Ticket 49368 - Fix typo in log message
- Ticket 48059 - Add docstrings to CLU tests
- Ticket 47840 - Add docstrings to setup tests
- Ticket 49348 - support perlless and wrapperless install

* Tue Aug 22 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.7.2-1
- Bump verison to 1.3.7.2
- Ticket 49038 - Fix regression from legacy code cleanup
- Ticket 49295 - Fix CI tests
- Ticket 48067 - Add bugzilla tests for ds_logs
- Ticket 49356 - mapping tree crash can occur during tot init
- Ticket 49275 - fix compiler warns for gcc 7
- Ticket 49248 - Add a docstring to account locking test case
- Ticket 49445 - remove dead code
- Ticket 48081 - Add regression tests for pwpolicy
- Ticket 48056 - Add docstrings to basic test suite
- Ticket 49349 - global name 'imap' is not defined
- Ticket 83 - lib389 - Fix tests and create_test.py
- Ticket 48185 - Remove referint-logchanges attr from referint's config
- Ticket 48081 - Add regression tests for pwpolicy
- Ticket 83 - lib389 - Replace topology agmt objects
- Ticket 49331 - change autoscaling defaults
- Ticket 49330 - Improve ndn cache performance.
- Ticket 49347 - reproducable build numbers
- Ticket 39344 - changelog ldif import fails
- Ticket 49337 - Add regression tests for import tests
- Ticket 49309 - syntax checking on referint's delay attr
- Ticket 49336 - SECURITY: Locked account provides different return code
- Ticket 49332 - Event queue is not working
- Ticket 49313 - Change the retrochangelog default cache size
- Ticket 49329 - Descriptive error msg for USN cleanup task
- Ticket 49328 - Cleanup source code
- Ticket 49299 - Add normalized dn cache stats to dbmon.sh
- Ticket 49290 - improve idl handling in complex searches
- Ticket 49328 - Update clang-format config file
- Ticket 49091 - remove usage of changelog semaphore
- Ticket 49275 - shadow warnings for gcc7 - pass 1
- Ticket 49316 - fix missing not condition in clock cleanu
- Ticket 49038 - Remove legacy replication
- Ticket 49287 - v3 extend csnpl handling to multiple backends
- Ticket 49310 - remove sds logging in debug builds
- Ticket 49031 - Improve memberof with a cache of group parents
- Ticket 49316 - Fix clock unsafety in DS
- Ticket 48210 - Add IP addr and connid to monitor output
- Ticket 49295 - Fix CI tests and compiler warnings
- Ticket 49295 - Fix CI tests
- Ticket 49305 - Improve atomic behaviours in 389-ds
- Ticket 49298 - fix missing header
- Ticket 49314 - Add untracked files to the .gitignore
- Ticket 49303 - Fix error in CI test
- Ticket 49302 - fix dirsrv importst due to lib389 change
- Ticket 49303 - Add option to disable TLS client-initiated renegotiation
- Ticket 49298 - force sync() on shutdown
- Ticket 49306 - make -f rpm.mk rpms produces build without tcmalloc enabled
- Ticket 49297 - improve search perf in bpt by removing a deref
- Ticket 49284 - resolve crash in memberof when deleting attrs
- Ticket 49290 - unindexed range searches don't provide notes=U
- Ticket 49301 - Add one logpipe test case

* Fri Aug 11 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.3.7.1-2.5
- Rebuilt after RPM update (№ 3)

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.3.7.1-2.4
- Rebuilt for RPM soname bump

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.3.7.1-2.3
- Rebuilt for RPM soname bump

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.7.1-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.7.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 29 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.7.1-2
- Bump version to 1.3.7.1-2
- Fix specfile for python dependency issue with ds-replcheck

* Mon Jun 26 2017 Mark Reynolds <mreynoilds@redhat.com> - 1.3.7.1-1
- Bump verson to 1.3.7.1
- Ticket 49288 - RootDN Access wrong plugin path in template-dse.ldif.in
- Ticket 49289 - Improve result handling from connections with NS
- Ticket 49294 - radiusd before in unit file
- Ticket 49293 - inttypes in nunc-stans
- Ticket 49295 - Fix latest CI test failures
- Ticket 623 - Add test case and refactor the cleanallruv suite
- Ticket 49291 - slapi_search_internal_callback_pb may SIGSEV if related pblock has not operation set
- Ticket 49008 - Fix MO plugin betxn test
- Ticket 48944 - Add CI test case
- Ticket 49227 - ldapsearch does not return the expected Error log level
- Ticket 49028 - Add autotuning test suite
- Ticket 49281 - improve db2* tests
- Ticket 49273 - bak2db doesn't operate with dbversion
- Ticket 49184 - adjust logging level in MO plugin
- Ticket 49257 - Update CI script
- Ticket 49257 - only register modify callbacks
- Ticket 49008 - Adjust CI test for new memberOf behavior
- Ticket 49273 - Fix compiler warning in dbversion_write, missing newline
- Ticket 49277 - improve out of box system tuning for EL7
- Ticket 49273 - crash when DBVERSION is corrupt.
- Ticket 49273 - crash when DBVERSIOn is corrupt.
- Ticket 49268 - master branch fails on big endian systems
- Ticket 49271 - Fix pbkdf2 and openssl missing issue
- Ticket 49242 - add gdb script to rpm
- Ticket 49269 - Fix coverity errors
- Ticket 49241 - add symblic link location to db2bak.pl output
- Ticket #49072: memberOf fixup task does not validate args
- Ticket 49257 - Reject nsslapd-cachememsize & nsslapd-cachesize when nsslapd-cache-autosize is set
- Ticket 48538 - Failed to delete old semaphore
- Ticket 49231 - force EXTERNAL always
- Ticket 49267 - autosize split of 0 results in dbcache of 0
- Ticket 49099 - resolve systemd startup interaction with ns
- Ticket 49157 - fix error in ds-logpipe.py
- Ticket 48864 - remove config.h from spal header.
- Ticket 48681 - logconv.pl - Fix SASL Bind stats and rework report format
- Ticket 49261 - Fix script usage and man pages
- Ticket 49238 - AddressSanitizer: heap-use-after-free in libreplication
- Ticket 48864 - Fix FreeIPA build
- Ticket 49257 - Reject dbcachesize updates while auto cache sizing is enabled
- Ticket 49249 - cos_cache is erroneously logging schema checking failure
- Ticket 49248 - update eduPerson to 201602
- Ticket 48050 - Add a test case for an issue 49014
- Ticket 49258 - Allow nsslapd-cache-autosize to be modified while the server is running
- Ticket 49165 - Fix compiler warnings
- Ticket 49247 - resolve build issues on debian
- Ticket 48123 - create contrib section
- Ticket 49099 - fix configure.ac due to NS change
- Ticket 49250 - remove mempool experimental!
- Ticket 49099 - ns workers prep
- Ticket 49185 - Fix leaks in compute init and dblayer
- Ticket 49246 - ns-slapd crashes in role cache creation
- Ticket 49244 - resolve various test case issues
- Ticket 49157 - ds-logpipe.py crashes for non-existing users
- Ticket 49053 - Fix rpm build
- Ticket 49237 - Drop support for libdb older than 4.7
- Ticket 49053 - Enable flto for DS
- Ticket 49243 - segv in memberof fixup
- Ticket 48985 - Add schema for nested groups to work out of box.
- Ticket 49241 - Update man page and usage for db2bak.pl
- Ticket 49071 - Add test case to tickets
- Ticket 49075 - Adjust logging severity levels
- Ticket 47662 - db2index not properly evalauating arguments
- Ticket 49240 - ci compiler warns
- Ticket 48989 - fix perf counters
- Ticket 48681 - logconv.pl - fix sasl/bind stats
- Ticket 49097 - fix pblock whitespace
- Ticket 49097 - fix the pblock to be a hierachial structure
- Ticket 49239 - move ds-replcheck man page and add script
- Ticket 49239 - Add a tool to compare entries on LDAP servers.
- Ticket 49231 - fix sasl mech handling
- Ticket 49233 - Fix crash in persistent search
- Ticket 49225 - Fix CI Test
- Ticket 49230 - slapi_register_plugin creates config entry where it should not
- Ticket 49225 - Add additional CRYPT password storage schemes

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.6.6-3.23
- Perl 5.26 re-rebuild of bootstrapped packages

* Tue Jun 6 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.6-3.2
- Revise server upgrade logic

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.6.6-3.1
- Perl 5.26 rebuild

* Thu May 25 2017 Charalampos Stratakis <cstratak@redhat.com> - 1.3.6.6-3
- Bump verstion to 1.3.6.6-3
- Ensure the binaries are pointing to the Python 3 interpreter (rhbz#1244234)

* Mon May 22 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.6-2
- Bump version to 1.3.6.6-2
- Disable tcmalloc on ppc64 & ppc64le - crash in makstrdb during build

* Mon May 22 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.6-1
- Bump version to 1.3.6.6-1
- Ticket 49157 - fix error in ds-logpipe.py
- Ticket 48864 - remove config.h from spal header.
- Ticket 48681 - logconv.pl - Fix SASL Bind stats and rework report format
- Ticket 49261 - Fix script usage and man pages
- Ticket 49238 - AddressSanitizer: heap-use-after-free in libreplication
- Ticket 48864 - Fix FreeIPA build
- Ticket 49257 - Reject dbcachesize updates while auto cache sizing is enabled
- Ticket 49249 - cos_cache is erroneously logging schema checking failure
- Ticket 49258 - Allow nsslapd-cache-autosize to be modified while the server is running
- Ticket 49247 - resolve build issues on debian
- Ticket 49246 - ns-slapd crashes in role cache creation
- Ticket 49157 - ds-logpipe.py crashes for non-existing users
- Ticket 49241 - Update man page and usage for db2bak.pl
- Ticket 49075 - Adjust logging severity levels
- Ticket 47662 - db2index not properly evaluating arguments
- Ticket 48989 - fix perf counters

* Thu Apr 27 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.5-1
- Bump version to 1.3.6.5-1
- Ticket 49231 - fix sasl mech handling
- Ticket 49233 - Fix crash in persistent search
- Ticket 49230 - slapi_register_plugin creates config entry where it should not
- Ticket 49135 - PBKDF2 should determine rounds at startup
- Issue 49236 - Fix CI Tests
- Ticket 48310 - entry distribution should be case insensitive
- Ticket 49224 - without --prefix, $prefixdir would be NONE in defaults.

* Fri Apr 21 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.4-1
- Bump version to 1.3.6.4-1
- Ticket 49228 - Fix SSE4.2 detection.
- Ticket 49229 - Correct issues in latest commits
- Ticket 49226 - Memory leak in ldap-agent-bin
- Ticket 49214 - Implement htree concept
- Ticket 49119 - Cleanup configure.ac options and defines
- Ticket 49097 - whitespace fixes for pblock change
- Ticket 49097 - Pblock get/set cleanup
- Ticket 49222 - Resolve various test issues on rawhide
- Issue 48978 - Fix the emergency logging functions severity levels
- Issue 49227 - ldapsearch for nsslapd-errorlog-level returns  incorrect values
- Ticket 49041 - nss won't start if sql db type set
- Ticket 49223 - Fix sds queue locking
- Issue 49204 - Fix 32bit arch build failures
- Issue 49204 - Need to update function declaration
- Ticket 49204 - Fix lower bounds on import autosize + On small VM, autotune breaks the access of the suffixes
- Issue 49221 - During an upgrade the provided localhost name is ignored
- Issue 49220 - Remote crash via crafted LDAP messages (SECURITY FIX)
- Ticket 49184 - Overflow in memberof
- Ticket 48050 - Add account policy tests to plugins test suite
- Ticket 49207 - Supply docker POC build for DS.
- Issue 47662 - CLI args get removed
- Issue 49210 - Fix regression when checking is password min  age should be checked
- Ticket 48864 - Add cgroup memory limit detection to 389-ds
- Issue 48085 - Expand the repl acceptance test suite
- Ticket 49209 - Hang due to omitted replica lock release
- Ticket 48864 - Cleanup memory detection before we add cgroup support
- Ticket 48864 - Cleanup up broken format macros and imports
- Ticket 49153 - Remove vacuum lock on transaction cleanup
- Ticket 49200 - provide minimal dse.ldif for python installer
- Issue 49205 - Fix logconv.pl man page
- Issue 49177 - Fix pkg-config file
- Issue 49035 - dbmon.sh shows pages-in-use that exceeds the cache size
- Ticket 48432 - Linux capabilities on ns-slapd
- Ticket 49196 - Autotune generates crit messages
- Ticket 49194 - Lower default ioblock timeout
- Ticket 49193 - gcc7 warning fixes
- Issue 49039 - password min age should be ignored if password needs to be reset
- Ticket 48989 - Re-implement lock counter
- Issue 49192 - Deleting suffix can hang server
- Issue 49156 - Modify token :assert: to :expectedresults:
- Ticket 48989 - missing return in counter
- Ticket 48989 - Improve counter overflow fix
- Ticket 49190 - Upgrade lfds to 7.1.1
- Ticket 49187 - Fix attribute definition
- Ticket 49185 - Fix memleak in compute init

* Wed Mar 22 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.3-4
- Bump verson to 1.3.6.3-4
- Issue 49177 - rpm would not create valid pkgconfig files(pt2)

* Wed Mar 22 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.3-3
- Bump version to 1.3.6.3-3
- Ticket 49186 - Fix NS to improve shutdown relability
- Ticket 49174 - nunc-stans can not use negative timeout
- Ticket 49076 - To debug DB_DEADLOCK condition, allow to reset DB_TXN_NOWAIT flag on txn_begin
- Issue 49188 - retrocl can crash server at shutdown
- Ticket 47840 - Add setup_ds test suite

* Tue Mar 21 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.3-2
- Bump version to 1.3.6.3-2
- Fix srvcore version dependancy

* Tue Mar 21 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.3-1
- Bump verson to 1.3.6.3
- Issue 48989 - Overflow in counters and monitor
- Issue 49095 - targetattr wildcard evaluation is incorrectly case sensitive
- Ticket 49177 - rpm would not create valid pkgconfig files
- Issue 49176 - Remove tcmalloc restriction from s390x
- Issue 49157 - ds-logpipe.py crashes for non-existing users
- Issue 49065 - dbmon.sh fails if you have nsslapd-require-secure-binds enabled
- Issue 49095 - Fix double-free in _cl5NewDBFile() error path

* Wed Mar 15 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.2-2
- Bump verson to 1.3.6.2-2
- Issue 49169 - Fix covscan errors(regression)
- Ticket 49172 - Fix test schema files
- Ticket 49171 - Nunc Stans incorrectly reports a timeout
- Ticket 49171 - Nunc Stans incorrectly reports a timeout
- Issue 49169 - Fix covscan errors

* Tue Mar 14 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.2-1
- Bump version to 1.3.6.2-1
- Ticket 49164 - Change NS to acq-rel semantics for atomics
- Ticket 49154 - Nunc Stans stress should assert it has 95% success rate
- Ticket 49165 - pw_verify did not handle external auth
- Issue 49062 - Reset agmt update staus and total init
- Ticket 49151 - Remove defunct selinux policy

* Fri Mar 10 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-2
- Bump version to 1.3.6.1-2
- Issue 49162 - Only check event.m4 if nunc-stans is enabled
- Issue 49156 - Add more IDs and fix docstrings
- Issue 49156 - Fix typo in the import
- Ticket 49160 - Fix sds benchmark and copyright
- Issue 47536 - Fix CI testcase
- Issue 49159 - test_schema_comparewithfiles fails with python-ldap>=2.4.26
- Issue 49156 - Clean up test suites dir structure and docstrings
- Issue 49158 - fix latest coverity issues
- Ticket 49155 - Fix db2ldif path in test
- Issue 49122 - Fix rpm build
- Issue 49044 - Fix script usage and man pages
- Ticket 48707 - Update rfc to accomodate that authid is mandatory
- Ticket 49141 - Enable tcmalloc
- Ticket 49142 - bytes vs unicode in plugin tests
- Ticket 49139 - Update makefile and rpm for import
- Ticket 49139 - Import libsds and nunc-stans for bundling
- Issue 49122 - Filtered nsrole that uses nsrole crashes the  server
- Issue 49147 - Fix tests compatibility with older versions
- Issue 49141 - Fix spec file for tcmalloc
- Issue 49141 - Use tcmalloc by default
- Ticket 49086 - SDN premangaling broken after SASL change
- Ticket 49137 - Add sasl plain test - ds
- Ticket 49138 - Increase systemd timout
- Issue 48226 - Fix CI test
- Ticket 49140 - Remove legacy inst reference in test
- Ticket 49134  Remove hardcoded elements from db lock test
- Fix compiler warning
- Ticket 47925 - Move add and delete operation aci checks to be before plugins.
- Ticket 49086 - public api compatability test for SDN changes.
- Ticket 49116 - Pblock usage analytics
- Ticket 49020 - Add CI test
- Revise README for pagure
- Ticket #49121 - ns-slapd crashes in ldif_sput due to the output buf size is less than the real size.
- Ticket 48085 - Add replica acceptance test suite
- Ticket 49008 - Fix regression in check if ruv element exists
- Ticket 49108 - ds_selinux_port_query doesn't detect ports labeled with range
- Ticket 49057 - Fix tests failures on older versions of DS
- Ticket 49111 - Integrate cmocka skeleton to Directory Server
- Ticket 49016 - (un)register/migration/remove may fail if there is no suffix on 'userRoot' backend
- Ticket 48085 - Add single master replication test suite
- Ticket #49104 - Add CI test
- Ticket #49104 - dbscan-bin crashing due to a segmentation fault
- Ticket 49105 - Sig FPE when ns-slapd has 0 backends.
- Ticket 49075 - Adjust log severity levels
- Ticket 49008 - Add CI test
- Ticket 49008 v2: aborted operation can leave RUV in incorrect state
- Ticket 47973 - CI Test case (test_ticket47973_case)
- Ticket 47973 - CI Test case (test_ticket47973_case)
- Ticket 47973 - custom schema is registered in small caps after schema reload
- Ticket 49089 - List library build deps
- Ticket 49085 - Make a short topology fixture alias
- Ticket #49088 - 389-ds-base rpm postinstall script bugs
- Ticket 49028 - Autosize database cache by default.
- Ticket 49089 - Fix invalid cxxlink statement from hpux
- Ticket 49087 - ds resolve jenkins issues.
- Ticket #49082 - Adjusted the CI test case to the fix.
- Ticket #49082 - Fix password expiration related shadow attributes
- Ticket #49080 - shadowExpire should not be a calculated value
- Ticket 49027 - on secfailure do not store cleartext password content
- Ticket 49031 - Improve memberof with a cache of ancestors for groups
- Ticket 49079: deadlock on cos cache rebuild
- Ticket 48665 - Fix RHEL6 test compatibility issues
- Ticket 49055 - Fix create_test.py issues
- Ticket 48797 - Add freebsd support to ns-slapd: main
- Ticket 49055 - Refactor create_test.py
- Ticket 49060 - Increase number of masters, hubs and consumers in topology
- Ticket 49055 - Clean up test tickets and suites
- Ticket 48964 - should not free repl name after purging changelog
- Ticket 48050 - Refactor acctpolicy_plugin suite
- Ticket 48964 - cleanallruv changelog purging removes wrong  rid
- Ticket 49073: nsDS5ReplicatedAttributeListTotal fails when excluding no attribute
- Ticket 49074 - incompatible nsEncryptionConfig object definition prevents RHEL 7->6 schema replication
- Ticket 48835 - package tests into python site packages - fix rpm
- Ticket 49066 - Memory leaks in server - part 2
- Ticket 49072 - validate memberof fixup task args
- Ticket 49071 - Import with duplicate DNs throws unexpected errors
- Ticket 47858 - Add test case for nsTombstone
- Ticket 48835 - Tests with setup.py.in
- Ticket 49066 - Memory leaks in server
- Ticket 47982 - Add CI test suite ds_logs
- Ticket 49052 - Environment quoting on fedora causes ds to fail to start.
- Ticket 47662 - Better input argument validation and error messages for cli tools
- Ticket 48681 - logconv.pl lists sasl binds with no dn as anonymous
- Ticket 48861: memberof plugin tests suite
- Ticket 48861: Memberof plugins can update several times the same entry to set the same values
- Ticket 48163 - Re-space schema.c
- Ticket 48163 - Read schema from multiple locations
- Ticket 48894 - improve entrywsi delete
- Ticket 49051 - Enable SASL LOGIN/PLAIN support as a precursor to LDAPSSOTOKEN
- Ticket 49020 - do not treat missing csn as fatal
- Ticket 48133 v2 Non tombstone entry which dn starting with "nsuniqueid=...," cannot be delete
- Ticket 49055 - Clean up test suites
- Ticket 48797 - Add freebsd support to ns-slapd: Configure and makefile.
- Ticket 48797 - Add freebsd support to ns-slapd: Add freebsd support for ldaputil
- Ticket 48797 - Add freebsd support to ns-slapd: Add support for dsktune
- Ticket 48797 - Add freebsd support to ns-slapd: Add support for cpp in Fbsd
- Ticket 48797 - Add freebsd support to ns-slapd: Header files
- Ticket 48978 - Fix implicit function declaration
- Ticket 49002 - Remove memset on allocation
- Ticket 49021 - Automatic thread tuning
- Ticket 48894 - Issues with delete of entrywsi with large entries.
- Ticket 49054 - Fix sasl_map unused paramater compiler warnings.
- Ticket 48050 - Add test suite to acctpolicy_plugin
- Ticket 49048 - Fix rpm build failure
- Ticket 49042 - Test failure that expects old default
- Ticket 49042 - Increase cache defaults slightly
- Ticket 48894 - Issue with high number of entry state objects.
- Ticket 48978 - Fix more log refactoring issues
- Ticket 48707 - Draft Ldap SSO Token proposal
- Ticket 49024 - Fix the rest of the CI failures
- Ticket #48987 - Heap use after free in dblayer_close_indexes
- Ticket 48945 - Improve db2ldif error message.
- Ticket 49024 - Fix inst_dir parameter in defaults.inf
- Ticket 49024 - Fix dbdir paths and adjust test cases
- Ticket 48961 - Allow reset of configuration values to defaults.
- Ticket #47911 - Move dirsrv-snmp.service to 389-ds-base-snmp package
- Ticket bz1358565 - Fix compiler warning about unused variable
- Ticket bz1358565 -  clear and unsalted password types are vulnerable to timing attack
- Ticket 49016 - (un)register/migration/remove may fail if there is no suffix on 'userRoot' backend
- Ticket 397 - Add PBKDF2 to Directory Server password storage.
- Ticket 49024 - Fix CI test failures and defaults.inf
- Ticket 49026 - Support nunc-stans pkgconfig
- Ticket 49025 - Upgrade nunc-stans to 0.2.1
- Ticket 48978 - error log refactoring error

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.6.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Oct 27 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.6.1-0
- Bump version to 1.3.6.1-1
- Ticket 142   - Refactor and move CI test
- Ticket 47703 - remove search limit for aci group evaluation
- Ticket 47978 - Refactor slapi_log_error
- Ticket 48272 - ADDN Sytle prebind plugin
- Ticket 48272 - Fix compiler warnings for addn
- Ticket 48278 - cleanAllRUV should remove keep-alive entry
- Ticket 48328 - Add missing dependency
- Ticket 48414 - cleanAllRUV should clean the agreement RUV
- Ticket 48538 - Failed to delete old semaphore
- Ticket 48805 - Misleading indent and Uninitialised struct member
- Ticket 48805 - Sign comparison checks.
- Ticket 48832 - Fix CI test suite for password min age
- Ticket 48896 - CI test: test case for ticket 48896
- Ticket 48896 - Default Setting for passwordMinTokenLength does not work
- Ticket 48906 - Allow nsslapd-db-locks to be configurable online
- Ticket 48909 - Replication stops working in FIPS mode
- Ticket 48921 - CI Replication stress tests have limits set too low
- Ticket 48944 - on a read only replica invalid state info can accumulate
- Ticket 48947 - Update default password hash to SSHA512
- Ticket 48957 - Update repl-monitor to handle new status messages
- Ticket 48969 - nsslapd-auditfaillog always has an explicit path
- Ticket 48978 - Build fails on i686
- Ticket 48978 - Convert slapi_log_error() to a variadic macro
- Ticket 48978 - Fine tune error logging
- Ticket 48978 - Fix CI test to account for new logging format
- Ticket 48978 - Fix logging format errors and replace LDAP_DEBUG
- Ticket 48978 - refactor LDADebug() to slapi_log_err()
- Ticket 48978 - refactor LDAPDebug()
- Ticket 48978 - Update error logging with new codes
- Ticket 48978 - Update the logging function to accept sev level
- Ticket 48979 - Allow to compile 389ds with warning Wstrict-prototypes
- Ticket 48979 - Strict Prototypes
- Ticket 48982 - Comment about resolving failure to open plugin.
- Ticket 48982 - Enabling a plugin that has a versioned so causes overflow
- Ticket 48982 - One line fix, remove unused variable.
- Ticket 48982 - When plugin doesn't enable, actually log the path it used
- Ticket 48983 - Configure and Makefile.in from new default paths work.
- Ticket 48983 -  generate install path info from autotools scripts
- Ticket 48984 - Add lib389 paths module
- Ticket 48986 - 47808 triggers overflow in uiduniq.c
- Ticket 48992 - Total init may fail if the pushed schema is rejected
- Ticket 48996 - Fix rpm to work with ns 0.2.0
- Ticket 48996 - remove unused variable.
- Ticket 48996 - update DS for ns 0.2.0
- Ticket 49005 - Update lib389 to work in containers correctly.
- Ticket 49006 - Enable nunc-stans by default.
- Ticket 49006 - Nunc stans use DS stack size
- Ticket 49007 - Update configure scripts
- Ticket 49007 - Update DS basic test to better work with systemd.
- Ticket 49009 - args debug logging must be more restrictive
- Ticket 49011 - Remove configure artifacts
- Ticket 49012 - Removed un-used counters
- Ticket 49013 - Correct signal handling with NS in DS
- Ticket 49014 - ns-accountstatus.pl shows wrong status for accounts inactivated by Account policy plugin
- Ticket 49017 - Various minor test failures
- use a consumer maxcsn only as anchor if supplier is more advanced

* Mon Oct 24 2016 Mark Reynolds <mreynolds@redhat.com> - 1.3.5.14-2
- Bump version to 1.3.5.14-2
- Ticket 49011 - Remove configure artifacts
- Ticket 49006 - Enable nunc-stans 0.2.0 by default

* Thu Oct 13 2016 Mark Reynolds <mreynolds@redhat.com> - 1.3.5.14-1
- Bump version to 1.3.5.14-1
- Ticket 48992 - Total init may fail if the pushed schema is rejected
- Ticket 48832 - Fix CI test suite for password min age
- Ticket 48983 - Configure and Makefile.in from new default paths work.
- Ticket 48983 - Configure and Makefile.in from new default paths work.
- Ticket 48983 - generate install path info from autotools scripts
- Ticket 48944 - on a read only replica invalid state info can accumulate
- Ticket 48766 - use a consumer maxcsn only as anchor if supplier is more advanced
- Ticket 48921 - CI Replication stress tests have limits set too low
- Ticket 48969 - nsslapd-auditfaillog always has an explicit path
- Ticket 48957 - Update repl-monitor to handle new status messages
- Ticket 48832 - Fix CI tests
- Ticket 48975 - Disabling CLEAR password storage scheme will  crash server when setting a password
- Ticket 48369 - Add CI test suite
- Ticket 48970 - Serverside sorting crashes the server
- Ticket 48972 - remove old pwp code that adds/removes ACIs
- Ticket 48957 - set proper update status to replication  agreement in case of failure
- Ticket 48950 - Add systemd warning to the LD_PRELOAD example in /etc/sysconfig/dirsrv
- provide backend dir in suffix template
- Ticket 48953 - Skip labelling and unlabelling ports during the test
- Ticket 48967 - Add CI test and refactor test suite
- Ticket 48967 - passwordMinAge attribute doesn't limit the minimum age of the password
- Fix jenkins warnings about unused vars
- Ticket 48402 - v3 allow plugins to detect a restore or import
- Ticket #48969 - nsslapd-auditfaillog always has an explicit path
- Ticket 48964 - cleanAllRUV changelog purging incorrectly  processes all backends
- Ticket 48965 - Fix building rpms using rpm.mk
- Ticket 48965 - Fix generation of the pre-release version
- Bugzilla 1368956 - man page of ns-accountstatus.pl shows redundant entries for -p port option
- Ticket 48960 - Crash in import_wait_for_space_in_fifo().
- Ticket 48832 - Fix more CI test failures
- Ticket 48958 - Audit fail log doesn't work if audit log disabled.
- Ticket 48956 - ns-accountstatus.pl showing "activated" user even if it is inactivated
- Ticket 48954 - replication fails because anchorcsn cannot be found
- Ticket 48832 - Fix CI tests failures from jenkins server
- Ticket 48950 - Change example in /etc/sysconfig/dirsrv to use tcmalloc


* Mon Aug  8 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.13-1
- Release 1.3.5.13-1
- Ticket 48450 - Autotools components for ds_systemd_ask_password_acl

* Thu Aug  4 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.12-1
- Release 1.3.5.12-1
- Ticket 48450 - Add prestart work around for systemd ask password
- Ticket 48943 - When fine-grained policy is applied, a sub-tree has a priority over a user while changing password
- Ticket 47976 - Add fixed CI test case
- Ticket 48882 - server can hang in connection list processing
- Ticket 48921 - Adding replication and reliability tests
- Ticket 48936 - Duplicate collation entries
- Ticket 48832 - Fix timing and localhost issues
- Ticket 48832 - Fix pytest compatibility in CI tests
- Ticket 48832 - CI Tests - make tests more portable
- Ticket 48943 - Add CI Test for the password test suite
- Ticket 48940 - DS logs have warning:ancestorid not indexed
- Ticket 48934 - remove-ds.pl deletes an instance even if wrong prefix was specified
- Ticket 48336 - Missing semanage dependency
- Bug 1347760 - Additional CI test case
- Resolves: Bug 1347760 - CVE-2016-4992 389-ds-base: Information disclosure via repeated use of LDAP ADD operation, etc.
- Ticket 48832 - CI tests - convert all the tests to use  py.test
- Ticket 48939 - nsslapd-workingdir is empty when ns-slapd is started by systemd
- Ticket 48935 - Update dirsrv.systemd file
- Ticket 48832 - Fix lib389 CI ticket/suite test failures
- Ticket 47824 - Remove CI test from tickets and add logging
- Ticket 48930 - Paged result search can hang the server
- Ticket 48191 - Move CI test to the pr suite and refactor
- Ticket 48928 - log of page result cookie should log empty cookie with a different value than 0
- Ticket 48752 - Add CI test
- Ticket 47664 - Move CI test to the pr suite and refactor

* Thu Jul 14 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.11-1
- Release 1.3.5.11-1
- Ticket 48144 - Add /usr/sbin/status-dirsrv script to get the status of the directory server instance.
- Ticket 48743 - If a cipher is disabled do not attempt to look it up
- Ticket 48755 - moving an entry could make the online init fail
- Ticket 48767 - flow control in replication also blocks receiving results
- Ticket 48912 - ntUserNtPassword schema
- Ticket 48914 - db2bak.pl task enters infinitive loop when bak fs is almost full
- Ticket 48916 - DNA Threshold set to 0 causes SIGFPE
- Ticket 48918 - Upgrade to 389-ds-base >= 1.3.5.5 doesn't install 389-ds-base-snmp
- Ticket 48919 - Compiler warnings while building 389-ds-base on RHEL7
- Ticket 48920 - Memory leak in pwdhash-bin
- Ticket 48922 - Fix crash when deleting backend while import is running
- Ticket 48924 - Fixup tombstone task needs to set proper flag when updating tombstones
- Ticket 48925 - slapd crash with SIGILL: Dsktune should detect lack of CMPXCHG16B
- Bug 1347761  - CVE-2016-4992 389-ds-base: Information disclosure via repeated use of LDAP ADD operation, etc.
- Bug 1353956  - Upgrade from FreeIPA Fedora 23 container to Fedora 24 fails with syntax error at
                 /usr/share/dirsrv/updates/91reindex.pl line 17, near ")
                 Regression introduced by Ticket 48755 to 1.3.5.10-1.
- Bug 1350393  - setup-ds.pl fails on F24 if perl-Errno is not updated (DS 48901)
- Bug 1114928  - etup-ds.pl creates configuration files under /usr (DS 528, 47840)

* Fri Jul  1 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.10-1
-Release 1.3.5.10-1
- Ticket 47538 - Fix repl-monitor color and lag times
- Ticket 47538 - repl-monitor.pl legend not properly sorted
- Ticket 47538 - repl-monitor.pl not displaying correct color code for lag time
- Ticket 48109 - substring index with nssubstrbegin: 1 is not being used with filters like (attr=x*)
- Ticket 48346 - ldaputil code cleanup
- Ticket 48346 - log too verbose when re-acquiring expired  ticket
- Ticket 48354 - Review of default ACI in the directory server
- Ticket 48366 - proxyauth does not work bound as directory manager
- Ticket 48449 - Import readNSState.py from RichM's repo
- Ticket 48636 - Fix config validation check
- Ticket 48637 - DN cache is not always updated when ADD  operation fails
- Ticket 48745 - Matching Rule caseExactIA5Match indexes incorrectly values with upper cases
- Ticket 48755 - CI test: test case for ticket 48755
- Ticket 48755 - moving an entry could make the online init fail
- Ticket 48889 - ldclt - fix man page and usage info
- Ticket 48891 - ns-slapd crashes during the shutdown after adding attribute with a matching rule
- Ticket 48892 - Wrong result code display in audit-failure log
- Ticket 48893 - cn=config should not have readable components to anonymous
- Ticket 48895 - tests package should be noarch
- Ticket 48898 - Crash during shutdown if nunc-stans is enabled
- Ticket 48899 - Values of dbcachetries/dbcachehits in cn=monitor could overflow.
- Ticket 48900 - Add connection perf stats to logconv.pl
- Ticket 48902 - Strdup pwdstoragescheme name to prevent misbehaving plugins
- Ticket 48904 - syncrepl search returning error 329; plugin sending a bad error code
- Ticket 48905 - coverity defects

* Tue Jun 14 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.6-1
- Release 1.3.5.6-1
- Ticket 48234 - CI test: test case for ticket 48234
- Ticket 48234 - "matching rules" in ACI's "bind rules not fully evaluated
- Ticket 48636 - Improve replication convergence
- Revert "Ticket 48755 - moving an entry could make the online init fail"
- Ticket 48766 - Replication changelog can incorrectly skip over updates
- Ticket 47982 - Fix log hr timestamps when invalid value is set in cn=config

* Mon Jun 13 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.5-1
- Release 1.3.5.5-1
- Ticket 48848 - modrdn deleteoldrdn can fail to find old attribute value, perhaps due to case folding
- Ticket 48832 - CI test - fix ticket failures
- Ticket 48833 - 389 showing inconsistent values for shadowMax and shadowWarning in 1.3.5.1
- Ticket 48873 - Backend should accept the reduced cache allocation when issane == 1
- Ticket 48815 - ns-accountstatus.pl - fix DN normalization
- Ticket 48880 - adding pre/post extop ability
- Ticket 48449 - Import readNSState from richm's repo
- Ticket 48877 - Fixes for RPM spec with spectool
- Ticket 48404 - libslapd owned by libs and devel
- Ticket 48326 - Move CI test to config test suite and refactor
- Ticket 48755 - CI test: test case for ticket 48755
- Ticket 48755 - moving an entry could make the online init fail
- Ticket 48870 - Correct plugin execution order due to changes in exop
- Ticket 48799 - Test cases for objectClass values being dropped.
- Ticket 48863 - remove check for vmsize from util_info_sys_pages
- Ticket 48872 - Fix segfault and use after free in plugin shutdown
- Ticket 48862 - At startup DES to AES password conversion causes timeout in start script
- Ticket 48275 - search returns no entry when OR filter component contains non readable attribute
- Ticket 47911 - split out snmp agent into a subpackageTicket 47911
- Ticket 48336 - setup-ds should detect if port is already defined
- Ticket 48858 - Segfault changing nsslapd-rootpw
- Ticket 48855 - Add basic pwdPolicy tests
- Ticket 48747 - dirsrv service fails to start when nsslapd-listenhost is configured
- Ticket 48752 - Page result search should return empty cookie if there is no returned entry
- Ticket 48854 - Running db2index with no options breaks replication
- Ticket 48850 - Correct memory leaks in pwdhash-bin and ns-slapd
- Ticket 48849 - Systemd introduced incompatible changes that breaks ds build
- Ticket 48846 - 32 bit systems set low vmsize
- Ticket 48846 - Older kernels do not expose memavailable
- Ticket 48846 - Rlimit checks should detect RLIM_INFINITY
- Ticket 48617 - Coverity fixes
- Ticket 48745 - Matching Rule caseExactIA5Match indexes incorrectly values with upper cases
- Ticket 48844 - Regression introduced in matching rules by DS 48746
- Ticket 48363 - CI test - add test suite
- Ticket 48795 - Make various improvements to create_test.py
- Ticket 48834 - Fix jenkins: discared qualifier on auditlog.c
- Ticket 48834 - Modifier's name is not recorded in the audit log with modrdn and moddn operations
- Ticket 48754 - ldclt should support -H

* Thu May 19 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.5.4-1.1
- Perl 5.24 re-rebuild of bootstrapped packages

* Wed May 18 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.4-1
- Release 1.3.5.4-1
- Ticket 48836 - replication session fails because of permission denied
- Ticket 47819 - RFE - improve tombstone purging performance
- Ticket 48837 - Replication: total init aborted
- Ticket 48617 - Server ram checks work in isolation
- Ticket 48220 - The "repl-monitor" web page does not display "year" in date.
- Ticket 48829 - Add gssapi sasl replication bind test
- Ticket 48497 - uncomment pytest from CI test
- Ticket 48828 - db2ldif is not taking into account multiple suffixes or backends
- Ticket 48818 - Fix case where return code is always -1
- Ticket 48826 - 52updateAESplugin.pl may fail on older versions of perl
- Ticket 48825 - Configure make generate invalid makefile

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.5.3-1.1
- Perl 5.24 rebuild

* Sun May  8 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.3-1
- Release 1.3.5.3-1
- Ticket 47536 - Allow usage of OpenLDAP libraries that don't use NSS for crypto
- Ticket 47536 - CI test: added test cases for ticket 47536
- Ticket 47840 - default instance scripts if undefined.
- Ticket 47888 - Add CI test
- Ticket 47888 - DES to AES password conversion fails if a backend is empty
- Ticket 47951 - Fix startpid from altering dev/null
- Ticket 47968 - Disable journald logs by default
- Ticket 47982 - HR Log timers, regression fix for subsystem logging
- Ticket 48078 - CI test - paged_results - TET part
- Ticket 48144 - Add /usr/sbin/status-dirsrv script to get the status of the directory server instance.
- Ticket 48269 - ns-accountstatus status message improvement
- Ticket 48342 - DNA: deadlock during DNA_EXTEND_EXOP_REQUEST_OID
- Ticket 48342 - DNA Deadlock test cases
- Ticket 48342 - Prevent transaction abort if a transaction has not begun
- Ticket 48350 - Integrate ASAN into our rpm build process
- Ticket 48374 - entry cache locks not released in error conditions
- Ticket 48410 - 389-ds-base - Unable to remove / unregister a DS instance from admin server
- Ticket 48447 - with-initddir should accept no
- Ticket 48450 - Systemd password agent support
- Ticket 48492 - heap corruption at schema replication.
- Ticket 48597 - Deadlock when rebuilding the group of authorized replication managers
- Ticket 48662 - db2index with no attribute args fail.
- Ticket 48710 - auto-dn-suffix unrecognized option
- Ticket 48769 - Fix white space in extendedop.c
- Ticket 48769 - RFE: Be_txn extended operation plugin type
- Ticket 48770 - Improve extended op plugin handling
- Ticket 48775 - If nsSSL3 is on, even if SSL v3 is not really enabled, a confusing message is logged.
- Ticket 48779 - Remove startpidfile check in start-dirsrv
- Ticket 48781 - Vague error message: setup_ol_tls_conn - failed: unable to create new TLS context
- Ticket 48782 - Make sure that when LDAP_OPT_X_TLS_NEWCTX is set, the value is set to zero.
- Ticket 48783 - Fix ns-accountstatus.pl syntax error
- Ticket 48784 - CI test: added test cases for ticket 48784
- Ticket 48784 - Make the SSL version set to the client library configurable.
- Ticket 48798 - Enable DS to offer weaker DH params in NSS
- Ticket 48799 - objectclass values could be dropped on the consumer
- Ticket 48800 - Cleaning up error buffers
- Ticket 48801 - ASAN errors during tests
- Ticket 48802 - Compilation warnings from clang
- Ticket 48808 - Add test case
- Ticket 48808 - Paged results search returns the blank list of entries
- Ticket 48813 - password history is not updated when an admin resets the password
- Ticket 48815 - ns-accountstatus.sh does handle DN's with single quotes
- Ticket 48818 - In docker, no one can hear your process hang.
- Ticket 48822 - (389-ds-base-1.3.5) Fixing coverity issues.
- Ticket 48824 - Cleanup rpm.mk and 389 specfile

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 1.3.5.1-3.1
- rebuild for ICU 57.1

* Mon Apr 11 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.1-3
- Release 1.3.5.1-3
- Fixed the %%if expression for use_nunc_stans.
- Removed %%if % {use_nunc_stans} from Source3 as well as from nunc_stans_ver.

* Mon Mar 28 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.1-2
- Release 1.3.5.1-2
- Fixed License to GPLv3+
- Generate a user dirsrv in the package install.

* Wed Mar 23 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.1-1
- Release 1.3.5.1-1
- Ticket 47982 - improve timestamp resolution in logs
- Ticket 48759 - no plugin calls in tombstone purging
- Ticket 48665 - Prevent sefault in ldbm_instance_modify_config_entry
- Ticket 48757 - License tag does not match actual license of code
- Ticket 48746 - Crash when indexing an attribute with a matching rule
- Ticket 48497 - extended search without MR indexed attribute prevents later indexing with that MR
- Ticket 48368 - Resolve the py.test conflicts with the create_test.py issue
- Ticket 48748 - Fix memory_leaks test suite teardown failure
- Ticket 48383 - import tasks with dynamic buffer sizes
- Ticket 48420 - change severity of some messages related to "keep alive" entries
- Ticket 48386 - Clean up dsktune code
- Ticket 48537 - undefined reference to `abstraction_increment'
- Ticket 48747 - dirsrv service fails to start when nsslapd-listenhost is configured

* Tue Feb 23 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.0-1
- Release 1.3.5.0
- nunc-stans - bump version to 0.1.8
- Ticket 132   - Makefile.am must include header files and template scripts
- Ticket 142   - [RFE] Default password syntax settings don't work with fine-grained policies
- Ticket 548   - RFE: Allow AD password sync to update shadowLastChange
- Ticket 47788 - Only check postop result if its a replication operation
- Ticket 47840 - add configure option to disable instance specific scripts
- Ticket 47968 - [RFE] Send logs to journald
- Ticket 47977 - [RFE] Implement sd_notify mechanism
- Ticket 48016 - search, matching rules and filter error "unsupported type 0xA9"
- Ticket 48144 - Add /usr/sbin/status-dirsrv script to get the status of the directory server instance.
- Ticket 48145 - RFE Add log file for rejected changes
- Ticket 48147 - Unable to enable DS service for auto start
- Ticket 48151 - Improve CleanAllRUV task logging
- Ticket 48218 - cleanAllRUV - modify the existing "force" option to bypass the "replica online" checks
- Ticket 48244 - No validation check for the value for nsslapd-db-locks.
- Ticket 48257 - Fix coverity issues - 08/24/2015
- Ticket 48263 - allow plugins to detect tombstone operations
- Ticket 48269 - RFE: need an easy way to detect locked accounts locked by inactivity.
- Ticket 48270 - fail to index an attribute with a specific matching rule/48269
- Ticket 48280 - enable logging of internal ops in the audit log
- Ticket 48285 - The dirsrv user/group should be created in rpm %%pre, and ideally with fixed uid/gid
- Ticket 48289 - 389-ds-base: ldclt-bin killed by SIGSEGV
- Ticket 48290 - No man page entry for - option '-u' of dbgen.pl for adding group entries with uniquemembers
- Ticket 48294 - Linked Attributes plug-in - won't update links after MODRDN operation
- Ticket 48295 - Entry cache is not rolled back -- Linked Attributes plug-in - wrong behaviour when adding valid and broken links
- Ticket 48311 - nunc-stans: Attempt to release connection that is not acquired
- Ticket 48317 - SELinux port labeling retry attempts are excessive
- Ticket 48326 - [RFE] it could be nice to have nsslapd-maxbersize default to bigger than 2Mb
- Ticket 48350 - configure.ac add options for debbuging and security analysis / hardening.
- Ticket 48351 - Fix buffer overflow error when reading url with len 0
- Ticket 48363 - Support for rfc3673 '+' to return operational attributes
- Ticket 48369 - [RFE] response control for password age should be sent by default by RHDS
- Ticket 48384 - Server startup should warn about values consuming too much ram
- Ticket 48387 - ASAN invalid read in cos_cache.c
- Ticket 48394 - lower password history minimum to 1
- Ticket 48395 - ASAN - Use after free in uiduniq 7bit.c
- Ticket 48398 - Coverity defect 13352 - Resource leak in auditlog.c
- Ticket 48400 - ldclt - segmentation fault error while binding
- Ticket 48445 - keep alive entries can break replication
- Ticket 48446 - logconv.pl displays negative operation speeds
- Ticket 48566 - acl.c attrFilterArray maybe uninitialised.
- Ticket 48662 - db2index with no attribute args fail.

* Fri Feb 12 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.8-1
- Release 1.3.4.8
- Ticket 48445 - keep alive entries can break replication
- Ticket 47788 - Only check postop result if its a replication operation
- Ticket 48536 - Crash in slapi_get_object_extension
- Ticket 48492 - heap corruption at schema replication.
- Ticket 48448 - dirsrv start-stop fail in certain shell environments.

* Tue Feb 09 2016 Mark Reynolds <mreynolds@redhat.com> - 1.3.4.7-1.2
- Fix spec file for nunc-stans build problem on Rawhide

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4.7-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.7-1
- Release 1.3.4.7
- Bug 1299417 - worker threads do not detect abnormally closed connections (DS 48412)
- Ticket 47788 - Supplier can skip a failing update, although  it should retry
- Ticket 48341 - deadlock on connection mutex
- Ticket 48406 - Avoid self deadlock by PR_Lock(conn->c_mutex)
- Revert "Ticket #48338 - SimplePagedResults -- abandon could happen between the abandon check and sending results"

* Tue Jan 12 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.6-1
- Release 1.3.4.6
- Ticket 48388 - db2ldif -r segfaults from time to time
- Ticket 48312 - Crash when doing modrdn on managed entry
- Ticket 48332 - allow users to specify to relax the FQDN constraint
- Ticket 48375 - SimplePagedResults -- in the search error case, simple paged results slot was not released.
- Ticket 48362 - With exhausted range, part of DNA shared configuration is deleted after server restart
- Ticket 48289 - 389-ds-base: ldclt-bin killed by SIGSEGV
- Ticket 48305 - perl module conditional test is not conditional when checking SELinux policies
- Ticket 48370 - The 'eq' index does not get updated properly when deleting and re-adding attributes in the same modify operation
- Ticket 48369 - RFE - Add config setting to always send the  password expiring time

* Wed Nov 18 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.5-1
- Release 1.3.4.5
- Ticket 48316 - Perl-5.20.3-328: Use of literal control characters in variable names is deprecated
- Ticket 48348 - Running /usr/sbin/setup-ds.pl fails with Can't locate bigint.pm, plus two warnings
- Ticket 48339 - Share nsslapd-threadnumber in the case nunc-stans is enabled, as well.
- Ticket 48311 - nunc-stans: Attempt to release connection that is not acquired https://fedorahosted.org/389/ticket/48311
- Ticket 48325 - Add lib389 test script
- Ticket 48344 - acl - regression - trailing ', (comma)' in macro matched value is not removed.
- Ticket 48325 - Replica promotion leaves RUV out of order
- Ticket 48338 - SimplePagedResults -- abandon could happen between the abandon check and sending results
- Ticket 47976 - deadlock in mep delete post op
- Ticket 48311 - nunc-stans: Attempt to release connection that   is not acquired
- Ticket 47978 - Deadlock between two MODs on the same entry between entry cache and backend lock
- Ticket 48305 - perl module conditional test is not conditional when checking SELinux policies
- Ticket 47957 - Add replication test suite for a wait async feature
- Ticket 48227 - rpm.mk doesn't build srpms for 389-ds and nunc-stans
- Ticket 48264 - Ticket 47553 tests refactoring
- Ticket 48304 - ns-slapd - LOGINFO:Unable to remove file
- Ticket 48298 - ns-slapd crash during ipa-replica-manage del
- Ticket 48192 - Individual abandoned simple paged results request has no chance to be cleaned up
- Ticket 48299 - pagedresults - when timed out, search results could have been already freed.
- Ticket 48204 - update lib389 test scripts for python 3
- Ticket 48283 - many attrlist_replace errors in connection with cleanallruv
- Ticket 48266 - do not free repl keep alive entry on error
- Ticket 48284 - free entry when internal add fails
- Ticket 48266 - Online init crashes consumer
- Ticket 48188 - segfault in ns-slapd due to accessing Slapi_DN freed in pre bind plug-in
- Ticket 48217 - cleanallruv - fix regression with server shutdown
- Ticket 48266 - coverity issue
- Ticket 48266 - Fractional replication evaluates several times the same CSN
- Ticket 48279 - Check NULL reference in nssasl_mutex_lock etc. (saslbind.c)
- Ticket 48226 - In MMR, double free coould occur under some special condition
- Ticket 48273 - Update lib389 tests for new valgrind functions
- Ticket 48276 - initialize free_flags in reslimit_update_from_entry()
- Ticket 47553 - Automated the verification procedure
- Ticket 47761 - Added a few testcases to the basic testsuite
- Ticket 48254 - Shell CLI fails with usage errors if an argument containing white spaces is given
- Ticket 47511 - bashisms in 389-ds-base admin scripts
- Ticket 48267 - Add config setting to MO plugin to add objectclass

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4.4-1.2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 1.3.4.4-1.1
- rebuild for ICU 56.1

* Fri Sep  4 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.4-1
- Release 1.3.4.4
- Ticket 48255 - total update request can be lost
- Ticket 48263 - allow plugins to detect tombstone operations
- Ticket 48265 - Complex filter in a search request doen't work as expected. (regression)
- Ticket 47981 - COS cache doesn't properly mark vattr cache as invalid when there are multiple suffixes
- Ticket 48204 - Convert all python scripts to support python3
- Ticket 48258 - dna plugin needs to handle binddn groups for authorization
- Ticket 48252 - db2index creates index entry from deleted records
- Ticket 48228 - wrong password check if passwordInHistory is decreased.
- Ticket 48252 - db2index creates index entry from deleted records
- Ticket 47757 - Unable to dereference unqiemember attribute because it is dn [#UID] not dn syntax
- Ticket 48254 - Shell CLI fails with usage errors if an argument containing white spaces is given
- Ticket 48254 - CLI db2index fails with usage errors
- Ticket 47831 - remove debug logging from retro cl
- Ticket 48243 - replica upgrade failed in starting dirsrv service due to upgrade scripts did not run
- Ticket 48233 - Server crashes in ACL_LasFindFlush during  shutdown if ACIs contain IP addresss restrictions
- Ticket 48250 - Slapd crashes reported from latest build
- Ticket 48249 - sync_repl uuid may be invalid
- Ticket 48245 - Man pages and help for remove-ds.pl doesn't display "-a" option
- Ticket 47511 - bashisms in 389-ds-base admin scripts
- Ticket 47686 - removing chaining database links trigger valgrind read errors
- Ticket 47931 - memberOf & retrocl deadlocks
- Ticket 48228 - wrong password check if passwordInHistory is decreased.
- Ticket 48215 - update dbverify usage in main.c
- Ticket 48215 - verify_db.pl doesn't verify DB specified by -a option
- Ticket 47810 - memberOf plugin not properly rejecting updates
- Ticket 48231 - logconv autobind handling regression caused by 47446
- Ticket 48232 - winsync lastlogon attribute not syncing between DS and AD.

* Mon Jul 27 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.3-1
- Release 1.3.4.3
- Ticket 48204 - Add Python 3 compatibility to ds-logpipe

* Fri Jul 24 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.2-1
- Release 1.3.4.2
- Ticket 48010 - winsync range retrieval gets only 5000 values upon initialization
- Ticket 48206 - Crash during retro changelog trimming
- Ticket 48224 - redux 2 - logconv.pl should handle *.tar.xz, *.txz, *.xz log files
- Ticket 47910 - logconv.pl - check that the end time is greater than the start time
- Ticket 48179 - Starting a replica agreement can lead to  deadlock
- Ticket 48226 - CI test: added test cases for ticket 48226
- Ticket 48226 - In MMR, double free coould occur under some special condition
- Ticket 48224 - redux - logconv.pl should handle *.tar.xz, *.txz, *.xz log files
- Ticket 48203 - Fix coverity issues - 07/14/2015
- Ticket 48194 - CI test: fixing test cases for ticket 48194
- Ticket 48224 - logconv.pl should handle *.tar.xz, *.txz, *.xz log files
- Ticket 47910 - logconv.pl - validate start and end time args
- Ticket 48223 - Winsync fails when AD users have multiple spaces (two)inside the value of the rdn attribute
- Ticket 47878 - Remove warning suppression in 1.3.4
- Ticket 48119 - Silent install needs to properly exit when INF file is missing
- Ticket 48216 - crash in ns-slapd when deleting winSyncSubtreePair from sync agreement
- Ticket 48217 - cleanAllRUV hangs shutdown if not all of the  replicas are online
- Ticket 48013 - Inconsistent behaviour of DS when LDAP Sync is used with an invalid cookie
- Ticket 47799 - Any negative LDAP error code number reported as Illegal error by ldclt.
- Ticket 48208 - CleanAllRUV should completely purge changelog
- Ticket 48203 - Fix coverity issues - 07/07/2015
- Ticket 48119 - setup-ds.pl does not log invalid --file path errors the same way as other errors.
- Ticket 48192 - Individual abandoned simple paged results request has no chance to be cleaned up
- Ticket 48214 - CI test: added test cases for ticket 48213
- Ticket 48214 - ldapsearch on nsslapd-maxbersize returns 0 instead of current value
- Ticket 48212 - CI test: added test cases for ticket 48212
- Ticket 48212 - Dynamic nsMatchingRule changes had no effect on the attrinfo thus following reindexing, as well.
- Ticket 48195 - Slow replication when deleting large quantities of multi-valued attributes

* Fri Jul 24 2015 Tomas Radej <tradej@redhat.com> - 1.3.4.1-2
- Updated dep on policycoreutils-python-utils (semanage was moved)

* Wed Jun 24 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.1-1
- Release 1.3.4.1
- Resolves: Bug 1234277 - distro-wide architecture set overriden by buildsystem; Upgrade nunc-stans to 0.1.5.
- Enable nunc-stans just for x86_64.
- Ticket 48203 - Fix coverity issues - 06/22/2015

* Fri Jun 19 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-1
- Release 1.3.4.0 (rebase)
- Enable nunc-stans in the build.
- Ticket 47490 - test case failing if 47721 is also fixed
- Ticket 47640 - Linked attributes transaction not aborted when  linked entry does not exit
- Ticket 47669 - CI test: added test cases for ticket 47669
- Ticket 47669 - Retro Changelog Plugin accepts invalid value in nsslapd-changelogmaxage attribute
- Ticket 47723 - winsync sets AccountUserControl in AD to 544
- Ticket 47787 - Make the test case more robust
- Ticket 47833 - TEST CASE only (modrdn fails if renamed entry member of a group and is out of memberof scope)
- Ticket 47878 - Improve setup-ds update logging
- Ticket 47893 - should use Sys::Hostname instead Net::Domain
- Ticket 47910 - allow logconv.pl -S/-E switches to work even when timestamps not present in access log
- Ticket 47913 - remove-ds.pl should not remove /var/lib/dirsrv
- Ticket 47921 - indirect cos does not reflect changes in the cos attribute
- Ticket 47927 - Uniqueness plugin: should allow to exclude some subtrees from its scope
- Ticket 47953 - testcase for removing invalid aci
- Ticket 47966 - CI test: added test cases for ticket 47966
- Ticket 47966 - slapd crashes during Dogtag clone reinstallation
- Ticket 47972 - make parsing of nsslapd-changelogmaxage more fault tolerant
- Ticket 47972 - make parsing of nsslapd-changelogmaxage more fool proof
- Ticket 47998 - cleanup WINDOWS ifdef's
- Ticket 47998 - remove remaining obsolete OS code/files
- Ticket 47998 - remove "windows" files
- Ticket 47999 - address several race conditions in tests
- Ticket 47999 - lib389 individual tests not running correctly  when run as a whole
- Ticket 48003 - build "suite" framework
- Ticket 48008 - db2bak.pl man page should be improved.
- Ticket 48017 - add script to generate lib389 CI test script
- Ticket 48019 - Remove refs to constants.py and backup/restore from lib389 tests
- Ticket 48023 - replace old replication check with lib389 function
- Ticket 48025 - add an option '-u' to dbgen.pl for adding group entries with uniquemembers
- Ticket 48026 - fix invalid write for friendly attribute names
- Ticket 48026 - Fix memory leak in uniqueness plugin
- Ticket 48026 - Support for uniqueness plugin to enforce uniqueness on a set of attributes.
- Ticket 48032 - change C code license to GPLv3; change C code license to allow openssl
- Ticket 48035 - nunc-stans - Revise shutdown sequence
- Ticket 48036 - ns_set_shutdown should call ns_job_done
- Ticket 48037 - ns_thrpool_new should take a config struct rather than many parameters
- Ticket 48038 - logging should be pluggable
- Ticket 48039 - nunc-stans malloc should be pluggable
- Ticket 48040 - preserve the FD when disabling a listener
- Ticket 48043 - use nunc-stans config initializer
- Ticket 48103 - update DS for new nunc-stans header file
- Ticket 48110 - Free all the nunc-stans signal jobs when shutdown is detected
- Ticket 48111 - "make clean" wipes out original files
- Ticket 48122 - nunc-stans FD leak
- Ticket 48127 - Using RPM, allows non root user to create/remove DS instance
- Ticket 48141 - aci with wildcard and macro not correctly evaluated
- Ticket 48143 - Password is not correctly passed to perl command line tools if it contains shell special characters.
- Ticket 48149 - ns-slapd double free or corruption crash
- Ticket 48154 - abort cleanAllRUV tasks should not certify-all by default
- Ticket 48169 - support NSS 3.18
- Ticket 48170 - Parse nsIndexType correctly
- Ticket 48175 - Avoid using regex in ACL if possible
- Ticket 48178 - add config param to enable nunc-stans
- Ticket 48191 - CI test: added test cases for ticket 48191
- Ticket 48191 - RFE: Adding nsslapd-maxsimplepaged-per-conn
- Ticket 48191 - RFE: Adding nsslapd-maxsimplepaged-per-conn Adding nsslapd-maxsimplepaged-per-conn
- Ticket 48194 - CI test: added test cases for ticket 48194
- Ticket 48197 - error texts from preop plugins not sent to client

* Wed Jun 17 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.12-1
- release 1.3.3.12
- Resolves: Bug 1232896 - CVE-2015-3230 389-ds-base: nsSSL3Ciphers preference not enforced server side

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3.11-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.3.11-1.1
- Perl 5.22 rebuild

* Wed Jun 10 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.11-1
- release 1.3.3.11
- Ticket 48192 - Individual abandoned simple paged results request has no chance to be cleaned up
- Ticket 48190 - idm/ipa 389-ds-base entry cache converges to 500 KB in dblayer_is_cachesize_sane
- Ticket 48183 - bind on db chained to AD returns err=32
- Ticket 48158 - cleanAllRUV task limit not being enforced correctly
- Ticket 48158 - Remove cleanAllRUV task limit of 4
- Ticket 48146 - async simple paged results issue; need to close a small window for a pr index competed among multiple threads.
- Ticket 48146 - async simple paged results issue; log pr index
- Ticket 48109 - substring index with nssubstrbegin: 1 is not being used with filters like (attr=x*)
- Ticket 48177 - dynamic plugins should not return an error when modifying a critical plugin
- Ticket 48146 - async simple paged results issue

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.3.10-1.1
- Perl 5.22 rebuild

* Tue Apr 28 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.10-1
- release 1.3.3.10
- Resolves: Bug 1216203 - CVE-2015-1854 389ds-base: access control bypass with modrdn

* Fri Mar  6 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.9-1
- bump version to 1.3.3.9
- Bug 1199675 - CVE-2014-8112 CVE-2014-8105 389-ds-base: various flaws [fedora-all]
- Ticket 47801 - RHDS keeps on logging write_changelog_and_ruv: failed to update RUV for unknown
- Ticket 47957 - Make ReplicaWaitForAsyncResults configurable
- Ticket 47431 - CI test: added test cases for ticket 47431
- Ticket 47431 - Duplicate values for the attribute nsslapd-pluginarg are not handled correctly
- Ticket 47936: Create a global lock to serialize write operations over several backends
- Ticket 48021 - nsDS5ReplicaBindDNGroup checkinterval not working properly
- Ticket 48048 - Fix coverity issues - 2015/3/1
- Ticket 48109 - substring index with nssubstrbegin: 1 is not being used with filters like (attr=x*)
- Ticket 48109 - CI test: added test cases for ticket 48109
- Ticket 48109 - substring index with nssubstrbegin: 1 is not being used with filters like (attr=x*)
- Ticket 48048 - Fix coverity issues - 2015/2/24
- Ticket 48030 - spec file should run "systemctl stop" against each running instance instead of dirsrv.target
- Ticket 47828: DNA scope: allow to exlude some subtrees
- Ticket 47988: test case
- Ticket 47901: After total init, nsds5replicaLastInitStatus can report an erroneous error status (like 'Referral')
- Ticket 48003 - add template scripts
- Ticket 48003 - build "suite" framework
- Ticket 48005 - CI test: added test cases for ticket 48005
- Ticket 48005 - ns-slapd crash in shutdown phase
- Ticket 47742 - 64bit problem on big endian: auth method not supported
- Ticket 47836 - Do not return '0' as empty fallback value of nsds5replicalastupdatestart and nsds5replicalastupdatestart
- Ticket 47728 - compilation failed with ' incomplete struct/union/enum' if not set USE_POSIX_RWLOCKS
- Ticket 48027 - revise the rootdn plugin configuration validation
- Ticket 47451 - dynamic plugins - fix crash caused by invalid  plugin config
- Ticket 48001 - ns-activate.pl fails to activate account if it was disabled on AD

* Wed Feb 25 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.8-2
- Fixes spec file to make sure all the server instances are stopped before upgrade
- Ticket 48030 - DNS errors after IPA upgrade due to broken ReplSync

* Wed Feb 04 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.8-1
- bump version to 1.3.3.8
- Ticket 48001 - ns-activate.pl fails to activate account if it was disabled on AD
- Ticket 47963 - memberof skip nested groups breaks the plugin

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 1.3.3.7-2.1
- Bump for rebuild.

* Wed Jan 28 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.7-2
- removed USE_64=1 which is not used any more.

* Wed Jan 28 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.7-1
- bump version to 1.3.3.7
- Coverity 12970 - Explicit null dereference
- Ticket 47988 - Schema learning mechanism, in replication, unable to extend an existing definition
- Ticket 47996 - ldclt needs to support SSL Version range
- Ticket 47738 - use PL_strcasestr instead of strcasestr
- Ticket 47462 - Stop using DES in the reversible password  encryption plug-in
- Ticket 47807 - SLAPI_REQUESTOR_ISROOT not set for extended operation plugins
- Ticket 47991 - upgrade script fails if /etc and /var are on different file systems
- Ticket 47989 - Windows Sync accidentally cleared raw_entry
- Ticket 47964 - v2 - Incorrect search result after replacing an empty attribute
- Ticket 47934 - nsslapd-db-locks modify not taking into account.
- Ticket 47617 - replication changelog trimming setting validation
- Ticket 47905 - Bad manipulation of passwordhistory
- Ticket 47973 - During schema reload sometimes the search returns no results
- Ticket 47981 - COS cache doesn't properly mark vattr cache as  invalid when there are multiple suffixes
- Ticket 47980 - Nested COS definitions can be incorrectly  processed
- Ticket 47451 - Dynamic plugins - fixed thread synchronization
- Ticket 47750 - During delete operation do not refresh cache entry if it is a tombstone
- Ticket 47947 - start dirsrv after chrony on RHEL7 and Fedora
- fix jenkins warning
- Ticket 47526 - Additional fix for ticket 47526 v3
- Ticket 47451 - Add Dynamic Plugin CI Suite
- Ticket 47965 - Fix coverity issues (2014/12/16)
- Ticket 47451 - Fix jenkins errors
- Ticket 47451 - Dynamic Plugin - various fixes
- Ticket 47935 - Error: failed to open an LDAP connection to host 'example.org' port '389' as user 'cn=Directory Manager'. Error: unknown.
- Ticket 47750 - Need to refresh cache entry after called betxn postop plugins
- Ticket 47942 -  DS hangs during online total update
- Ticket 47960 - cookie_change_info returns random negative number if there was no change in a tree
- Ticket 47960 - cookie_change_info returns random negative number if there was no change in a tree
- Ticket 47722 - Using the filter file does not work
- Ticket 47636 - Error log levels not displayed correctly
- Ticket 47965 - Fix coverity issues (2014/11/24)
- Ticket 47969 - Fix coverity issue
- Ticket 47949 - logconv.pl -- support parsing/showing/reporting different protocol versions
- Ticket 47525 - Crash if setting invalid plugin config area for MemberOf Plugin
- Ticket 47970 - add lib389 testcase
- Ticket 47970 - Account lockout attributes incorrectly updated after failed SASL Bind
- Ticket 47969 - COS memory leak when rebuilding the cache
- Ticket 47967 - cos_cache_build_definition_list does not stop during server shutdown
- Ticket 47451 - Running a plugin task can crash the server
- Ticket 47963 - skip nested groups breaks memberof fixup task
- Ticket 47963 - RFE - memberOf - add option to skip nested  group lookups during delete operations
- Ticket 47810 - RI plugin does not return result code if update fails

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 1.3.3.6-1.1
- rebuild for ICU 54.1

* Thu Nov 20 2014 Mark Reynolds <mreynolds@redhat.com> - 1.3.3.6-1
- 5d72a2f bump version to 1.3.3.6-1
- Ticket 47950 - Bind DN tracking unable to write to internalModifiersName without special permissions
- Ticket 47958 - Memory leak in password admin if the admin entry does not exist
- Ticket 47952 - PasswordAdminDN attribute is not properly returned to client
- Ticket 47451 - Need to unregister tasks created by plugins
- Ticket 47928 - Disable SSL v3, by default.
- Ticket 47953 - Should not check aci syntax when deleting an aci
- Ticket 47948 - ldap_sasl_bind fails assertion (ld != NULL) if it is called from chainingdb_bind over SSL/startTLS
- Ticket 47945 - Add SSL/TLS version info to the access log
- Ticket 47939 - Malformed cookie for LDAP Sync makes DS crash
- Ticket 47937 - Crash in entry_add_present_values_wsi_multi_valued
- Ticket 47928 - CI test: added test cases for ticket 47928
- Ticket 47553 - Enhance ACIs to have more control over MODRDN operations

* Fri Oct 10 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.5-1
- Release 1.3.3.5
- Ticket 47914 - Add FreeIPA Conflicts to 389 spec file
- Ticket 47922 - dynamically added macro aci is not evaluated on the fly
- Ticket 47897 - Need to move slapi_pblock_set(pb, SLAPI_MODRDN_EXISTING_ENTRY, original_entry->ep_entry) prior to original_entry overwritten
- Ticket 47920 - Encoding of SearchResultEntry is missing tag
- Ticket 47912 - Proper handling of "No original_tombstone for changenumber" errors
- Ticket 47899 - Fix slapi_td_plugin_lock_init prototype
- Ticket 47919 - ldbm_back_modify SLAPI_PLUGIN_BE_PRE_MODIFY_FN does not return even if one of the preop plugins fails.
- Ticket 47892 - Fix remaining compiler warnings
- ticket 47916 - plugin logging parameter only triggers result logging
- Ticket 47918 - result of dna_dn_is_shared_config is incorrectly used
- Ticket 47900 - Server fails to start if password admin is set
- Ticket 47892 - coverity defects found in 1.3.3.x

* Wed Oct 01 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.4-1
- Release 1.3.3.4
- Ticket 47880 - CI test: added test cases for ticket 47880
- Ticket 47880 - provide enabled ciphers as search result
- Ticket 47838 - CI test: adjusted test cases based on the phase 2 fixes for ticket 47838
- Ticket 47838 - harden the list of ciphers available by default (phase 2)
- Ticket 47900 - Adding an entry with an invalid password as rootDN is incorrectly rejected
- Ticket 47908 - 389-ds 1.3.3.0 does not adjust cipher suite configuration on upgrade, breaks itself and pki-server
- Ticket 47907 - ldclt: assertion failure with -e "add,counteach" -e "object=<ldif file>,rdn=uid:test[A=INCRNNOLOOP(0;24
- Ticket 47750 - Creating a glue fails if one above level is a conflict or missing

* Sun Sep 14 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.3.3.3-2
- Use generic 64 bit detection (fixes aarch64/ppc64le)
- PPC/s390 has lm_sensors
- Minor spec cleanups

* Fri Sep 12 2014 Rich Megginson <rmeggins@redhat.com> - 1.3.3.3-1
- Release 1.3.3.3
- Ticket #47892 - coverity defects found in 1.3.3.1

* Fri Sep 12 2014 Nathan Kinder <nkinder@redhat.com> - 1.3.3.2-1
- Release 1.3.3.2
- Ticket 47889 - DS crashed during ipa-server-install on test_ava_filter
- Ticket 47895 - If no effective ciphers are available, disable security setting.
- Ticket 47838 - harden the list of ciphers available by default
- Ticket 47885 - did not always return a response control
- Ticket 47890 - minor memory leaks in utilities
- Ticket 47834 - Tombstone_to_glue: if parents are also converted to glue, the target entry's DN must be adjusted.
- Ticket 47748 - Simultaneous adding a user and binding as the user could fail in the password policy check
- Ticket 47875 - dirsrv not running with old openldap
- Ticket 47885 - deref plugin should not return references with noc access rights

* Thu Sep 04 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.3.0-2
- Perl 5.20 rebuild

* Wed Sep 03 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.0-1
- Release 1.3.3.0
- Ticket 47879 - coverity defects in plugins/replication/windows_protocol_util.c
- Ticket 47876 - coverity defects in slapd/tools/mmldif.c
- Ticket 47574 - start dirsrv after ntpd
- Ticket 47838 - harden the list of ciphers available by default
- Ticket 47579 - add dbmon.sh
- Ticket 47819 - Fix memory leak
- Ticket 47819 - Improve tombstone purging performance
- Ticket 47714 - [RFE] Update lastLoginTime also in Account Policy plugin if account lockout is based on passwordExpirationTime.
- Ticket 47812 - logconv.pl missing -U option from usage
- Ticket 47664 - Page control does not work if effective rights control is specified
- Ticket 47790 - Integer config attributes accept invalid  values at server startup
- Ticket 47710 - Missing warning for invalid replica backoff configuration
- Ticket 47853 - Missing newline at end of the error log messages in memberof
- Ticket 47853 - client hangs in add if memberof fails
- Ticket 47746 - ldap/servers/slapd/back-ldbm/dblayer.c: possible minor problem with sscanf
- Ticket 47711 - improve dbgen rdn generation, output and man page.
- Ticket 47855 - Fix previous commit
- Ticket 47859 - Coverity: 12692 & 12717
- Ticket 47855 - clear tmp directory at the start of each test
- Ticket 47844 - Fix hyphens used as minus signed and other manpage mistakes
- Ticket 47843 - Fix various typos in manpages & code
- Ticket 47832 - attrcrypt_generate_key calls slapd_pk11_TokenKeyGenWithFlags with improper macro
- Ticket 47852 - Updating winsync one-way sync does not affect the behaviour dynamically
- Ticket 47846 - server crashes deleting a replication agreement
- Ticket 47823 - attribute uniqueness enforced on all subtrees
- Ticket 47654 - Fix regression (deadlock/crash)
- Ticket 47827 - Fix coverity issue 12695
- Ticket 47829: memberof scope: allow to exclude subtrees
- Ticket 47815 - Add operations rejected by betxn plugins remain in cache
- Ticket 47808 - If be_txn plugin fails in ldbm_back_add, adding entry is double freed
- Ticket 555   - add fixup-memberuid.pl script
- Ticket 47827 - online import crashes server if using verbose error logging
- fix compiler error with alst coverity commit
- fix coverity issue 12621
- Ticket 47810 - investigate betxn plugins to ensure they  return the correct error code
- Ticket 47602 - txn commit being performed too early
- Ticket 47752 - Don't add unhashed password mod if we don't have an unhashed value
- Ticket 47803 - syncrepl crash if attribute list is non-empty
- Ticket 47466 - Fix coverity issue
- Ticket 47644 - Managed Entry Plugin - transaction not aborted upon failure to create managed entry
- Ticket 47791 - Negative value of nsSaslMapPriority is not  reset to lowest priority
- Ticket 47805 - syncrepl doesn't send notification when attribute in search filter changes
- Ticket 47636 - errorlog-level 16384 is listed as 0 in cn=config
- Ticket 47451 - Remove old code from linked attr plugin
- Ticket 47756 - fix coverity issues
- Ticket 47761 - Return all attributes in rootdse without explicit request
- fix assertion failure introduced with fix for ticket 47667
- Ticket 47712 - betxn: retro changelog broken after cancelled transaction
- Ticket 47667 - Allow nsDS5ReplicaBindDN to be a group DN
- Ticket 47655 - Improve replication total update logging
- Ticket 47756 - Improve import logging and abort processing
- Ticket 47451 - add/enable/disable/remove plugins without server restart
- Ticket 47553 - Enhance ACIs to have more control over MODRDN operations
- Ticket 47727 - Updating nsds5ReplicaHost attribute in a replication agreement fails with error 53
- Ticket 47725 - compiler error on daemon.c
- Ticket 47701 - Make retro changelog trim interval programmable
- Ticket 47453 - configure SASL/GSSAPI/Kerberos without server restart
- Ticket 47701 - Make retro changelog trim interval programmable
- Ticket 47602 - Make ldbm_back_seq independently support transactions
- Ticket 47552 - logconv: unindexed report should list bind dn
- Ticket 47619 - cannot reindex retrochangelog
- Update test cases due to new modules: Schema, tasks, plugins and index
- Ticket 47608 - change slapi_entry_attr_get_bool to handle "on"/"off" values, support default value
- Ticket 47437 - Some attributes in cn=config should not be multivalued
- Ticket 47573 - schema push can be erronously prevented
- Ticket 47618 - Enable normalized DN cache by default
- Ticket 47570 - slapi_ldap_init unusable during independent plugin development
- Ticket 47659 - ldbm_usn_init: Valgrind reports Invalid read / SIGSEGV
- Ticket 47654 - fix double free
- Ticket 47675 - logconv errors when search has invalid bind dn
- Ticket 47657 - add schema test suite and tests for Ticket #47634
- Ticket 47668 - test: port ticket47490_test to Replica/Agreement interface (47600)
- Ticket 47654 - Cleanup old memory leaks reported from valgrind
- Ticket 47651 - Finaliser to remove instances backups
- Ticket 47603 - should not modify pre op entry during config validation
- Ticket 47628 - port testcases to new DirSrv interface
- Ticket 47525 - Don't modify preop entry in memberOf config
- Ticket 605   - support TLS 1.1 - Fixing "Coverity 12415 - Logically dead code"
- Ticket 605   - support TLS 1.1 - lower the log level for the supported NSS version range
- Ticket 47368 - fix memory leaks
- Ticket 605   - support TLS 1.1 - adding backward compatibility
- Ticket 605   - support TLS 1.1
- Ticket 47603 - Allow RI plugin to use alternate config area
- Ticket 47586 - Need to rebind after a stop (fix to run direct python script)
- Ticket 47525 - Need to add locking around config area access
- Ticket 47457 - default nsslapd-sasl-max-buffer-size should be 2MB
- Ticket 47525 - Fix memory leak
- Ticket 381   - Recognize compressed log files
- Ticket 47525 - Allow memberOf to use an alternate config area
- Ticket 47529 - Automember plug-in should treat MODRDN operations as ADD operations
- Ticket 47521 - Complex filter in a search request doen't work as expected.
- Ticket 47582 - agmt_count in Replica could become (PRUint64)-1
- Ticket 47368 - Fix coverity issues
- Ticket 47555 - db2bak.pl issue when specifying non-default directory
- Ticket 47368 - Fix Jenkins errors
- Ticket 47368 - IPA server dirsrv RUV entry data excluded from replication
- Ticket 538   - - hardcoded sasl2 plugin path in ldaputil.c, saslbind.c
- Ticket 47519 - memory leaks in access control
- Ticket 47398 - memberOf on a user is converted to lowercase
- Coverity Issue 12033
- Ticket 47530 - dbscan on entryrdn should show all matching values
- Ticket 47422 - With 1.3.04 and subtree-renaming OFF, when a user is deleted after restarting the server, the same entry can't be added
- bump autoconf to 2.69, automake to 1.13.4, libtool to 2.4.2
- Ticket 47436 - 389-ds-base - shebang with /usr/bin/env
- Ticket 47499 - if nsslapd-cachememsize set to the number larger than the RAM available, should result in proper error message.
- Ticket 47530 - dbscan on entryrdn should show all matching values
- Ticket 47535 - update man page
- Ticket 53    - Need to update supported locales Cleaning up typos and format.
- Ticket 47535 - Logconv.pl - RFE - add on option for a minimum etime for unindexed search stats
- Ticket 47491 - Update systemd service file to use PartOf directive

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.2.23-1.1
- Perl 5.20 rebuild

* Wed Aug 27 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.23-1
- Release 1.3.2.23
- Ticket 47871 - 389-ds-base-1.3.2.21-1.fc20 crashed over the weekend
- Ticket 47866 - Errors after upgrading related to attribute "dnaremotebindmethod"
- Ticket 47816 - v2- internal syncrepl searches are flagged as unindexed
- Ticket 47877 - check_and_add_entry fails for changetype: add and existing entry
- Ticket 47834 - Tombstone_to_glue: if parents are also converted to glue, the target entry's DN must be adjusted.
- Ticket 47875 - dirsrv not running with old openldap
- Revert "Ticket #47875 - dirsrv not running with old openldap"
- Ticket 47875 - dirsrv not running with old openldap
- Ticket 47446 - logconv.pl memory continually grows
- Ticket 47874 - Performance degradation with scope ONE after some load
- Ticket 47872 - Filter AND with only one clause should be optimized
- Ticket 47834 - Tombstone_to_glue: if parents are also converted to glue, the target entry's DN must be adjusted.
- Ticket 47862 - repl-monitor fails to convert "*" to default values
- Ticket 47824 - paged results control is not working in some cases when we have a subsuffix.
- Ticket 47862 - Repl-monitor.pl ignores the provided connection parameters
- Ticket 346   - Fixing memory leaks
- Ticket 47753 - Add switch to disable pre-hashed password checking
- Ticket 47861 - Certain schema files are not replaced during upgrade
- Ticket 47858 - Internal searches using OP_FLAG_REVERSE_CANDIDATE_ORDER can crash the server
- Ticket 47797 - fix the indentation
- Ticket 47797 - DB deadlock when two threads (on separated backend) try to record changes in retroCL
- Ticket 47692 - single valued attribute replicated ADD does not work
- Ticket 47781 - Server deadlock if online import started while  server is under load

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.2.22-1.3
- Perl 5.20 rebuild

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 1.3.2.22-1.2
- rebuild for ICU 53.1

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2.22-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.22-1
- Release 1.3.2.21
- Resolves: #1127833
            Ticket 47869 - unauthenticated information disclosure (Bug 1123477)
  389-ds-base-1.3.2.22 = 389-ds-base-1.3.2.19 + Bug 1127833 fix.

* Thu Aug 07 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.21-1
- Release 1.3.2.21
- Resolves: #1127833
            Ticket 47869 - unauthenticated information disclosure (Bug 1123477)
- Ticket 47834 - Tombstone_to_glue: if parents are also converted to glue, the target entry's DN must be adjusted.
- Ticket 47862 - repl-monitor fails to convert "*" to default values
- Ticket 47824 - paged results control is not working in some cases when we have a subsuffix.
- Ticket 47862 - Repl-monitor.pl ignores the provided connection parameters
- Ticket 346   - Fixing memory leaks

* Tue Jul 22 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.20-1
- Release 1.3.2.20
- Ticket 47753 - Add switch to disable pre-hashed password checking
- Ticket 47861 - Certain schema files are not replaced during upgrade
- Ticket 47858 - Internal searches using OP_FLAG_REVERSE_CANDIDATE_ORDER can crash the server
- Ticket 47797 - DB deadlock when two threads (on separated backend) try to record changes in retroCL
- Ticket 47834 - Tombstone_to_glue: if parents are also converted to glue, the target entry's DN must be adjusted.
- Ticket 47692 - single valued attribute replicated ADD does not work
- Ticket 47781 - Server deadlock if online import started while  server is under load

* Thu Jul 03 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.19-1
- Release 1.3.2.19
- Ticket 47779 - Potential deadlock after startup if a dna configuration change is made
- Ticket 47839 - 389-ds production segfault: __memcpy_sse2_unaligned...

* Tue Jul 01 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.18-1
- Release 1.3.2.18
- Ticket 47750 - Creating a glue fails if one above level is a conflict or missing
- Ticket 47763 - winsync plugin modify is broken
- Ticket 47821 - deref plugin cannot handle complex acis
- Ticket 47831 - server restart wipes out index config if there is a default index
- Ticket 47817 - The error result text message should be obtained just prior to sending result
- Ticket 47815 - Add operations rejected by betxn plugins remain in cache
- Ticket 47809 - find a way to remove replication plugin errors messages "changelog iteration code returned a dummy entry with csn %%s, skipping ..."
- Ticket 47704 - invalid sizelimits in aci group evaluation
- Ticket 47813 - remove "goto bail" from previous commit
- Ticket 47813 - managed entry plugin fails to update member  pointer on modrdn operation
- Ticket 47808 - If be_txn plugin fails in ldbm_back_add, adding entry is double freed.
- Ticket 47770 - #481 breaks possibility to reassemble memberuid list

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2.17-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.17-1
- Release 1.3.2.17
- Ticket 47446 - logconv.pl memory continually grows
- Ticket 47713 - Logconv.pl with an empty access log gives lots of errors
- Ticket 47806 - Failed deletion of aci: no such attribute
- bump version
- Ticket 47720 - Normalization from old DN format to New DN format doesnt handel condition properly when there is space in a suffix after the seperator operator.
- Ticket 47670 - Aci warnings in error log
- Ticket 47721 - Schema Replication Issue (follow up)
- Ticket 47721 - Schema Replication Issue (follow up + cleanup)
- Ticket 47721 - Schema Replication Issue
- Ticket 47676 - (cont.) Replication of the schema fails 'master branch' -> 1.2.11 or 1.3.1
- Ticket 47676 - Replication of the schema fails 'master branch' -> 1.2.11 or 1.3.1
- Ticket 47541 - Fix Jenkins errors
- Ticket 47541 - Replication of the schema may overwrite  consumer 'attributetypes' even if  consumer definition is a superset
- Ticket 47804 - db2bak.pl error with changelogdb
- Ticket 47780 - Some VLV search request causes memory leaks
- Ticket 47787 - A replicated MOD fails (Unwilling to perform) if it targets a tombstone
- Ticket 47764 - Problem with deletion while replicated
- Ticket 47750 - Creating a glue fails if one above level is a conflict or missing; Ticket 47696 - Large Searches Hang - Possibly entryrdn related
- Ticket 47772 - fix coverity issue
- Ticket 47793 - Server crashes if uniqueMember is invalid syntax and memberOf plugin is enabled.
- Ticket 47792 - database plugins need a way to call betxn  plugins
- Ticket 47707 - 389 DS Server crashes and dies while handles paged searches from clients
- Ticket 47792 - code cleanup
- Ticket 47779 - Need to lock server list when removing list
- Ticket 47771 - Move parentsdn initialization to avoid crash
- Ticket 47779 - Part of DNA shared configuration is deleted after server restart
- Ticket 346   - Slow ldapmodify operation time for large quantities of multi-valued attribute values
- Ticket 47782 - Parent numbordinate count can be incorrectly updated if an error occurs
- Ticket 47772 - empty modify returns LDAP_INVALID_DN_SYNTAX
- Ticket 47774 - mem leak in do_search - rawbase not freed upon certain errors
- Ticket 47773 - mem leak in do_bind when there is an error
- Ticket 47771 - Performing deletes during tombstone purging results in operation errors
- Ticket 47767 - Nested tombstones become orphaned after purge
- Ticket 47766 - Tombstone purging can crash the server if the backend is stopped/disabled
- Ticket 47759 - Crash in replication when server is under write load
- Ticket 47740 - Fix coverity issues(part 7)
- Ticket 47748 - Simultaneous adding a user and binding as the user could fail in the password policy check
- Ticket 47743 - Memory leak with proxy auth control
- Ticket 47740 - Crash caused by changes to certmap.c
- Ticket 47733 - ds logs many "Operation error fetching Null DN" messages
- Ticket 47740 - Fix coverity issues: null deferences - Part 6
- Ticket 47732 - ds logs many "SLAPI_PLUGIN_BE_TXN_POST_DELETE_FN plugin returned error" messages
- Ticket 47740 - Coverity issue in 1.3.3
- Ticket 47735 - e_uniqueid fails to set if an entry is a conflict entry
- Ticket 47740 - Fix coverity issues - Part 5
- Ticket 47740 - Fix coverity erorrs - Part 4
- Ticket 47640 - Fix coverity issues - part 3
- Ticket 47740 - Fix sync plugin resource leaks
- Ticket 47538 - RFE: repl-monitor.pl plain text output, cmdline config options
- Ticket 47740 - Coverity Fixes (Mark - part 1)
- Ticket 47734 - Change made in resolving ticket #346 fails on Debian SPARC64
- Ticket 47722 - Fixed filter not correctly identified
- Ticket 47722 - rsearch filter error on any search filter

* Fri Mar 14 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.16-1
- Release 1.3.2.16 (This release is 1.3.2.13 + Ticket 47739)
- Ticket 47739 - directory server is insecurely misinterpreting authzid on a SASL/GSSAPI bind

* Thu Mar 13 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.15-1
- Bump version to 1.3.2.15
- Ticket 47735 - e_uniqueid fails to set if an entry is a conflict entry
- Ticket 47740 - Coverity issue in 1.3.3
- Ticket 47740 - Fix coverity issues - Part 5
- Ticket 47740 - Fix coverity erorrs - Part 4
- Ticket 47640 - Fix coverity issues - part 3
- Ticket 47740 - Fix sync plugin resource leaks
- Ticket 47538 - RFE: repl-monitor.pl plain text output, cmdline config options
- Ticket 47740 - Coverity Fixes (Mark - part 1)
- Ticket 47734 - Change made in resolving ticket #346 fails on Debian SPARC64
- Ticket 47722 - Fixed filter not correctly identified
- Ticket 47722 - rsearch filter error on any search filter

* Mon Mar 10 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.14-1
- Bump version to 1.3.2.14
- Ticket 47739 - directory server is insecurely misinterpreting authzid on a SASL/GSSAPI bind
- Ticket 47737 - Under heavy stress, failure of turning a tombstone into glue makes the server hung
- Ticket 47735 - e_uniqueid fails to set if an entry is a conflict entry
- Ticket 47729 - Directory Server crashes if shutdown during a replication initialization
- Ticket 47637 - rsa_null_sha should not be enabled by default

* Fri Feb 28 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.13-1
- Bump version to 1.3.2.13
- The previous version 1.3.2.12 missed to increment the version in VERSION.sh

* Fri Feb 28 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.12-1
- Bump version to 1.3.2.12
- Ticket 408   - create a normalized dn cache
- Ticket 571   - Empty control list causes LDAP protocol error is thrown (dup 47361)
- Ticket 408   - create a normalized dn cache
- Ticket 47699 - Propagate plugin precedence to all registered function types
- Ticket 525   - Replication retry time attributes cannot be added
- Ticket 47709 - package issue in 389-ds-base
- Ticket 47700 - Unresolved external symbol references break loading of the ACL plugin
- Ticket 47642 - Windows Sync group issues
- Ticket 525   - Replication retry time attributes cannot be added
- Ticket 47692 - single valued attribute replicated ADD does not work
- Ticket 47615 - Failed to compile the DS 389 1.3.2.3 version against Berkeley DB 4.2 version
- Ticket 47677 - Size returned by slapi_entry_size is not accurate
- Ticket 47693 - Environment variables are not passed when DS is started via service

* Thu Feb 20 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.11-3
- Added arch aware python dir; moved libns-dshttpd.so* to devel and libs package.

* Fri Feb 14 2014 Parag Nemade <paragn AT fedoraproject DOT org> - 1.3.2.11-2
- Rebuild for icu 52

* Wed Feb  5 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.11-1
- Bump version to 1.3.2.11
- Ticket 47653 - Need a way to allow users to create entries assigned to themselves.
- Ticket 471   - logconv.pl tool removes the access logs contents if "-M" is not correctly used
- Ticket 47374 - flush.pl is not included in perl5
- Ticket 47649 - Server hangs in cos_cache when adding a user entry
- Ticket 443   - Deleting attribute present in nsslapd-allowed-to-delete-attrs returns Operations error
- Ticket 47638 - Overflow in nsslapd-disk-monitoring-threshold on 32bit platform
- Ticket 47641 - 7-bit check plugin not checking MODRDN operation
- Ticket 342   - better error message when cache overflows
- Ticket 47516 - replication stops with excessive clock skew
- Ticket 47620 - Unable to delete protocol timeout attribute
- Ticket 408   - Fix crash when disabling/enabling the setting
- Ticket 47629 - random crashes related to sync repl
- Ticket 47571 - targetattr ACIs ignore subtype
- Ticket 47660 - config_set_allowed_to_delete_attrs: Valgrind reports Invalid read
- Revert "Ticket 47653 - Need a way to allow users to create entries assigned to themselves"

* Wed Jan  8 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.10-1
- Bump version to 1.3.2.10
- Ticket 447 - Possible to add invalid attribute to nsslapd-allowed-to-delete-attrs
- Ticket 47653 - Need a way to allow users to create entries assigned to themselves
- Ticket 47647 - remove bogus definition in 60rfc3712.ldif
- Ticket 47634 - support AttributeTypeDescription USAGE userApplications distributedOperation dSAOperation
- Ticket 47645 - reset stack, op fields to NULL - clean up stacks at shutdown - free unused plugin config entries

* Tue Dec 17 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.9-1
- Bump version to 1.3.2.9
- Ticket 47621 - v2 make referential integrity configuration more flexible
- Ticket 47620 - Fix missing left bracket
- Ticket 47620 - Fix dereferenced NULL pointer in agmtlist_modify_callback()
- Ticket 47606 - replica init/bulk import errors should be more verbose
- Ticket 47631 - objectclass may, must lists skip rest of objectclass once first is found in sup
- Ticket 47627 - Fix replication logging
- Ticket 47620 - Fix logically dead code.
- Ticket 47313 - Indexed search with filter containing '&' and "!" with attribute subtypes gives wrong result
- Ticket 47620 - Config value validation improvement
- Ticket 47620 - Fix cherry-pick error for 1.3.2 and 1.3.1
- Ticket 47613 - Issues setting allowed mechanisms
- Ticket 47617 - allow configuring changelog trim interval
- Ticket 47601 - Plugin library path validation prevents intentional loading of out-of-tree modules
- Ticket 47627 - changelog iteration should ignore cleaned rids when getting the minCSN
- Ticket 47623 - fix memleak caused by 47347
- Ticket 47622 - Automember betxnpreoperation - transaction not aborted when group entry does not exist
- Ticket 47623 - fix memleak caused by 47347
- Ticket 47620 - 389-ds rejects nsds5ReplicaProtocolTimeout attribute

* Fri Dec  6 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.8-1
- Bump version to 1.3.2.8
- Ticket 47612 - ns-slapd eats all the memory
- Ticket 47527 - Allow referential integrity suffixes to be configurable
- Ticket 47526 - Allow memberof suffixes to be configurable
- Ticket 342   - better error message when cache overflows (phase 2)
- Ticket 47587 - hard coded limit of 64 masters in agreement and changelog code
- Ticket 47611 - Add script to build patched RPMs
- Ticket 47614 - Possible to specify invalid SASL mechanism in nsslapd-allowed-sasl-mechanisms
- Ticket 47613 - Impossible to configure nsslapd-allowed-sasl-mechanisms
- Ticket 47592 - automember plugin task memory leaks
- Ticket 47591 - entries with empty objectclass attribute value can be hidden
- Ticket 47596 - attrcrypt fails to find unlocked key

* Mon Nov 25 2013 Mark Reynolds <mreynolds@redhat.com> - 1.3.2.7-1
- 924ead4 Bump version to 1.3.2.7
- Ticket 47593 - Update plugin API for OTP plugin
- Ticket 47599 - fix memory leak in ldbm_back_seq()

* Fri Nov 22 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.2.6-1
- Ticket 47599 - Reduce lock scope in retro changelog plug-in
-  previous fix missing defition of retrocl_cn_lock

* Thu Nov 21 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.2.5-1
- Ticket #47605 CVE-2013-4485: DoS due to improper handling of ger attr searches

* Wed Nov 20 2013 Mark Reynolds <mreynolds@redhat.com> - 1.3.2.4-1
6cdca01 bump version to 1.3.2.4
Ticket 47599 - Reduce lock scope in retro changelog plug-in
Ticket 47596 - attrcrypt fails to find unlocked key
Ticket 47598 - Convert ldbm_back_seq code to be transaction aware
Ticket 47597 - Convert retro changelog plug-in to betxn
Ticket 47585 - Replication Failures related to skipped entries due to cleaned rids
Ticket 47588 - Compiler warnings building on F19
Ticket 47581 - Winsync plugin segfault during incremental backoff (phase 2)
Ticket 47581 - Winsync plugin segfault during incremental backoff
Ticket 47577 - crash when removing entries from cache
6b16d30 Revert "Ticket #47559 hung server - related to sasl and initialize"

* Mon Oct 28 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.3-1
- release 1.3.2.3
- Ticket 47515 - Fedora 20: setup-ds-admin.pl
- Ticket 47569 - Fix build warnings
- Ticket 47569 - ACIs do not allow attribute subtypes in targetattr keyword
- Ticket 47565 - Content Sync update file needs extensibleObject
- Ticket 47560 - fixup memberof task does not work: task entry not added
- Ticket 47559 - hung server - related to sasl and initialize

* Fri Oct 11 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.2-1
- release 1.3.2.2
- Ticket 47517 - memory leak in range searches and other various leaks
- ticket 47550 - wip (cherry picked from commit 82377636267787be5182457d619d5a0b662d2658)
- Ticket 47550 - logconv: failed logins: Use of uninitialized value in numeric comparison at logconv.pl line 949

* Thu Oct 10 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.1-1
- release 1.3.2.1
- Ticket 47513 - tmpfiles.d references /var/lock when they should reference /run/lock
- Ticket 47551 - logconv: -V does not produce unindexed search report
- Ticket 47490 - Schema replication between DS versions may overwrite newer base schema

* Fri Oct 4 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.2.0-1
- release 1.3.2.0
- Ticket 48 - Active Directory has certain uids which are reserved and will cause a Directory Server replica initialization of an AD server to abort.
- Ticket 53 - Need to update supported locales
- Ticket 54 - locale "nl" not supported by collation plugin
- Ticket 77 - [RFE] Add ACI support for ldapi
- Ticket 123 - Enhancement request: "whoami" extended operation
- Ticket 153 - Schema file parsing overly picky?
- Ticket 182 - Pwd retry counters replication not enabled by default, and enabling it could lead to undesired results
- Ticket 197 - rhds82 rfe - BDB backend - clear free page files to reduce changelog size
- Ticket 205 - rhds81 rfe - snmp counters index strings for multiple network interfaces with ip addr and tcp port pairs
- Ticket 208 - [RFE] Roles with explicit scoping in RHDS
- Ticket 283 - Expose slapi_eq_* API
- Ticket 314 - ChainOnUpdate: "cn=directory manager" can modify userRoot on consumer without changes being chained or replicated. Directory integrity compromised.
- Ticket 411 - [RFE] mods optimizer
- Ticket 415 - winsync doesn't sync DN valued attributes if DS DN value doesn't exist
- Ticket 428 - posix winsync should support ADD user/group entries from DS to AD
- Ticket 460 - support multiple subtrees and filters
- Ticket 512 - improve performance of vattr code
- Ticket 513 - recycle operation pblocks
- Ticket 514 - investigate connection locking
- Ticket 521 - modrdn + NSMMReplicationPlugin - Consumer failed to replay change
- Ticket 564 - Is ldbm_txn_ruv_modify_context still required ?
- Ticket 568 - using transaction batchval violates durability
- Ticket 569 - examine replication code to reduce amount of stored state information
- Ticket 586 - selinux errors with /usr/sbin/setup-ds-admin.pl
- Ticket 589 - [RFE] Support RFC 4527 Read Entry Controls
- Ticket 601 - multi master replication allows schema violation
- Ticket 602 - replication inconsistency if attribute is modified several times in one operaion
- Ticket 607 - Replication issue: Entry can diverge betwen servers
- Ticket 609 - nsDS5BeginReplicaRefresh attribute accepts any value and it doesn't throw any error when server restarts.
- Ticket 615 - High contention on cos cache lock
- Ticket 617 - Possible to add invalid ACI value
- Ticket 626 - Possible to add nonexistent target to ACI
- Ticket 630 - The backend name provided to bak2db is not validated
- Ticket 47306 - execute index_add_mods only for indexed attributes
- Ticket 47310 - Attribute "dsOnlyMemberUid" not allowed when syncing nested posix groups from AD with posixWinsync
- Ticket 47313 - Indexed search with filter containing '&' and "!" with attribute subtypes gives wrong result
- Ticket 47314 - Winsync should support range retrieval
- Ticket 47316 - Search against 'view' is always reported as unindexed
- Ticket 47317 - should set LDAP_OPT_X_SASL_NOCANON to LDAP_OPT_ON by default
- Ticket 47319 - make connection buffer size adjustable
- Ticket 47320 - put conn on work_q not poll list if conn has buffered more_data
- Ticket 47323 - resurrected entry is not correctly indexed
- Ticket 47326 - idl switch does not work
- Ticket 47329 - Improve slapi_back_transaction_begin() return code when transactions are not available
- Ticket 47331 - Self entry access ACI not working properly
- Ticket 47337 - mep_pre_op: Unable to fetch origin entry
- Ticket 47340 - Deleting a separator ',' in 7-bit check plugin arguments makes the server fail to start with segfault
- Ticket 47350 - Allow search to look up 'in memory RUV'
- Ticket 47354 - Indexed search are logged with 'notes=U' in the access logs
- Ticket 47358 - backend performance - introduce optimization levels
- Ticket 47360 - Delete attribute could crash the server
- Ticket 47363 - 7-bit checking is not necessary for userPassword
- Ticket 47370 - DS crashes with some 7-bit check plugin configurations
- Ticket 47371 - Some updates of "passwordgraceusertime" are useless when updating "userpassword"
- Ticket 47372 - make old-idl tunable
- Ticket 47381 - nsslapd-db-transaction-batch-val turns to -1
- Ticket 47382 - Add a warning message when a connection hits the max number of threads
- Ticket 47384 - Plugin library path validation
- Ticket 47387 - improve logconv.pl performance with large access logs
- Ticket 47388 - [RFE] Support 'Content Synchronization Operation' (SyncRepl) - RFC 4533
- Ticket 47389 - Non-directory manager can change the individual userPassword's storage scheme
- Ticket 47394 - remove-ds.pl should remove /var/lock/dirsrv
- Ticket 47400 - MMR stress test with dna enabled causes a deadlock
- Ticket 47411 - Replace substring search with plain search in referint plugin
- Ticket 47416 - IPA replica's - "SASL encrypted packet length exceeds maximum allowed limit"
- Ticket 47423 - 7-bit check plugin does not work for userpassword attribute
- Ticket 47425 - should only call windows_update_done if repl agmt type is windows
- Ticket 47426 - move compute_idletimeout out of handle_pr_read_ready
- Ticket 47433 - With SeLinux, ports can be labelled per range. setup-ds.pl or setup-ds-admin.pl fail to detect already ranged labelled ports
- Ticket 47463 - IDL-style can become mismatched during partial restoration
- Ticket 47487 - enhance retro changelog
- Ticket 47502 - updates to ruv entry are written to retro changelog
- Ticket 47504 - idlistscanlimit per index/type/value
- Ticket 47505 - get rid of valueset_add_valuearray_ext
- Ticket 47520 - Fix various issues with logconv.pl
- Ticket 47522 - Password administrators should be able to violate password policy
- Ticket 47531 - 1.3.2 with mozldap - need to redo sasl_io_recv
- Ticket 47532 - 1.3.2 with mozldap - crashes in new operation work_q
- Ticket 47539 - Disabling DNA plug-in throws error 53
- Ticket 47543 - mozldap - fix compiler warnings

* Mon Sep 30 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.11-1
- Ticket 47513 - Set localrundir outside of the "with-fhs" block
- Ticket 47513 - Refine the check for @localrundir@
- Ticket 47510 - remove unnecessary typedef
- Ticket 47510 - Repl Sync does not compile against MozLDAP libraries

* Fri Sep 27 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.10-1
- Ticket #47534 - RUV tombstone search with scope "one" doesn`t work
- Ticket 47510 - 389-ds-base does not compile against MozLDAP libraries
- Ticket #47523 - Set up replcation/agreement before initializing the sub suffix, the sub suffix is not found by ldapsearch
- Ticket 47528 - 389-ds-base built with mozldap can crash from invalid free
- Ticket #47504 idlistscanlimit per index/type/value
- Ticket 47513 - tmpfiles.d references /var/lock when they should reference /run/lock
- Ticket #47492 - PassSync removes User must change password flag on the Windows side
- Ticket 47509 - CLEANALLRUV doesnt run across all replicas
- Ticket #47516 replication stops with excessive clock skew
- 6829200 Coverity fix - 11952 - for Ticket 47512
- Ticket 47512 - backend txn plugin fixup tasks should be done in a txn

* Fri Sep 13 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.9-1
- release 1.3.1.9
- Ticket 449 - Allow macro aci keywords to be case-insensitive
- Ticket 47489 - Under specific values of nsDS5ReplicaName, replication may get broken or updates missing
- Ticket 47507 - automember rebuild task not working as expected

* Fri Sep  6 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.8-1
- Ticket #47455 - valgrind - value mem leaks, uninit mem usage
-  fix breakage in slapi-nis introduced with the previous fix
- Ticket 47500 - start-dirsrv/restart-dirsrv/stop-disrv do not register with systemd correctly

* Wed Aug 28 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.7-1
- bump version to 1.3.1.7
- Bug 1002215 - CVE-2013-4283 389-ds-base: ns-slapd crash due to bogus DN
- Ticket 47488 - Users from AD sub OU does not sync to IPA
- Ticket 47461 - logconv.pl - Use of comma-less variable list is deprecated
- Ticket 47473 - setup-ds.pl doesn't lookup the "root" group correctly

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1.3.1.6-1.1
- Perl 5.18 rebuild

* Thu Aug 01 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-1
- bump version to 1.3.1.6
- Ticket 47455 - valgrind - value mem leaks, uninit mem usage
- fix coverity 11915 - dead code - introduced with fix for ticket 346
- fix coverity 11895 - null deref - caused by fix to ticket 47392
- fix compiler warning in posix winsync code for posix_group_del_memberuid_callback
- Fix compiler warnings for Ticket 47395 and 47397
- fix compiler warning (cherry picked from commit 904416f4631d842a105851b4a9931ae17822a107)
- Ticket 47450 - Fix compiler formatting warning errors for 32/64 bit arch
- fix compiler warnings
- Fix compiler warning (cherry picked from commit ec6ebc0b0f085a82041d993ab2450a3922ef5502)

* Wed Jul 31 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.5-1
- bump version to 1.3.1.5
- Ticket 47456 - delete present values should append values to deleted values
- Ticket 47455 - valgrind - value mem leaks, uninit mem usage
- Ticket 47448 - Segfault in 389-ds-base-1.3.1.4-1.fc19 when setting up FreeIPA replication
- Ticket 47440 - Fix runtime errors caused by last patch.
- Ticket 47440 - Fix compilation warnings and header files
- Ticket 47405 - CVE-2013-2219 ACLs inoperative in some search scenarios
- Ticket 47447 - logconv.pl man page missing -m,-M,-B,-D
- Ticket 47378 - fix recent compiler warnings
- Ticket 47427 - Overflow in nsslapd-disk-monitoring-threshold
- Ticket 47449 - deadlock after adding and deleting entries
- Ticket 47441 - Disk Monitoring not checking filesystem with logs
- Ticket 47427 - Overflow in nsslapd-disk-monitoring-threshold

* Fri Jul 19 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.4-1
- bump version to 1.3.1.4
- Ticket 47435 - Very large entryusn values after enabling the USN plugin and the lastusn value is negative.
- Ticket 47424 - Replication problem with add-delete requests on single-valued attributes
- Ticket 47367 - (phase 2) ldapdelete returns non-leaf entry error while trying to remove a leaf entry
- Ticket 47367 - (phase 1) ldapdelete returns non-leaf entry error while trying to remove a leaf entry
- Ticket 47421 - memory leaks in set_krb5_creds
- Ticket 346 - version 4 Slow ldapmodify operation time for large quantities of multi-valued attribute values
- Ticket 47369  version2 - provide default syntax plugin
- Ticket 47427 - Overflow in nsslapd-disk-monitoring-threshold
- Ticket 47399 - RHDS denies MODRDN access if ACI list contains any DENY rule
- Ticket 47427 - Overflow in nsslapd-disk-monitoring-threshold
- Ticket 47428 - Memory leak in 389-ds-base 1.2.11.15
- Ticket 47392 - ldbm errors when adding/modifying/deleting entries
- Ticket 47385 - Disk Monitoring is not triggered as expected.
- Ticket 47410 - changelog db deadlocks with DNA and replication

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.3.1.3-1.1
- Perl 5.18 rebuild

* Wed Jul 03 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.3-1
- bump version to 1.3.1.3
- Ticket 47374 - flush.pl is not included in perl5
- Ticket 47391 - deleting and adding userpassword fails to update the password (additional fix)
- Ticket 47393 - Attribute are not encrypted on a consumer after a full initialization
- Ticket 47395 47397 - v2 correct behaviour of account policy if only stateattr is configured or no alternate attr is configured
- Ticket 47396 - crash on modrdn of tombstone
- Ticket 47400 - MMR stress test with dna enabled causes a deadlock
- Ticket 47409 - allow setting db deadlock rejection policy
- Ticket 47419 - Unhashed userpassword can accidentally get removed from mods
- Ticket 47420 - An upgrade script 80upgradednformat.pl fails to handle a server instance name incuding '-'

* Sat Jun 15 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.2-1
- bump version to 1.3.1.2
- Ticket 47391 - deleting and adding userpassword fails to update the password
- Coverity Fixes (Part 7)

* Fri Jun 14 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.1-1
- bump version to 1.3.1.1
- Ticket 402 - nhashed#user#password in entry extension
- Ticket 511 - Revision - allow turning off vattr lookup in search entry return
- Ticket 580 - Wrong error code return when using EXTERNAL SASL and no client certificate
- Ticket 47327 - error syncing group if group member user is not synced
- Ticket 47355 - dse.ldif doesn't replicate update to nsslapd-sasl-mapping-fallback
- Ticket 47359 - new ldap connections can block ldaps and ldapi connections
- Ticket 47362 - ipa upgrade selinuxusermap data not replicating
- Ticket 47375 - flush_ber error sending back start_tls response will deadlock
- Ticket 47376 - DESC should not be empty as per RFC 2252 (ldapv3)
- Ticket 47377 - make listen backlog size configurable
- Ticket 47378 - fix recent compiler warnings
- Ticket 47383 - connections attribute in cn=snmp,cn=monitor is counted twice
- Ticket 47385 - DS not shutting down when disk monitoring threshold is reached
- Coverity Fixes (part 1)
- Coverity Fixes (Part 2)
- Coverity Fixes (Part 3)
- Coverity Fixes (Part 4)
- Coverity Fixes (Part 5)

* Thu May 02 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.0-1
- bump version to 1.3.1.0
- Ticket 332 - Command line perl scripts should attempt most secure connection type first
- Ticket 342 - better error message when cache overflows
- Ticket 417 - RFE - forcing passwordmustchange attribute by non-cn=directory manager
- Ticket 419 - logconv.pl - improve memory management
- Ticket 422 - 389-ds-base - Can't call method "getText"
- Ticket 433 - multiple bugs in start-dirsrv, stop-dirsrv, restart-dirsrv scripts
- Ticket 458 - RFE - Make it possible for privileges to be provided to an admin user to import an LDIF file containing hashed passwords
- Ticket 471 - logconv.pl tool removes the access logs contents if "-M" is not correctly used
- Ticket 487 - Possible to add invalid attribute values to PAM PTA plugin configuration
- Ticket 502 - setup-ds.pl script should wait if "semanage.trans.LOCK" presen
- Ticket 505 - use lock-free access name2asi and oid2asi tables (additional)
- Ticket 508 - lock-free access to FrontendConfig structure
- Ticket 511 - allow turning off vattr lookup in search entry return
- Ticket 525 - Introducing a user visible configuration variable for controlling replication retry time
- Ticket 528 - RFE - get rid of instance specific scripts
- Ticket 529 - dn normalization must handle multiple space characters in attributes
- Ticket 532 - RUV is not getting updated for both Master and consumer
- Ticket 533 - only scan for attributes to decrypt if there are encrypted attrs configured
- Ticket 534 - RFE: Add SASL mappings fallback
- Ticket 537 - Improvement of range search
- Ticket 539 - logconv.pl should handle microsecond timing
- Ticket 543 - Sorting with attributes in ldapsearch gives incorrect result
- Ticket 545 - Segfault during initial LDIF import: str2entry_dupcheck()
- Ticket 547 - Incorrect assumption in ndn cache
- Ticket 550 - posix winsync will not create memberuid values if group entry become posix group in the same sync interval
- Ticket 551 - Multivalued rootdn-days-allowed in RootDN Access Control plugin always results in access control violation
- Ticket 552 - Adding rootdn-open-time without rootdn-close-time to RootDN Acess Control results in inconsistent configuration
- Ticket 558 - Replication - make timeout for protocol shutdown configurable
- Ticket 561 - disable writing unhashed#user#password to changelog
- Ticket 563 - DSCreate.pm: Error messages cannot be used in the if expression since they could be localized.
- Ticket 565 - turbo mode and replication - allow disable of turbo mode
- Ticket 571 - server does not accept 0 length LDAP Control sequence
- Ticket 574 - problems with dbcachesize disk space calculation
- Ticket 583 - dirsrv fails to start on reboot due to /var/run/dirsrv permissions
- Ticket 585 - Behaviours of "db2ldif -a <filename>" and "db2ldif.pl -a <filename>" are inconsistent
- Ticket 587 - Replication error messages in the DS error logs
- Ticket 588 - Create MAN pages for command line scripts
- Ticket 600 - Server should return unavailableCriticalExtension when processing a badly formed critical control
- Ticket 603 - A logic error in str2simple
- Ticket 604 - Required attribute not checked during search operation
- Ticket 608 - Posix Winsync plugin throws "posix_winsync_end_update_cb: failed to add task entry" error message
- Ticket 611 - logconv.pl missing stats for StartTLS, LDAPI, and AUTOBIND
- Ticket 612 - improve dbgen rdn generation, output
- Ticket 613 - ldclt: add timestamp, interval, nozeropad, other improvements
- Ticket 616 - High contention on computed attribute lock
- Ticket 618 - Crash at shutdown while stopping replica agreements
- Ticket 620 - Better logging of error messages for 389-ds-base
- Ticket 621 - modify operations without values need to be written to the changelog
- Ticket 622 - DS logging errors "libdb: BDB0171 seek: 2147483648: (262144 * 8192) + 0: No such file or directory
- Ticket 631 - Replication: "Incremental update started" status message without consumer initialized
- Ticket 633 - allow nsslapd-nagle to be disabled, and also tcp cork
- Ticket 47299 - allow cmdline scripts to work with non-root user
- Ticket 47302 - get rid of sbindir start/stop/restart slapd scripts
- Ticket 47303 - start/stop/restart dirsrv scripts should report and error if no instances
- Ticket 47304 - reinitialization of a master with a disabled agreement hangs
- Ticket 47311 - segfault in db2ldif(trigger by a cleanallruv task)
- Ticket 47312 - replace PR_GetFileInfo with PR_GetFileInfo64
- Ticket 47315 - filter option in fixup-memberof requires more clarification
- Ticket 47325 - Crash at shutdown on a replica aggrement
- Ticket 47330 - changelog db extension / upgrade is obsolete
- Ticket 47336 - logconv.pl -m not working for all stats
- Ticket 47341 - logconv.pl -m time calculation is wrong
- Ticket 47343 - 389-ds-base: Does not support aarch64 in f19 and rawhide
- Ticket 47347 - Simple paged results should support async search
- Ticket 47348 - add etimes to per second/minute stats
- Ticket 47349 - DS instance crashes under a high load

* Thu Mar 28 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0.5-1
- bump version to 1.3.0.5
- Ticket 47308 - unintended information exposure when anonymous access is set to rootdse
- Ticket 628 - crash in aci evaluation
- Ticket 627 - ns-slapd crashes sporadically with segmentation fault in libslapd.so
- Ticket 634 - Deadlock in DNA plug-in Ticket #576 - DNA: use event queue for config update only at the start up
- Ticket 632 - 389-ds-base cannot handle Kerberos tickets with PAC
- Ticket 623 - cleanAllRUV task fails to cleanup config upon completion

* Mon Mar 11 2013 Mark Reynolds <mreynolds@redhat.com> - 1.3.0.4-1
- e53d691 bump version to 1.3.0.4
- Bug 912964 - CVE-2013-0312 389-ds: unauthenticated denial of service vulnerability in handling of LDAPv3 control data
- Ticket 570 - DS returns error 20 when replacing values of a multi-valued attribute (only when replication is enabled)
- Ticket 490 - Slow role performance when using a lot of roles
- Ticket 590 - ns-slapd segfaults while trying to delete a tombstone entry

* Wed Feb 13 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0.3-1
- bump version to 1.3.0.3
- Ticket #584 - Existence of an entry is not checked when its password is to be deleted
- Ticket 562 - Crash when deleting suffix

* Fri Feb 01 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.3.0.2-2
- Rebuild for icu 50

* Wed Jan 16 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0.2-1
- bump version to 1.3.0.2
- Ticket #542 - Cannot dynamically set nsslapd-maxbersize

* Wed Jan 16 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0.1-1
- bump version to 1.3.0.1
- Ticket 556 - Don't overwrite certmap.conf during upgrade

* Tue Jan 08 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0.0-1
- bump version to 1.3.0.0

* Tue Jan 08 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0-0.3.rc3
- bump version to 1.3.0.rc3
- Ticket 549 - DNA plugin no longer reports additional info when range is depleted
- Ticket 541 - need to set plugin as off in ldif template
- Ticket 541 - RootDN Access Control plugin is missing after upgrade 

* Fri Dec 14 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0-0.2.rc2
- bump version to 1.3.0.rc2
- Trac Ticket #497 - Escaped character cannot be used in the substring search filter
- Ticket 509 - lock-free access to be->be_suffixlock
- Trac Ticket #522 - betxn: upgrade is not implemented yet

* Tue Dec 11 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0-0.1.rc1
- bump version to 1.3.0.rc1
- Ticket #322 - Create DOAP description for the 389 Directory Server project
- Trac Ticket #499 - Handling URP results is not corrrect
- Ticket 509 - lock-free access to be->be_suffixlock
- Ticket 456 - improve entry cache sizing
- Trac Ticket #531 - loading an entry from the database should use str2entry_f
- Trac Ticket #536 - Clean up compiler warnings for 1.3
- Trac Ticket #531 - loading an entry from the database should use str2entry_fast
- Ticket 509 - lock-free access to be->be_suffixlock
- Ticket 527 - ns-slapd segfaults if it cannot rename the logs
- Ticket 395 - RFE: 389-ds shouldn't advertise in the rootDSE that we can handle a sasl mech if we really can't
- Ticket 216 - disable replication agreements
- Ticket 518 - dse.ldif is 0 length after server kill or machine kill
- Ticket 393 - Change in winSyncInterval does not take immediate effect
- Ticket 20 - Allow automember to work on entries that have already been added
- Coverity Fixes
- Ticket 349 - nsViewFilter syntax issue in 389DS 1.2.5
- Ticket 337 - improve CLEANRUV functionality
- Fix for ticket 504
- Ticket 394 - modify-delete userpassword
- minor fixes for bdb 4.2/4.3 and mozldap
- Trac Ticket #276 - Multiple threads simultaneously working on connection's private buffer causes ns-slapd to abort
- Fix for ticket 465: cn=monitor showing stats for other db instances
- Ticket 507 - use mutex for FrontendConfig lock instead of rwlock
- Fix for ticket 510 Avoid creating an attribute just to determine the syntax for a type, look up the syntax directly by type
- Coverity defect: Resource leak 13110
- Ticket 517 - crash in DNA if no dnaMagicRegen is specified
- Trac Ticket #520 - RedHat Directory Server crashes (segfaults) when moving ldap entry
- Trac Ticket #519 - Search with a complex filter including range search is slow
- Trac Ticket #500 - Newly created users with organizationalPerson objectClass fails to sync from AD to DS with missing attribute error
- Trac Ticket #311 - IP lookup failing with multiple DNS entries
- Trac Ticket #447 - Possible to add invalid attribute to nsslapd-allowed-to-delete-attrs
- Trac Ticket #443 - Deleting attribute present in nsslapd-allowed-to-delete-attrs returns Operations error
- Ticket #503 - Improve AD version in winsync log message
- Trac Ticket #190 - Un-resolvable server in replication agreement produces unclear error message
- Coverity fixes
- Trac Ticket #391 - Slapd crashes when deleting backends while operations are still in progress
- Trac Ticket #448 - Possible to set invalid macros in Macro ACIs
- Trac Ticket #498 - Cannot abaondon simple paged result search
- Coverity defects
- Trac Ticket #494 - slapd entered to infinite loop during new index addition
- Fixing compiler warnings in the posix-winsync plugin
- Coverity defects
- Ticket 147 - Internal Password Policy usage very inefficient
- Ticket 495 - internalModifiersname not updated by DNA plugin
- Revert "Ticket 495 - internalModifiersname not updated by DNA plugin"
- Ticket 495 - internalModifiersname not updated by DNA plugin
- Ticket 468 - if pam_passthru is enabled, need to AC_CHECK_HEADERS([security/pam_appl.h])
- Ticket 486 - nsslapd-enablePlugin should not be multivalued
- Ticket 488 - Doc: DS error log messages with typo
- Trac Ticket #451 - Allow db2ldif to be quiet
- Ticket #491 - multimaster_extop_cleanruv returns wrong error codes
- Ticket #481 - expand nested posix groups
- Trac Ticket #455 - Insufficient rights to unhashed#user#password when user deletes his password
- Ticket #446 - anonymous limits are being applied to directory manager

* Tue Oct 9 2012 Mark Reynolds <mareynol@redhat.com> - 1.3.0.a1-1
- Ticket #28 - MOD operations with chained delete/add get back error 53 on backend config
- Ticket #173 - ds-logpipe.py script's man page and script help should be updated for -t option.
- Ticket #196 - RFE: Interpret IPV6 addresses for ACIs, replication, and chaining 
- Ticket #218 - RFE - Make RIP working with Replicated Entries 
- Ticket #328 - make sure all internal search filters are properly escaped 
- Ticket #329 - 389-admin build fails on F-18 with new apache
- Ticket #344 - deadlock in replica_write_ruv
- Ticket #351 - use betxn plugins by default
- Ticket #352 - make cos, roles, views betxn aware 
- Ticket #356 - logconv.pl - RFE - track bind info
- Ticket #365 - Audit log - clear text password in user changes 
- Ticket #370 - Opening merge qualifier CoS entry using RHDS console changes the entry.
- Ticket #372 - Setting nsslapd-listenhost or nsslapd-securelistenhost breaks ACI processing
- Ticket #386 - Overconsumption of memory with large cachememsize and heavy use of ldapmodify
- Ticket #402 - unhashedTicket #userTicket #password in entry extension
- Ticket #408 - Create a normalized dn cache
- Ticket #453 - db2index with -tattrname:type,type fails
- Ticket #461 - fix build problem with mozldap c sdk 
- Ticket #462 - add test for include file mntent.h 
- Ticket #463 - different parameters of getmntent in Solaris

* Tue Sep 25 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.15-1
- Trac Ticket #470 - 389 prevents from adding a posixaccount with userpassword after schema reload
- Ticket 477 - CLEANALLRUV if there are only winsync agmts task will hang
- Ticket 457 - dirsrv init script returns 0 even when few or all instances fail to start
- Ticket 473 - change VERSION.sh to have console version be major.minor
- Ticket 475 - Root DN Access Control - improve value checking for config
- Trac Ticket #466 - entry_apply_mod - ADD: Failed to set unhashed#user#password to extension
- Ticket 474 - Root DN Access Control - days allowed not working correctly
- Ticket 467 - CLEANALLRUV abort task should be able to ignore down replicas
- 0b79915 fix compiler warnings in ticket 374 code
- Ticket 452 - automember rebuild task adds users to groups that do not match the configuration scope

* Fri Sep  7 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.14-1
- Ticket 450 - CLEANALLRUV task gets stuck on winsync replication agreement
- Ticket 386 - large memory growth with ldapmodify(heap fragmentation)
-  this patch doesn't fix the bug - it allows us to experiment with
-  different values of mxfast
- Ticket #374 - consumer can go into total update mode for no reason

* Tue Sep  4 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.13-1
- Ticket #426 - support posix schema for user and group sync
-   1) plugin config ldif must contain pluginid, etc. during upgrade or it
-      will fail due to schema errors
-   2) posix winsync should have a lower precedence (25) than the default (50)
-      so that it will be run first
-   3) posix winsync should support the Winsync API v3 - the v2 functions are
-      just stubs for now - but the precedence cb is active

* Thu Aug 30 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.12-1
- 8e5087a Coverity defects - 13089: Dereference after null check ldbm_back_delete
- Trac Ticket #437 - variable dn should not be used in ldbm_back_delete
- ba1f5b2 fix coverity resource leak in windows_plugin_add
- e3e81db Simplify program flow: change while loops to for
- a0d5dc0 Fix logic errors: del_mod should be latched (might not be last mod), and avoid skipping add-mods (int value 0)
- 0808f7e Simplify program flow: make adduids/moduids/deluids action blocks all similar
- 77eb760 Simplify program flow: eliminate unnecessary continue
- c9e9db7 Memory leaks: unmatched slapi_attr_get_valueset and slapi_value_new
- a4ca0cc Change "return"s in modGroupMembership to "break"s to avoid leaking
- d49035c Factorize into new isPosixGroup function
- 3b61c03 coverity - posix winsync mem leaks, null check, deadcode, null ref, use after free
- 33ce2a9 fix mem leaks with parent dn log message, setting winsync windows domain
- Ticket #440 - periodic dirsync timed event causes server to loop repeatedly
- Ticket #355 - winsync should not delete entry that appears to be out of scope
- Ticket 436 - nsds5ReplicaEnabled can be set with any invalid values.
- 487932d coverity - mbo dead code - winsync leaks, deadcode, null check, test code
- 2734a71 CLEANALLRUV coverity fixes
- Ticket #426 - support posix schema for user and group sync
- Ticket #430 - server to server ssl client auth broken with latest openldap

* Mon Aug 20 2012 Mark Reynolds <mareynol@redhat.com> - 1.2.11.11-1
6c0778f bumped version to 1.2.11.11
Ticket 429 - added nsslapd-readonly to DS schema
Ticket 403 - fix CLEANALLRUV regression from last commit
Trac Ticket #346 - Slow ldapmodify operation time for large quantities of multi-valued attribute values

* Wed Aug 15 2012 Mark Reynolds <mareynol@redhat.com> - 1.2.11.10-1
db6b354 bumped version to 1.2.11.10
Ticket 403 - CLEANALLRUV revisions

* Tue Aug 7 2012 Mark Reynolds <mareynol@redhat.com> - 1.2.11.9-1
ea05e69 Bumped version to 1.2.11.9
Ticket 407 - dna memory leak - fix crash from prev fix

* Fri Aug 3 2012 Mark Reynolds <mareynol@redhat.com> - 1.2.11.8-1
ddcf669 bump version to 1.2.11.8 for offical release
Ticket #425 - support multiple winsync plugins
Ticket 403 - cleanallruv coverity fixes
Ticket 407 - memory leak in dna plugin
Ticket 403 - CLEANALLRUV feature
Ticket 413 - "Server is unwilling to perform" when running ldapmodify on nsds5ReplicaStripAttrs
3168f04 Coverity defects
5ff0a02 COVERITY FIXES
Ticket #388 - Improve replication agreement status messages
0760116 Update the slapi-plugin documentation on new slapi functions, and added a slapi function for checking on shutdowns
Ticket #369 - restore of replica ldif file on second master after deleting two records shows only 1 deletion
Ticket #409 - Report during startup if nsslapd-cachememsize is too small
Ticket #412 - memberof performance enhancement
12813: Uninitialized pointer read string_values2keys
Ticket #346 - Slow ldapmodify operation time for large quantities of multi-valued attribute values
Ticket #346 - Slow ldapmodify operation time for large quantities of multi-valued attribute values
Ticket #410 - Referential integrity plug-in does not work when update interval is not zero
Ticket #406 - Impossible to rename entry (modrdn) with Attribute Uniqueness plugin enabled
Ticket #405 - referint modrdn not working if case is different
Ticket 399 - slapi_ldap_bind() doesn't check bind results

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11.7-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.2.11.7-2.1
- Perl 5.16 rebuild

* Wed Jun 27 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.7-2
- Ticket 378 - unhashed#user#password visible after changing password
-  fix func declaration from previous patch
- Ticket 366 - Change DS to purge ticket from krb cache in case of authentication error

* Wed Jun 27 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.7-1
- Trac Ticket 396 - Account Usability Control Not Working

* Thu Jun 21 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.6-1
- Ticket #378 - audit log does not log unhashed password: enabled, by default.
- Ticket #378 - unhashed#user#password visible after changing password
- Ticket #365 - passwords in clear text in the audit log

* Tue Jun 19 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.5-2
- workaround for https://bugzilla.redhat.com/show_bug.cgi?id=833529

* Mon Jun 18 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.5-1
- Ticket #387 - managed entry sometimes doesn't delete the managed entry
- 5903815 improve txn test index handling
- Ticket #360 - ldapmodify returns Operations error - fix delete caching
- bcfa9e3 Coverity Fix for CLEANALLRUV
- Trac Ticket #335 - transaction retries need to be cache aware
- Ticket #389 - ADD operations not in audit log
- 44cdc84 fix coverity issues with uninit vals, no return checking
- Ticket 368 - Make the cleanAllRUV task one step
- Ticket #110 - RFE limiting root DN by host, IP, time of day, day of week

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.2.11.4-1.1
- Perl 5.16 rebuild

* Tue May 22 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.4-1
- Ticket #360 - ldapmodify returns Operations error
- Ticket #321 - krbExtraData is being null modified and replicated on each ssh login
- Trac Ticket #359 - Database RUV could mismatch the one in changelog under the stress
- Ticket #361: Bad DNs in ACIs can segfault ns-slapd
- Trac Ticket #338 - letters in object's cn get converted to lowercase when renaming object
- Ticket #337 - Improve CLEANRUV task

* Sat May  5 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.3-1
- Ticket #358 - managed entry doesn't delete linked entry

* Fri May  4 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.2-1
- Ticket #351 - use betxn plugins by default
-   revert - make no plugins betxn by default - too great a risk
-   for deadlocks until we can test this better
- Ticket #348 - crash in ldap_initialize with multiple threads
-   fixes PR_Init problem in ldclt

* Wed May  2 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.1-1
- f227f11 Suppress alert on unavailable port with forced setup
- Ticket #353 - coverity 12625-12629 - leaks, dead code, unchecked return
- Ticket #351 - use betxn plugins by default
- Trac Ticket #345 - db deadlock return should not log error
- Ticket #348 - crash in ldap_initialize with multiple threads
- Ticket #214 - Adding Replication agreement should complain if required nsds5ReplicaCredentials not supplied
- Ticket #207 - [RFE] enable attribute that tracks when a password was last set
- Ticket #216 - RFE - Disable replication agreements
- Ticket #337 - RFE - Improve CLEANRUV functionality
- Ticket #326 - MemberOf plugin should work on all backends
- Trac Ticket #19 - Convert entryUSN plugin to transaction aware type
- Ticket #347 - IPA dirsvr seg-fault during system longevity test
- Trac Ticket #310 - Avoid calling escape_string() for logged DNs
- Trac Ticket #338 - letters in object's cn get converted to lowercase when renaming object
- Ticket #183 - passwordMaxFailure should lockout password one sooner
- Trac Ticket #335 - transaction retries need to be cache aware
- Ticket #336 - [abrt] 389-ds-base-1.2.10.4-2.fc16: index_range_read_ext: Process /usr/sbin/ns-slapd was killed by signal 11 (SIGSEGV)
- Ticket #325 - logconv.pl : use of getopts to parse command line options
- Ticket #336 - [abrt] 389-ds-base-1.2.10.4-2.fc16: index_range_read_ext: Process /usr/sbin/ns-slapd was killed by signal 11 (SIGSEGV)
- 554e29d Coverity Fixes
- Trac Ticket #46 - (additional 2) setup-ds-admin.pl does not like ipv6 only hostnames
- Ticket #183 - passwordMaxFailure should lockout password one sooner - and should be configurable to avoid regressions
- Ticket #315 - small fix to libglobs
- Ticket #315 - ns-slapd exits/crashes if /var fills up
- Ticket #20 - Allow automember to work on entries that have already been added
- Trac Ticket #45 - Fine Grained Password policy: if passwordHistory is on, deleting the password fails.

* Fri Mar 30 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11-0.1.a1
- 453eb97 schema def must have DESC '' - close paren must be preceded by space
- Trac Ticket #46 - (additional) setup-ds-admin.pl does not like ipv6 only hostnames
- Ticket #331 - transaction errors with db 4.3 and db 4.2
- Ticket #261 - Add Solaris i386
- Ticket #316 and Ticket #70 - add post add/mod and AD add callback hooks
- Ticket #324 - Sync with group attribute containing () fails
- Ticket #319 - ldap-agent crashes on start with signal SIGSEGV
- 77cacd9 coverity 12606 Logically dead code
- Trac Ticket #303 - make DNA range requests work with transactions
- Ticket #320 - allow most plugins to be betxn plugins
- Ticket #24 - Add nsTLS1 to the DS schema
- Ticket #271 - Slow shutdown when you have 100+ replication agreements
- TIcket #285 - compilation fixes for '--format-security'
- Ticket 211 - Avoid preop range requests non-DNA operations
- Ticket #271 - replication code cleanup
- Ticket 317 - RHDS fractional replication with excluded password policy attributes leads to wrong error messages.
- Ticket #308 - Automembership plugin fails if data and config area mixed in the plugin configuration
- Ticket #292 - logconv.pl reporting unindexed search with different search base than shown in access logs
- 6f8680a coverity 12563 Read from pointer after free (fix 2)
- e6a9b22 coverity 12563 Read from pointer after free
- 245d494 Config changes fail because of unknown attribute "internalModifiersname"
- Ticket #191  - Implement SO_KEEPALIVE in network calls
- Ticket #289 - allow betxn plugin config changes
- 93adf5f destroy the entry cache and dn cache in the dse post op delete callback
- e2532d8 init txn thread private data for all database modes
- Ticket #291 - cannot use & in a sasl map search filter
- 6bf6e79 Schema Reload crash fix
- 60b2d12 Fixing compiler warnings
- Trac Ticket #260 - 389 DS does not support multiple paging controls on a single connection
- Ticket #302 - use thread local storage for internalModifiersName & internalCreatorsName
- fdcc256 Minor bug fix introcuded by commit 69c9f3bf7dd9fe2cadd5eae0ab72ce218b78820e
- Ticket #306 - void function cannot return value
- ticket 181 - Allow PAM passthru plug-in to have multiple config entries
- ticket 211 - Use of uninitialized variables in ldbm_back_modify()
- Ticket #74 - Add schema for DNA plugin (RFE)
- Ticket #301 - implement transaction support using thread local storage
- Ticket #211 - dnaNextValue gets incremented even if the user addition fails
- 144af59 coverity uninit var and resource leak
- Trac Ticket #34 - remove-ds.pl does not remove everything
- Trac Ticket #169 - allow 389 to use db5
- bc78101 fix compiler warning in acct policy plugin
- Trac Ticket #84 - 389 Directory Server Unnecessary Checkpoints
- Trac Ticket #27 - SASL/PLAIN binds do not work
- Ticket #129 - Should only update modifyTimestamp/modifiersName on MODIFYops
- Ticket #17 - new replication optimizations

* Tue Mar 27 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.2.10.4-4
- Ticket #46 - (revised) setup-ds-admin.pl does not like ipv6 only hostnames
- Ticket #66 - 389-ds-base spec file does not have a BuildRequires on gcc-c++

* Fri Mar 23 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.2.10.4-3
- Ticket #46 - setup-ds-admin.pl does not like ipv6 only hostnames

* Wed Mar 21 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.4-2
- get rid of posttrans - move update code to post

* Tue Mar 13 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.4-1
- Ticket #305 - Certain CMP operations hang or cause ns-slapd to crash

* Mon Mar  5 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.3-1
- b05139b memleak in normalize_mods2bvals
- c0eea24 memleak in mep_parse_config_entry
- 90bc9eb handle null smods
- Ticket #305 - Certain CMP operations hang or cause ns-slapd to crash
- Ticket #306 - void function cannot return value
- ticket 304 - Fix kernel version checking in dsktune

* Thu Feb 23 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.2-1
- Trac Ticket #298 - crash when replicating orphaned tombstone entry
- Ticket #281 - TLS not working with latest openldap
- Trac Ticket #290 - server hangs during shutdown if betxn pre/post op fails
- Trac Ticket #26 - Please support setting defaultNamingContext in the rootdse

* Tue Feb 14 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.2.10.1-2
- Ticket #124 - add Provides: ldif2ldbm to rpm

* Tue Feb 14 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.1-1
- Ticket #294 - 389 DS Segfaults during replica install in FreeIPA

* Mon Feb 13 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.0-1
- Ticket 284 - Remove unnecessary SNMP MIB files
- Ticket 51 - memory leaks in 389-ds-base-1.2.8.2-1.el5?
- Ticket 175 - logconv.pl improvements

* Fri Feb 10 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.2.10-0.10.rc1.2
- Introducing use_db4 macro to support db5 (libdb).

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 1.2.10-0.10.rc1.1
- Rebuild against PCRE 8.30

* Thu Feb  2 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.10.rc1
- ad9dd30 coverity 12488 Resource leak In attr_index_config(): Leak of memory or pointers to system resources
- Ticket #281 - TLS not working with latest openldap
- Ticket #280 - extensible binary filters do not work
- Ticket #279 - filter normalization does not use matching rules
- Trac Ticket #275 - Invalid read reported by valgrind
- Ticket #277 - cannot set repl referrals or state
- Ticket #278 - Schema replication update failed: Invalid syntax
- Ticket #39 - Account Policy Plugin does not work for simple binds when PAM Pass Through Auth plugin is enabled
- Ticket #13 - slapd process exits when put the database on read only mode while updates are coming to the server
- Ticket #87 - Manpages fixes
- c493fb4 fix a couple of minor coverity issues
- Ticket #55 - Limit of 1024 characters for nsMatchingRule
- Trac Ticket #274 - Reindexing entryrdn fails if ancestors are also tombstoned
- Ticket #6 - protocol error from proxied auth operation
- Ticket #38 - nisDomain schema is incorrect
- Ticket #273 - ruv tombstone searches don't work after reindex entryrdn
- Ticket #29 - Samba3-schema is missing sambaTrustedDomainPassword
- Ticket #22 - RFE: Support sendmail LDAP routing schema
- Ticket #161 - Review and address latest Coverity issues
- Ticket #140 - incorrect memset parameters
- Trac Ticket 35 - Log not clear enough on schema errors
- Trac Ticket 139 - eliminate the use of char *dn in favor of Slapi_DN *dn
- Trac Ticket #52 - FQDN set to nsslapd-listenhost makes the server start fail if IPv4-mapped-IPv6 address is given

* Tue Jan 24 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.9.a8
- Ticket #272 - add tombstonenumsubordinates to schema

* Mon Jan 23 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.8.a7
- fixes for systemd - remove .pid files after shutting down servers
- Ticket #263 - add systemd include directive
- Ticket #264 - upgrade needs better check for "server is running"

* Fri Jan 20 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.7.a7
- Ticket #262 - pid file not removed with systemd
- Ticket #50 - server should not call a plugin after the plugin close function is called
- Ticket #18 - Data inconsitency during replication
- Ticket #49 - better handling for server shutdown while long running tasks are active
- Ticket #15 - Get rid of rwlock.h/rwlock.c and just use slapi_rwlock instead
- Ticket #257 - repl-monitor doesn't work if leftmost hostnames are the same
- Ticket #12 - 389 DS DNA Plugin / Replication failing on GSSAPI
- 6aaeb77 add a hack to disable sasl hostname canonicalization
- Ticket 168 - minssf should not apply to rootdse
- Ticket #177 - logconv.pl doesn't detect restarts
- Ticket #159 - Managed Entry Plugin runs against managed entries upon any update without validating
- Ticket 75 - Unconfigure plugin opperations are being called.
- Ticket 26 - Please support setting defaultNamingContext in the rootdse.
- Ticket #71 - unable to delete managed entry config
- Ticket #167 - Mixing transaction and non-transaction plugins can cause deadlock
- Ticket #256 - debug build assertion in ACL_EvalDestroy()
- Ticket #4 - bak2db gets stuck in infinite loop
- Ticket #162 - Infinite loop / spin inside strcmpi_fast, acl_read_access_allowed_on_attr, server DoS
- Ticket #3: acl cache overflown problem
- Ticket 1 - pre-normalize filter and pre-compile substring regex - and other optimizations
- Ticket 2 - If node entries are tombstone'd, subordinate entries fail to get the full DN.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-0.6.a6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.6.a6
- Bug 755725 - 389 programs linked against openldap crash during shutdown
- Bug 755754 - Unable to start dirsrv service using systemd
- Bug 745259 - Incorrect entryUSN index under high load in replicated environment
- d439e3a use slapi_hexchar2int and slapi_str_to_u8 everywhere
- 5910551 csn_init_as_string should not use sscanf
- b53ba00 reduce calls to csn_as_string and slapi_log_error
- c897267 fix member variable name error in slapi_uniqueIDFormat
- 66808e5 uniqueid formatting - use slapi_u8_to_hex instead of sprintf
- 580a875 csn_as_string - use slapi_uN_to_hex instead of sprintf
- Bug 751645 - crash when simple paged fails to send entry to client
- Bug 752155 - Use restorecon after creating init script lock file

* Fri Nov  4 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.5.a5
- Bug 751495 - 'setup-ds.pl -u' fails with undefined routine 'updateSystemD'
- Bug 750625 750624 750622 744946 Coverity issues
- Bug 748575 - part 2 - rhds81 modrdn operation and 100% cpu use in replication
- Bug 748575 - rhds81 modrn operation and 100% cpu use in replication
- Bug 745259 - Incorrect entryUSN index under high load in replicated environment
- f639711 Reduce the number of DN normalization
- c06a8fa Keep unhashed password psuedo-attribute in the adding entry
- Bug 744945 - nsslapd-counters attribute value cannot be set to "off"
- 8d3b921 Use new PLUGIN_CONFIG_ENTRY feature to allow switching between txn and regular
- d316a67 Change referential integrity to be a betxnpostoperation plugin

* Fri Oct  7 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.4.a4
- Bug 741744 - part3 - MOD operations with chained delete/add get back error 53
- 1d2f5a0 make memberof transaction aware and able to be a betxnpostoperation plug in
- b6d3ba7 pass the plugin config entry to the plugin init function
- 28f7bfb set the ENTRY_POST_OP for modrdn betxnpostoperation plugins
- Bug 743966 - Compiler warnings in account usability plugin

* Wed Oct  5 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10.a3-0.3
- 498c42b fix transaction support in ldbm_delete

* Wed Oct  5 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10.a2-0.2
- Bug 740942 - allow resource limits to be set for paged searches independently of limits for other searches/operations
- Bug 741744 - MOD operations with chained delete/add get back error 53 on backend config
- Bug 742324 - allow nsslapd-idlistscanlimit to be set dynamically and per-user

* Wed Sep 21 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10.a1-0.1
- Bug 695736 - Providing native systemd file

* Wed Sep  7 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.10-2
- corrected source

* Wed Sep  7 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.10-1
- Bug 735114 - renaming a managed entry does not update mepmanagedby

* Thu Sep  1 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.9-1
- Bug 735121 - simple paged search + ip/dns based ACI hangs server
- Bug 722292 - (cov#11030) Leak of mapped_sdn in winsync rename code
- Bug 703990 - cross-platform - Support upgrade from Red Hat Directory Server
- Introducing an environment variable USE_VALGRIND to clean up the entry cache and dn cache on exit.

* Wed Aug 31 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.8-1
- Bug 732153 - subtree and user account lockout policies implemented?
- Bug 722292 - Entries in DS are not updated properly when using WinSync API

* Wed Aug 24 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.7-1
- Bug 733103 - large targetattr list with syntax errors cause server to crash or hang
- Bug 633803 - passwordisglobalpolicy attribute brakes TLS chaining
- Bug 732541 - Ignore error 32 when adding automember config
- Bug 728592 - Allow ns-slapd to start with an invalid server cert

* Wed Aug 10 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.6-1
- Bug 728510 - Run dirsync after sending updates to AD
- Bug 729717 - Fatal error messages when syncing deletes from AD
- Bug 729369 - upgrade DB to upgrade from entrydn to entryrdn format is not working.
- Bug 729378 - delete user subtree container in AD + modify password in DS == DS crash
- Bug 723937 - Slapi_Counter API broken on  32-bit F15
-   fixed again - separate tests for atomic ops and atomic bool cas

* Mon Aug  8 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.5-1
- Bug 727511 - ldclt SSL search requests are failing with "illegal error number -1" error
-  Fix another coverity NULL deref in previous patch

* Thu Aug  4 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.4-1
- Bug 727511 - ldclt SSL search requests are failing with "illegal error number -1" error
-  Fix coverity NULL deref in previous patch

* Wed Aug  3 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.3-1
- Bug 727511 - ldclt SSL search requests are failing with "illegal error number -1" error
-  previous patch broke build on el5

* Wed Aug  3 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.2-1
- Bug 727511 - ldclt SSL search requests are failing with "illegal error number -1" error

* Tue Aug  2 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.1-2
- Bug 723937 - Slapi_Counter API broken on  32-bit F15
-   fixed to use configure test for GCC provided 64-bit atomic functions

* Wed Jul 27 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.1-1
- Bug 663752 - Cert renewal for attrcrypt and encchangelog
-   this was "re-fixed" due to a deadlock condition with cl2ldif task cancel
- Bug 725953 - Winsync: DS entries fail to sync to AD, if the User's CN entry contains a comma
- Bug 725743 - Make memberOf use PRMonitor for it's operation lock
- Bug 725542 - Instance upgrade fails when upgrading 389-ds-base package
- Bug 723937 - Slapi_Counter API broken on  32-bit F15

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.2.9.0-1.2
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.2.9.0-1.1
- Perl mass rebuild

* Fri Jul 15 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.0-1
- Bug 720059 - RDN with % can cause crashes or missing entries
- Bug 709468 - RSA Authentication Server timeouts when using simple paged results on RHDS 8.2.
- Bug 691313 - Need TLS/SSL error messages in repl status and errors log
- Bug 712855 - Directory Server 8.2 logs "Netscape Portable Runtime error -5961 (TCP connection reset by peer.)" to error log whereas Directory Server 8.1 did not
- Bug 713209 - Update sudo schema
- Bug 719069 - clean up compiler warnings in 389-ds-base 1.2.9
- Bug 718303 - Intensive updates on masters could break the consumer's cache
- Bug 711679 - unresponsive LDAP service when deleting vlv on replica

* Mon Jun 27 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9-0.2.a2
- 389-ds-base-1.2.9.a2
- look for separate openldap ldif library
- Split automember regex rules into separate entries
- writing Inf file shows SchemaFile = ARRAY(0xhexnum)
- add support for ldif files with changetype: add
- Bug 716980 - winsync uses old AD entry if new one not found
- Bug 697694 - rhds82 - incr update state stop_fatal_error "requires administrator action", with extop_result: 9
- bump console version to 1.2.6
- Bug 711679 - unresponsive LDAP service when deleting vlv on replica
- Bug 703703 - setup-ds-admin.pl asks for legal agreement to a non-existant file
- Bug 706209 - LEGAL: RHEL6.1 License issue for 389-ds-base package
- Bug 663752 - Cert renewal for attrcrypt and encchangelog
- Bug 706179 - DS can not restart after create a new objectClass has entryusn attribute
- Bug 711906 - ns-slapd segfaults using suffix referrals
- Bug 707384 - only allow FIPS approved cipher suites in FIPS mode
- Bug 710377 - Import with chain-on-update crashes ns-slapd
- Bug 709826 - Memory leak: when extra referrals configured

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.9-0.1.a1.2
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.9-0.1.a1.1
- Perl 5.14 mass rebuild

* Thu May 26 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9-0.1.a1
- 389-ds-base-1.2.9.a1
- Auto Membership
- More Coverity fixes

* Mon May  2 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8.3-1
- 389-ds-base-1.2.8.3
- Bug 700145 - userpasswd not replicating
- Bug 700557 - Linked attrs callbacks access free'd pointers after close
- Bug 694336 - Group sync hangs Windows initial Sync
- Bug 700215 - ldclt core dumps
- Bug 695779 - windows sync can lose old values when a new value is added
- Bug 697027 - 12 - minor memory leaks found by Valgrind + TET

* Thu Apr 14 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8.2-1
- 389-ds-base-1.2.8.2
- Bug 696407 - If an entry with a mixed case RDN is turned to be
-    a tombstone, it fails to assemble DN from entryrdn

* Fri Apr  8 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8.1-1
- 389-ds-base-1.2.8.1
- Bug 693962 - Full replica push loses some entries with multi-valued RDNs

* Tue Apr  5 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8.0-1
- 389-ds-base-1.2.8.0
- Bug 693473 - rhds82 rfe - windows_tot_run to log Sizelimit exceeded instead of LDAP error - -1
- Bug 692991 - rhds82 - windows_tot_run: failed to obtain data to send to the consumer; LDAP error - -1
- Bug 693466 - Unable to change schema online
- Bug 693503 - matching rules do not inherit from superior attribute type
- Bug 693455 - nsMatchingRule does not work with multiple values
- Bug 693451 - cannot use localized matching rules
- Bug 692331 - Segfault on index update during full replication push on 1.2.7.5

* Mon Apr  4 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.10.rc5
- 389-ds-base-1.2.8.rc5
- Bug 692469 - Replica install fails after step for "enable GSSAPI for replication"

* Tue Mar 29 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.9.rc4
- 389-ds-base-1.2.8.rc4
- Bug 668385 - DS pipe log script is executed as many times as the dirsrv serv
ice is restarted
- 389-ds-base-1.2.8.rc3
- Bug 690955 - Mrclone fails due to the replica generation id mismatch

* Tue Mar 22 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.8.rc2
- 389-ds-base-1.2.8 release candidate 2 - git tag 389-ds-base-1.2.8.rc2
- Bug 689537 - (cov#10610) Fix Coverity NULL pointer dereferences
- Bug 689866 - ns-newpwpolicy.pl needs to use the new DN format
- Bug 681015 - RFE: allow fine grained password policy duration attributes
-              in days, hours, minutes, as well
- Bug 684996 - Exported tombstone cannot be imported correctly
- Bug 683250 - slapd crashing when traffic replayed
- Bug 668909 - Can't modify replication agreement in some cases
- Bug 504803 - Allow maxlogsize to be set if logmaxdiskspace is -1
- Bug 644784 - Memory leak in "testbind.c" plugin
- Bug 680558 - Winsync plugin fails to restrain itself to the configured subtree

* Mon Mar  7 2011 Caolán McNamara <caolanm@redhat.com> - 1.2.8-0.7.rc1
- rebuild for icu 4.6

* Wed Mar  2 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.6.rc1
- 389-ds-base-1.2.8 release candidate 1 - git tag 389-ds-base-1.2.8.rc1
- Bug 518890 - setup-ds-admin.pl - improve hostname validation
- Bug 681015 - RFE: allow fine grained password policy duration attributes in 
-     days, hours, minutes, as well
- Bug 514190 - setup-ds-admin.pl --debug does not log to file
- Bug 680555 - ns-slapd segfaults if I have more than 100 DBs
- Bug 681345 - setup-ds.pl should set SuiteSpotGroup automatically
- Bug 674852 - crash in ldap-agent when using OpenLDAP
- Bug 679978 - modifying attr value crashes the server, which is supposed to
-     be indexed as substring type, but has octetstring syntax
- Bug 676655 - winsync stops working after server restart
- Bug 677705 - ds-logpipe.py script is failing to validate "-s" and
-     "--serverpid" options with "-t".
- Bug 625424 - repl-monitor.pl doesn't work in hub node

* Mon Feb 28 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.5.a3
- Bug 676598 - 389-ds-base multilib: file conflicts
- split off libs into a separate -libs package

* Thu Feb 24 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.4.a3
- do not create /var/run/dirsrv - setup will create it instead
- remove the fedora-ds initscript upgrade stuff - we do not support that anymore
- convert the remaining lua stuff to plain old shell script

* Wed Feb  9 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.3.a3
- 1.2.8.a3 release - git tag 389-ds-base-1.2.8.a3
- Bug 675320 - empty modify operation with repl on or lastmod off will crash server
- Bug 675265 - preventryusn gets added to entries on a failed delete
- Bug 677774 - added support for tmpfiles.d
- Bug 666076 - dirsrv crash (1.2.7.5) with multiple simple paged result search
es
- Bug 672468 - Don't use empty path elements in LD_LIBRARY_PATH
- Bug 671199 - Don't allow other to write to rundir
- Bug 678646 - Ignore tombstone operations in managed entry plug-in
- Bug 676053 - export task followed by import task causes cache assertion
- Bug 677440 - clean up compiler warnings in 389-ds-base 1.2.8
- Bug 675113 - ns-slapd core dump in windows_tot_run if oneway sync is used
- Bug 676689 - crash while adding a new user to be synced to windows
- Bug 604881 - admin server log files have incorrect permissions/ownerships
- Bug 668385 - DS pipe log script is executed as many times as the dirsrv serv
ice is restarted
- Bug 675853 - dirsrv crash segfault in need_new_pw()

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-0.2.a2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.2.a2
- 1.2.8.a2 release - git tag 389-ds-base-1.2.8.a2
- Bug 674430 - Improve error messages for attribute uniqueness
- Bug 616213 - insufficient stack size for HP-UX on PA-RISC
- Bug 615052 - intrinsics and 64-bit atomics code fails to compile
-    on PA-RISC
- Bug 151705 - Need to update Console Cipher Preferences with new ciphers
- Bug 668862 - init scripts return wrong error code
- Bug 670616 - Allow SSF to be set for local (ldapi) connections
- Bug 667935 - DS pipe log script's logregex.py plugin is not redirecting the 
-    log output to the text file
- Bug 668619 - slapd stops responding
- Bug 624547 - attrcrypt should query the given slot/token for
-    supported ciphers
- Bug 646381 - Faulty password for nsmultiplexorcredentials does not give any 
-    error message in logs

* Fri Jan 21 2011 Nathan Kinder <nkinder@redhat.com> - 1.2.8-0.1.a1
- 1.2.8-0.1.a1 release - git tag 389-ds-base-1.2.8.a1
- many bug fixes

* Thu Dec 16 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.5-1
- 1.2.7.5 release - git tag 389-ds-base-1.2.7.5
- Bug 663597 - Memory leaks in normalization code

* Tue Dec 14 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.4-2
- Resolves: bug 656541 - use %%ghost on files in /var/lock

* Fri Dec 10 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.4-1
- 1.2.7.4 release - git tag 389-ds-base-1.2.7.4
- Bug 661792 - Valid managed entry config rejected

* Wed Dec  8 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.3-1
- 1.2.7.3 release - git tag 389-ds-base-1.2.7.3
- Bug 658312 - Invalid free in Managed Entry plug-in
- Bug 641944 - Don't normalize non-DN RDN values

* Fri Dec  3 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.2-1
- 1.2.7.2 release - git tag 389-ds-base-1.2.7.2
- Bug 659456 - Incorrect usage of ber_printf() in winsync code
- Bug 658309 - Process escaped characters in managed entry mappings
- Bug 197886 - Initialize return value for UUID generation code
- Bug 658312 - Allow mapped attribute types to be quoted
- Bug 197886 - Avoid overflow of UUID generator

* Tue Nov 23 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.1-2
- last commit had bogus commit log

* Tue Nov 23 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.1-1
- 1.2.7.1 release - git tag 389-ds-base-1.2.7.1
- Bug 656515 - Allow Name and Optional UID syntax for grouping attributes
- Bug 656392 - Remove calls to ber_err_print()
- Bug 625950 - hash nsslapd-rootpw changes in audit log

* Tue Nov 16 2010 Nathan Kinder <nkinder@redhat.com> - 1.2.7-2
- 1.2.7 release - git tag 389-ds-base-1.2.7

* Fri Nov 12 2010 Nathan Kinder <nkinder@redhat.com> - 1.2.7-1
- Bug 648949 - Merge dirsrv and dirsrv-admin policy modules into base policy

* Tue Nov  9 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.6.a5
- 1.2.7.a5 release - git tag 389-ds-base-1.2.7.a5
- Bug 643979 - Strange byte sequence for attribute with no values (nsslapd-ref
erral)
- Bug 635009 - Add one-way AD sync capability
- Bug 572018 - Upgrading from 1.2.5 to 1.2.6.a2 deletes userRoot
- put replication config entries in separate file
- Bug 567282 - server can not abandon searchRequest of "simple paged results"
- Bug 329751 - "nested" filtered roles searches candidates more than needed
- Bug 521088 - DNA should check ACLs before getting a value from the range

* Mon Nov  1 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.5.a4
- 1.2.7.a4 release - git tag 389-ds-base-1.2.7.a4
- Bug 647932 - multiple memberOf configuration adding memberOf where there is 
no member
- Bug 491733 - dbtest crashes
- Bug 606545 - core schema should include numSubordinates
- Bug 638773 - permissions too loose on pid and lock files
- Bug 189985 - Improve attribute uniqueness error message
- Bug 619623 - attr-unique-plugin ignores requiredObjectClass on modrdn operat
ions
- Bug 619633 - Make attribute uniqueness obey requiredObjectClass

* Wed Oct 27 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.4.a3
- 1.2.7.a3 release - a2 was never released - this is a rebuild to pick up
- Bug 644608 - RHDS 8.1->8.2 upgrade fails to properly migrate ACIs
- Adding the ancestorid fix code to ##upgradednformat.pl.

* Fri Oct 22 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.3.a3
- 1.2.7.a3 release - a2 was never released
- Bug 644608 - RHDS 8.1->8.2 upgrade fails to properly migrate ACIs
- Bug 629681 - Retro Changelog trimming does not behave as expected
- Bug 645061 - Upgrade: 06inetorgperson.ldif and 05rfc4524.ldif
-              are not upgraded in the server instance schema dir

* Tue Oct 19 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.2.a2
- 1.2.7.a2 release - a1 was the OpenLDAP testday release
- git tag 389-ds-base-1.2.7.a2
- added openldap support on platforms that use openldap with moznss
- for crypto (F-14 and later)
- many bug fixes
- Account Policy Plugin (keep track of last login, disable old accounts)

* Fri Oct  8 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.1.a1
- added openldap support

* Wed Sep 29 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6.1-3
- bump rel to rebuild again

* Mon Sep 27 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6.1-2
- bump rel to rebuild

* Thu Sep 23 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6.1-1
- This is the 1.2.6.1 release - git tag 389-ds-base-1.2.6.1
- Bug 634561 - Server crushes when using Windows Sync Agreement
- Bug 635987 - Incorrect sub scope search result with ACL containing ldap:///self
- Bug 612264 - ACI issue with (targetattr='userPassword')
- Bug 606920 - anonymous resource limit- nstimelimit - also applied to "cn=directory manager"
- Bug 631862 - crash - delete entries not in cache + referint

* Thu Aug 26 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-1
- This is the final 1.2.6 release

* Tue Aug 10 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.11.rc7
- 1.2.6 release candidate 7
- git tag 389-ds-base-1.2.6.rc7
- Bug 621928 - Unable to enable replica (rdn problem?) on 1.2.6 rc6

* Mon Aug  2 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.10.rc6
- 1.2.6 release candidate 6
- git tag 389-ds-base-1.2.6.rc6
- Bug 617013 - repl-monitor.pl use cpu upto 90%
- Bug 616618 - 389 v1.2.5 accepts 2 identical entries with different DN formats
- Bug 547503 - replication broken again, with 389 MMR replication and TCP errors
- Bug 613833 - Allow dirsrv_t to bind to rpc ports
- Bug 612242 - membership change on DS does not show on AD
- Bug 617629 - Missing aliases in new schema files
- Bug 619595 - Upgrading sub suffix under non-normalized suffix disappears
- Bug 616608 - SIGBUS in RDN index reads on platforms with strict alignments
- Bug 617862 - Replication: Unable to delete tombstone errors
- Bug 594745 - Get rid of dirsrv_lib_t label

* Wed Jul 14 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.9.rc3
- make selinux-devel explicit Require the base package in order
- to comply with Fedora Licensing Guidelines

* Thu Jul  1 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.8.rc3
- 1.2.6 release candidate 3
- git tag 389-ds-base-1.2.6.rc3
- Bug 603942 - null deref in _ger_parse_control() for subjectdn
- 609256  - Selinux: pwdhash fails if called via Admin Server CGI
- 578296  - Attribute type entrydn needs to be added when subtree rename switch is on
- 605827 - In-place upgrade: upgrade dn format should not run in setup-ds-admin.pl
- Bug 604453 - SASL Stress and Server crash: Program quits with the assertion failure in PR_Poll
- Bug 604453 - SASL Stress and Server crash: Program quits with the assertion failure in PR_Poll
- 606920 - anonymous resource limit - nstimelimit - also applied to "cn=directory manager"

* Wed Jun 16 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.7.rc2
- 1.2.6 release candidate 2

* Mon Jun 14 2010 Nathan Kinder <nkinder@redhat.com> - 1.2.6-0.6.rc1
- install replication session plugin header with devel package

* Wed Jun  9 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.5.rc1
- 1.2.6 release candidate 1

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2.6-0.4.a4.1
- Mass rebuild with perl-5.12.0

* Wed May 26 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.4.a4
- 1.2.6.a4 release

* Wed Apr  7 2010 Nathan Kinder <nkinder@redhat.com> - 1.2.6-0.4.a3
- 1.2.6.a3 release
- add managed entries plug-in
- many bug fixes
- moved selinux subpackage into base package

* Fri Apr  2 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.6-0.3.a2
- rebuild for icu 4.4

* Tue Mar  2 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.2.a2
- 1.2.6.a2 release
- add support for matching rules
- many bug fixes

* Thu Jan 14 2010 Nathan Kinder <nkinder@redhat.com> - 1.2.6-0.1.a1
- 1.2.6.a1 release
- Added SELinux policy and subpackages

* Tue Jan 12 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.5-1
- 1.2.5 final release

* Mon Jan  4 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.5-0.5.rc4
- 1.2.5.rc4 release

* Thu Dec 17 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.5-0.4.rc3
- 1.2.5.rc3 release

* Mon Dec  7 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.5-0.3.rc2
- 1.2.5.rc2 release

* Wed Dec  2 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.5-0.2.rc1
- 1.2.5.rc1 release

* Thu Nov 12 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.5-0.1.a1
- 1.2.5.a1 release

* Thu Oct 29 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.4-1
- 1.2.4 release
- resolves bug 221905 - added support for Salted MD5 (SMD5) passwords - primarily for migration
- resolves bug 529258 - Make upgrade remove obsolete schema from 99user.ldif

* Mon Sep 14 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.3-1
- 1.2.3 release
- added template-initconfig to %%files
- %%posttrans now runs update to update the server instances
- servers are shutdown, then restarted if running before install
- scriptlets mostly use lua now to pass data among scriptlet phases

* Tue Sep 01 2009 Caolán McNamara <caolanm@redhat.com> - 1.2.2-2
- rebuild with new openssl to fix dependencies

* Tue Aug 25 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.2-1
- backed out - added template-initconfig to %%files - this change is for the next major release
- bump version to 1.2.2
- fix reopened 509472 db2index all does not reindex all the db backends correctly
- fix 518520 -  pre hashed salted passwords do not work
- see https://bugzilla.redhat.com/show_bug.cgi?id=518519 for the list of
- bugs fixed in 1.2.2

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.1-5
- rebuilt with new openssl

* Wed Aug 19 2009 Noriko Hosoi <nhosoi@redhat.com> - 1.2.1-4
- added template-initconfig to %%files

* Wed Aug 12 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.1-3
- added BuildRequires pcre

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.1-1
- change name to 389
- change version to 1.2.1
- added initial support for numeric string syntax
- added initial support for syntax validation
- added initial support for paged results including sorting

* Tue Apr 28 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.0-4
- final release 1.2.0
- Resolves: bug 475338 - LOG: the intenal type of maxlogsize, maxdiskspace and minfreespace should be 64-bit integer
- Resolves: bug 496836 - SNMP ldap-agent on Solaris: Unable to open semaphore for server: 389
- CVS tag: FedoraDirSvr_1_2_0 FedoraDirSvr_1_2_0_20090428

* Mon Apr  6 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.0-3
- re-enable ppc builds

* Thu Apr  2 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.0-2
- exclude ppc builds - needs extensive porting work

* Mon Mar 30 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.0-1
- new release 1.2.0
- Made devel package depend on mozldap-devel
- only create run dir if it does not exist
- CVS tag: FedoraDirSvr_1_2_0_RC1 FedoraDirSvr_1_2_0_RC1_20090330

* Thu Oct 30 2008 Noriko Hosoi <nhosoi@redhat.com> - 1.1.3-7
- added db4-utils to Requires for verify-db.pl

* Mon Oct 13 2008 Noriko Hosoi <nhosoi@redhat.com> - 1.1.3-6
- Enabled LDAPI autobind

* Thu Oct  9 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.3-5
- updated update to patch bug463991-bdb47.patch

* Thu Oct  9 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.3-4
- updated patch bug463991-bdb47.patch

* Mon Sep 29 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.3-3
- added patch bug463991-bdb47.patch
- make ds work with bdb 4.7

* Wed Sep 24 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.3-2
- rolled back bogus winsync memory leak fix

* Tue Sep 23 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.3-1
- winsync api improvements for modify operations

* Fri Jun 13 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.2-1
- This is the 1.1.2 release.  The bugs fixed can be found here
- https://bugzilla.redhat.com/showdependencytree.cgi?id=452721
- Added winsync-plugin.h to the devel subpackage

* Fri Jun  6 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.1-2
- bump rev to rebuild and pick up new version of ICU

* Fri May 23 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.1-1
- 1.1.1 release candidate - several bug fixes

* Wed Apr 16 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.0.1-4
- fix bugzilla 439829 - patch to allow working with NSS 3.11.99 and later

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.0.1-3
- add patch to allow server to work with NSS 3.11.99 and later
- do NSS_Init after fork but before detaching from console

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.0.1-3
- add Requires for versioned perl (libperl.so)

* Wed Feb 27 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.0.1-2
- previous fix for 434403 used the wrong patch
- this is the right one

* Wed Feb 27 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.0.1-1
- Resolves bug 434403 - GCC 4.3 build fails
- Rolled new source tarball which includes Nathan's fix for the struct ucred
- NOTE: Change version back to 1.1.1 for next release
- this release was pulled from CVS tag FedoraDirSvr110_gcc43

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.0-5
- Autorebuild for GCC 4.3

* Thu Dec 20 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-4
- This is the GA release of Fedora DS 1.1
- Removed version numbers for BuildRequires and Requires
- Added full URL to source tarball

* Fri Dec 07 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.1.0-3
- Rebuild for deps

* Wed Nov  7 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-2.0
- This is the beta2 release
- new file added to package - /etc/sysconfig/dirsrv - for setting
- daemon environment as is usual in other linux daemons

* Thu Aug 16 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.2
- fix build breakage due to open()
- mock could not find BuildRequires: db4-devel >= 4.2.52
- mock works if >= version is removed - it correctly finds db4.6

* Fri Aug 10 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.1
- Change pathnames to use the pkgname macro which is dirsrv
- get rid of cvsdate in source name

* Fri Jul 20 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.3.20070720
- Added Requires for perldap, cyrus sasl plugins
- Removed template-migrate* files
- Added perl module directory
- Removed install.inf - setup-ds.pl can now easily generate one

* Mon Jun 18 2007 Nathan Kinder <nkinder@redhat.com> - 1.1.0-0.2.20070320
- added requires for mozldap-tools

* Tue Mar 20 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.1.20070320
- update to latest sources
- added migrateTo11 to allow migrating instances from 1.0.x to 1.1
- ldapi support
- fixed pam passthru plugin ENTRY method

* Fri Feb 23 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.1.20070223
- Renamed package to fedora-ds-base, but keep names of paths/files/services the same
- use the shortname macro (fedora-ds) for names of paths, files, and services instead
- of name, so that way we can continue to use e.g. /etc/fedora-ds instead of /etc/fedora-ds-base
- updated to latest sources

* Tue Feb 13 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.1.20070213
- More cleanup suggested by Dennis Gilmore
- This is the fedora extras candidate based on cvs tag FedoraDirSvr110a1

* Fri Feb  9 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.el4.20070209
- latest sources
- added init scripts
- use /etc as instconfigdir

* Wed Feb  7 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.el4.20070207
- latest sources
- moved all executables to _bindir

* Mon Jan 29 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.el4.20070129
- latest sources
- added /var/tmp/fedora-ds to dirs

* Fri Jan 26 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-8.el4.20070125
- added logconv.pl
- added slapi-plugin.h to devel package
- added explicit dirs for /var/log/fedora-ds et. al.

* Thu Jan 25 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-7.el4.20070125
- just move all .so files into the base package from the devel package

* Thu Jan 25 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-6.el4.20070125
- Move the plugin *.so files into the main package instead of the devel
- package because they are loaded directly by name via dlopen

* Fri Jan 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-5.el4.20070125
- Move the script-templates directory to datadir/fedora-ds

* Fri Jan 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-4.el4.20070119
- change mozldap to mozldap6

* Fri Jan 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-3.el4.20070119
- remove . from cvsdate define

* Fri Jan 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-2.el4.20070119
- Having a problem building in Brew - may be Release format

* Fri Jan 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.el4.cvs20070119
- Changed version to 1.1.0 and added Release 1.el4.cvs20070119
- merged in changes from Fedora Extras candidate spec file

* Mon Jan 15 2007 Rich Megginson <rmeggins@redhat.com> - 1.1-0.1.cvs20070115
- Bump component versions (nspr, nss, svrcore, mozldap) to their latest
- remove unneeded patches

* Tue Jan 09 2007 Dennis Gilmore <dennis@ausil.us> - 1.1-0.1.cvs20070108
- update to a cvs snapshot
- fedorafy the spec 
- create -devel subpackage
- apply a patch to use mozldap not mozldap6
- apply a patch to allow --prefix to work correctly

* Mon Dec 4 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-16
- Fixed the problem where the server would crash upon shutdown in dblayer
- due to a race condition among the database housekeeping threads
- Fix a problem with normalized absolute paths for db directories

* Tue Nov 28 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-15
- Touch all of the ldap/admin/src/scripts/*.in files so that they
- will be newer than their corresponding script template files, so
- that make will rebuild them.

* Mon Nov 27 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-14
- Chown new schema files when copying during instance creation

* Tue Nov 21 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-13
- Configure will get ldapsdk_bindir from pkg-config, or $libdir/mozldap6

* Tue Nov 21 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-12
- use eval to sed ./configure into ../configure

* Tue Nov 21 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-11
- jump through hoops to be able to run ../configure

* Tue Nov 21 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-10
- Need to make built dir in setup section

* Tue Nov 21 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-9
- The template scripts needed to use @libdir@ instead of hardcoding
- /usr/lib
- Use make DESTDIR=$RPM_BUILD_ROOT install instead of % makeinstall
- do the actual build in a "built" subdirectory, until we remove
- the old script templates

* Thu Nov 16 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-8
- Make replication plugin link with libdb

* Wed Nov 15 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-7
- Have make define LIBDIR, BINDIR, etc. for C code to use
- especially for create_instance.h

* Tue Nov 14 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-6
- Forgot to checkin new config.h.in for AC_CONFIG_HEADERS

* Tue Nov 14 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-5
- Add perldap as a Requires; update sources

* Thu Nov 9 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-4
- Fix ds_newinst.pl
- Remove obsolete #defines

* Thu Nov 9 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-3
- Update sources; rebuild to populate brew yum repo with dirsec-nss

* Tue Nov 7 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-2
- Update sources

* Thu Nov 2 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-1
- initial revision
