
%global pkgname   dirsrv
# for a pre-release, define the prerel field e.g. .a1 .rc2 - comment out for official release
# also remove the space between % and global - this space is needed because
# fedpkg verrel stupidly ignores comment lines
#% global prerel .rc3
# also need the relprefix field for a pre-release e.g. .0 - also comment out for official release
#% global relprefix 0.

%global use_openldap 1
%global use_db4 0
# If perl-Socket-2.000 or newer is available, set 0 to use_Socket6.
%global use_Socket6 0

# fedora 15 and later uses tmpfiles.d
# otherwise, comment this out
%{!?with_tmpfiles_d: %global with_tmpfiles_d %{_sysconfdir}/tmpfiles.d}

# systemd support
%global groupname %{pkgname}.target

# set PIE flag
%global _hardened_build 1

Summary:          389 Directory Server (base)
Name:             389-ds-base
Version:          1.3.3.1
Release:          %{?relprefix}16%{?prerel}%{?dist}
License:          GPLv2 with exceptions
URL:              http://port389.org/
Group:            System Environment/Daemons
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes:        %{name}-selinux
Conflicts:        selinux-policy-base < 3.9.8
Requires:         %{name}-libs = %{version}-%{release}
Provides:         ldif2ldbm 

BuildRequires:    nspr-devel
BuildRequires:    nss-devel
BuildRequires:    svrcore-devel
%if %{use_openldap}
BuildRequires:    openldap-devel
%else
BuildRequires:    mozldap-devel
%endif
%if %{use_db4}
BuildRequires:    db4-devel
%else
BuildRequires:    libdb-devel
%endif
BuildRequires:    cyrus-sasl-devel
BuildRequires:    icu
BuildRequires:    libicu-devel
BuildRequires:    pcre-devel
BuildRequires:    gcc-c++
# The following are needed to build the snmp ldap-agent
BuildRequires:    net-snmp-devel
%ifnarch sparc sparc64 ppc ppc64 s390 s390x
BuildRequires:    lm_sensors-devel
%endif
BuildRequires:    bzip2-devel
BuildRequires:    zlib-devel
BuildRequires:    openssl-devel
BuildRequires:    tcp_wrappers
# the following is for the pam passthru auth plug-in
BuildRequires:    pam-devel
BuildRequires:    systemd-units

# this is needed for using semanage from our setup scripts
Requires:         policycoreutils-python

# the following are needed for some of our scripts
%if %{use_openldap}
Requires:         openldap-clients
%else
Requires:         mozldap-tools
%endif
# use_openldap assumes perl-Mozilla-LDAP is built with openldap support
Requires:         perl-Mozilla-LDAP

# this is needed to setup SSL if you are not using the
# administration server package
Requires:         nss-tools

# these are not found by the auto-dependency method
# they are required to support the mandatory LDAP SASL mechs
Requires:         cyrus-sasl-gssapi
Requires:         cyrus-sasl-md5

# this is needed for verify-db.pl
%if %{use_db4}
Requires:         db4-utils
%else
Requires:         libdb-utils
%endif

# This picks up libperl.so as a Requires, so we add this versioned one
Requires:         perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# for the init script
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

# for setup-ds.pl to support ipv6 
%if %{use_Socket6}
Requires:         perl-Socket6
%else
Requires:         perl-Socket
%endif
Requires:         perl-NetAddr-IP

Source0:          http://port389.org/sources/%{name}-%{version}%{?prerel}.tar.bz2
# 389-ds-git.sh should be used to generate the source tarball from git
Source1:          %{name}-git.sh
Source2:          %{name}-devel.README
Patch0:           0000-Ticket-47748-Simultaneous-adding-a-user-and-binding-.patch
Patch1:           0001-Ticket-47834-Tombstone_to_glue-if-parents-are-also-c.patch
Patch2:           0002-Ticket-47890-minor-memory-leaks-in-utilities.patch
Patch3:           0003-fix-for-47885-did-not-always-return-a-response-contr.patch
Patch4:           0004-Ticket-47838-harden-the-list-of-ciphers-available-by.patch
Patch5:           0005-Ticket-47838-47895-CI-test-add-test-cases-for-ticket.patch
Patch6:           0006-Ticket-47895-If-no-effective-ciphers-are-available-d.patch
Patch7:           0007-Ticket-47889-DS-crashed-during-ipa-server-install-on.patch
Patch8:           0008-Ticket-47892-coverity-defects-found-in-1.3.3.1.patch
Patch9:           0009-Ticket-47750-Creating-a-glue-fails-if-one-above-leve.patch
Patch10:          0010-Ticket-47908-389-ds-1.3.3.0-does-not-adjust-cipher-s.patch
Patch11:          0011-Ticket-47838-harden-the-list-of-ciphers-available-by.patch
Patch12:          0012-Ticket-47838-CI-test-adjusted-test-cases-based-on-th.patch
Patch13:          0013-Ticket-47880-provide-enabled-ciphers-as-search-resul.patch
Patch14:          0014-Ticket-47880-CI-test-added-test-cases-for-ticket-478.patch
Patch15:          0015-Ticket-47892-coverity-defects-found-in-1.3.3.x.patch
Patch16:          0016-Ticket-47918-result-of-dna_dn_is_shared_config-is-in.patch
Patch17:          0017-Ticket-47892-Fix-remaining-compiler-warnings.patch
Patch18:          0018-Ticket-47919-ldbm_back_modify-SLAPI_PLUGIN_BE_PRE_MO.patch
Patch19:          0019-Ticket-47920-Encoding-of-SearchResultEntry-is-missin.patch
Patch20:          0020-Ticket-47897-Need-to-move-slapi_pblock_set-pb-SLAPI_.patch
Patch21:          0021-Ticket-47922-dynamically-added-macro-aci-is-not-eval.patch
Patch22:          0022-Ticket-47928-Disable-SSL-v3-by-default.patch
Patch23:          0023-Ticket-47928-CI-test-added-test-cases-for-ticket-479.patch
Patch24:          0024-Ticket-47937-Crash-in-entry_add_present_values_wsi_m.patch
Patch25:          0025-Ticket-47928-Disable-SSL-v3-by-default.patch
Patch26:          0026-Ticket-47939-Malformed-cookie-for-LDAP-Sync-makes-DS.patch
Patch27:          0027-Ticket-47945-Add-SSL-TLS-version-info-to-the-access-.patch
Patch28:          0028-Ticket-47948-ldap_sasl_bind-fails-assertion-ld-NULL-.patch
Patch29:          0029-Ticket-47953-Should-not-check-aci-syntax-when-deleti.patch
Patch30:          0030-Ticket-47928-Disable-SSL-v3-by-default.patch
Patch31:          0031-Fix-for-CVE-2014-8112.patch
Patch32:          0032-Ticket-47942-DS-hangs-during-online-total-update.patch
Patch33:          0033-Fix-for-CVE-2014-8105.patch
Patch34:          0034-Additional-fix-for-ticket-47526-v3.patch
Patch35:          0035-fix-jenkins-warning.patch
Patch36:          0036-Ticket-47950-Bind-DN-tracking-unable-to-write-to-int.patch
Patch37:          0037-Ticket-47949-logconv.pl-support-parsing-showing-repo.patch
Patch38:          0038-Ticket-47947-start-dirsrv-after-chrony-on-RHEL7-and-.patch
Patch39:          0039-Ticket-47967-cos_cache_build_definition_list-does-no.patch
Patch40:          0040-Ticket-47969-COS-memory-leak-when-rebuilding-the-cac.patch
Patch41:          0041-Ticket-47969-Fix-coverity-issue.patch
Patch42:          0042-Ticket-47970-Account-lockout-attributes-incorrectly-.patch
Patch43:          0043-Ticket-47970-add-lib389-testcase.patch
Patch44:          0044-Ticket-47960-cookie_change_info-returns-random-negat.patch
Patch45:          0045-Ticket-47960-cookie_change_info-returns-random-negat.patch
Patch46:          0046-Ticket-47636-Error-log-levels-not-displayed-correctl.patch
Patch47:          0047-Ticket-47722-Using-the-filter-file-does-not-work.patch
Patch48:          0048-Ticket-47451-Need-to-unregister-tasks-created-by-plu.patch
Patch49:          0049-Ticket-47451-Running-a-plugin-task-can-crash-the-ser.patch
Patch50:          0050-Ticket-47451-Dynamic-Plugin-various-fixes.patch
Patch51:          0051-Ticket-47451-Fix-jenkins-errors.patch
Patch52:          0052-Ticket-47451-Add-Dynamic-Plugin-CI-Suite.patch
Patch53:          0053-Ticket-47525-Crash-if-setting-invalid-plugin-config-.patch
Patch54:          0054-Ticket-47965-Fix-coverity-issues-2014-11-24.patch
Patch55:          0055-Ticket-47965-Fix-coverity-issues-2014-12-16.patch
Patch56:          0056-Ticket-47750-During-delete-operation-do-not-refresh-.patch
Patch57:          0057-Ticket-47989-Windows-Sync-accidentally-cleared-raw_e.patch
Patch58:          0058-Ticket-47991-upgrade-script-fails-if-etc-and-var-are.patch
Patch59:          0059-Ticket-47988-Schema-learning-mechanism-in-replicatio.patch
Patch60:          0060-Ticket-47988-Schema-learning-mechanism-in-replicatio.patch
Patch61:          0061-Ticket-48005-ns-slapd-crash-in-shutdown-phase.patch
Patch62:          0062-CVE-2015-1854-389ds-base-access-control-bypass-with-.patch

%description
389 Directory Server is an LDAPv3 compliant server.  The base package includes
the LDAP server and command line utilities for server administration.

%package          libs
Summary:          Core libraries for 389 Directory Server
Group:            System Environment/Daemons
BuildRequires:    nspr-devel
BuildRequires:    nss-devel
BuildRequires:    svrcore-devel
%if %{use_openldap}
BuildRequires:    openldap-devel
%else
BuildRequires:    mozldap-devel
%endif
%if %{use_db4}
BuildRequires:    db4-devel
%else
BuildRequires:    libdb-devel
%endif
BuildRequires:    cyrus-sasl-devel
BuildRequires:    libicu-devel
BuildRequires:    pcre-devel

%description      libs
Core libraries for the 389 Directory Server base package.  These libraries
are used by the main package and the -devel package.  This allows the -devel
package to be installed with just the -libs package and without the main package.

%package          devel
Summary:          Development libraries for 389 Directory Server
Group:            Development/Libraries
Requires:         %{name}-libs = %{version}-%{release}
Requires:         pkgconfig
Requires:         nspr-devel
Requires:         nss-devel
Requires:         svrcore-devel
%if %{use_openldap}
Requires:         openldap-devel
%else
Requires:         mozldap-devel
%endif

%description      devel
Development Libraries and headers for the 389 Directory Server base package.

%prep
%setup -q -n %{name}-%{version}%{?prerel}
cp %{SOURCE2} README.devel
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch62 -p1

%build
%if %{use_openldap}
OPENLDAP_FLAG="--with-openldap"
%endif
%{?with_tmpfiles_d: TMPFILES_FLAG="--with-tmpfiles-d=%{with_tmpfiles_d}"}
# hack hack hack https://bugzilla.redhat.com/show_bug.cgi?id=833529
NSSARGS="--with-svrcore-inc=%{_includedir} --with-svrcore-lib=%{_libdir} --with-nss-lib=%{_libdir} --with-nss-inc=%{_includedir}/nss3"
%configure --enable-autobind --with-selinux $OPENLDAP_FLAG $TMPFILES_FLAG \
           --with-systemdsystemunitdir=%{_unitdir} \
           --with-systemdsystemconfdir=%{_sysconfdir}/systemd/system \
           --with-systemdgroupname=%{groupname} $NSSARGS

# Generate symbolic info for debuggers
export XCFLAGS=$RPM_OPT_FLAGS

%ifarch x86_64 ppc64 ia64 s390x sparc64
export USE_64=1
%endif

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT 

make DESTDIR="$RPM_BUILD_ROOT" install

mkdir -p $RPM_BUILD_ROOT/var/log/%{pkgname}
mkdir -p $RPM_BUILD_ROOT/var/lib/%{pkgname}
mkdir -p $RPM_BUILD_ROOT/var/lock/%{pkgname}

# for systemd
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/%{groupname}.wants

#remove libtool and static libs
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/plugins/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/plugins/*.la

# make sure perl scripts have a proper shebang 
sed -i -e 's|#{{PERL-EXEC}}|#!/usr/bin/perl|' $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/script-templates/template-*.pl

%clean
rm -rf $RPM_BUILD_ROOT

%post
output=/dev/null
%systemd_post %{pkgname}-snmp.service
# reload to pick up any changes to systemd files
/bin/systemctl daemon-reload >$output 2>&1 || :
# reload to pick up any shared lib changes
/sbin/ldconfig
# restart the snmp subagent if needed
/bin/systemctl try-restart %{pkgname}-snmp.service > $output 2>&1 || :
# find all instances
instances="" # instances that require a restart after upgrade
ninst=0 # number of instances found in total
if [ -n "$DEBUGPOSTTRANS" ] ; then
   output=$DEBUGPOSTTRANS
fi
echo looking for services in %{_sysconfdir}/systemd/system/%{groupname}.wants/* >> $output 2>&1 || :
for service in %{_sysconfdir}/systemd/system/%{groupname}.wants/* ; do
    if [ ! -f "$service" ] ; then continue ; fi # in case nothing matches
    inst=`echo $service | sed -e 's,%{_sysconfdir}/systemd/system/%{groupname}.wants/,,'`
    echo found instance $inst - getting status >> $output 2>&1 || :
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
    %{_sbindir}/setup-ds.pl -l $output -$DEBUGPOSTSETUPOPT -u -s General.UpdateMode=offline >> $output 2>&1 || :
else
    %{_sbindir}/setup-ds.pl -l $output -u -s General.UpdateMode=offline >> $output 2>&1 || :
fi

# restart instances that require it
for inst in $instances ; do
    echo restarting instance $inst >> $output 2>&1 || :
    /bin/systemctl start $inst >> $output 2>&1 || :
done
exit 0

%preun
if [ $1 -eq 0 ]; then # Final removal
    # Package removal, not upgrade
    %systemd_preun %{pkgname}-snmp.service %{groupname}
    # remove instance specific service files/links
    rm -rf %{_sysconfdir}/systemd/system/%{groupname}.wants/* > /dev/null 2>&1 || :
fi

%postun
/sbin/ldconfig
if [ $1 = 0 ]; then # Final removal
    rm -rf /var/run/%{pkgname}
fi

%files
%defattr(-,root,root,-)
%doc LICENSE EXCEPTION LICENSE.GPLv2
%dir %{_sysconfdir}/%{pkgname}
%dir %{_sysconfdir}/%{pkgname}/schema
%config(noreplace)%{_sysconfdir}/%{pkgname}/schema/*.ldif
%dir %{_sysconfdir}/%{pkgname}/config
%dir %{_sysconfdir}/systemd/system/%{groupname}.wants
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/slapd-collations.conf
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/certmap.conf
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/ldap-agent.conf
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/template-initconfig
%config(noreplace)%{_sysconfdir}/sysconfig/%{pkgname}
%config(noreplace)%{_sysconfdir}/sysconfig/%{pkgname}.systemd
%{_datadir}/%{pkgname}
%{_unitdir}
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/%{pkgname}/perl
%{_libdir}/%{pkgname}/python
%dir %{_libdir}/%{pkgname}/plugins
%{_libdir}/%{pkgname}/plugins/*.so
%dir %{_localstatedir}/lib/%{pkgname}
%dir %{_localstatedir}/log/%{pkgname}
%ghost %dir %{_localstatedir}/lock/%{pkgname}
%{_mandir}/man1/*
%{_mandir}/man8/*

%files devel
%defattr(-,root,root,-)
%doc LICENSE EXCEPTION LICENSE.GPLv2 README.devel
%{_includedir}/%{pkgname}
%{_libdir}/%{pkgname}/libslapd.so
%{_libdir}/pkgconfig/*

%files libs
%defattr(-,root,root,-)
%doc LICENSE EXCEPTION LICENSE.GPLv2 README.devel
%dir %{_libdir}/%{pkgname}
%{_libdir}/%{pkgname}/libslapd.so.*
%{_libdir}/%{pkgname}/libns-dshttpd.so*

%changelog
* Tue Apr 21 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-16
- release 1.3.3.1-16
- Resolves: bug 1212894 - CVE-2015-1854 389ds-base: access control bypass with modrdn

* Mon Feb 23 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-15
- release 1.3.3.1-15
- Setting correct build tag 'rhel-7.1-z-candidate'

* Mon Feb 23 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-14
- release 1.3.3.1-14
- Resolves: bug 1189154 - DNS errors after IPA upgrade due to broken ReplSync (DS 48030)
            Fixes spec file to make sure all the server instances are stopped before upgrade
- Resolves: bug 1186548 - ns-slapd crash in shutdown phase (DS 48005)

* Sun Jan 25 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-13
- release 1.3.3.1-13
- Resolves: bug 1183655 - Fixed Covscan FORWARD_NULL defects (DS 47988)

* Sun Jan 25 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-12
- release 1.3.3.1-12
- Resolves: bug 1182477 - Windows Sync accidentally cleared raw_entry (DS 47989)
- Resolves: bug 1180325 - upgrade script fails if /etc and /var are on different file systems (DS 47991 )
- Resolves: bug 1183655 - Schema learning mechanism, in replication, unable to extend an existing definition (DS 47988)

* Mon Jan  5 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-11
- release 1.3.3.1-11
- Resolves: bug 1080186 - During delete operation do not refresh cache entry if it is a tombstone (DS 47750)

* Wed Dec 17 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-10
- release 1.3.3.1-10
- Resolves: bug 1172731 - CVE-2014-8112 password hashing bypassed when "nsslapd-unhashed-pw-switch" is set to off 
- Resolves: bug 1166265 - DS hangs during online total update (DS 47942)
- Resolves: bug 1168151 - CVE-2014-8105 information disclosure through 'cn=changelog' subtree
- Resolves: bug 1044170 - Allow memberOf suffixes to be configurable (DS 47526)
- Resolves: bug 1171356 - Bind DN tracking unable to write to internalModifiersName without special permissions (DS 47950)
- Resolves: bug 1153737 - logconv.pl -- support parsing/showing/reporting different protocol versions (DS 47949)
- Resolves: bug 1171355 - start dirsrv after chrony on RHEL7 and Fedora (DS 47947)
- Resolves: bug 1170707 - cos_cache_build_definition_list does not stop during server shutdown (DS 47967)
- Resolves: bug 1170708 - COS memory leak when rebuilding the cache (DS - Ticket 47969)
- Resolves: bug 1170709 - Account lockout attributes incorrectly updated after failed SASL Bind (DS 47970)
- Resolves: bug 1166260 - cookie_change_info returns random negative number if there was no change in a tree (DS 47960)
- Resolves: bug 1012991 - Error log levels not displayed correctly (DS 47636)
- Resolves: bug 1108881 - rsearch filter error on any search filter (DS 47722)
- Resolves: bug 994690  - Allow dynamically adding/enabling/disabling/removing plugins without requiring a server restart (DS 47451)
- Resolves: bug 1162997 - Running a plugin task can crash the server (DS 47451)
- Resolves: bug 1166252 - RHEL7.1 ns-slapd segfault when ipa-replica-install restarts (DS 47451)
- Resolves: bug 1172597 - Crash if setting invalid plugin config area for MemberOf Plugin (DS 47525)
- Resolves: bug 1139882 - coverity defects found in 1.3.3.x (DS 47965)
		    
* Thu Nov 13 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-9
- release 1.3.3.1-9
- Resolves: bug 1153737 - Disable SSL v3, by default. (DS 47928)
- Resolves: bug 1163461 - Should not check aci syntax when deleting an aci (DS 47953)

* Mon Nov 10 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-8
- release 1.3.3.1-8
- Resolves: bug 1156607 - Crash in entry_add_present_values_wsi_multi_valued (DS 47937)
- Resolves: bug 1153737 - Disable SSL v3, by default (DS 47928, DS 47945, DS 47948)
- Resolves: bug 1158804 - Malformed cookie for LDAP Sync makes DS crash (DS 47939)

* Thu Oct 23 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-7
- release 1.3.3.1-7
- Resolves: bug 1153737 - Disable SSL v3, by default (DS 47928)

* Fri Oct 10 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-6
- release 1.3.3.1-6
- Resolves: bug 1151287 - dynamically added macro aci is not evaluated on the fly (DS 47922)
- Resolves: bug 1080186 - Need to move slapi_pblock_set(pb, SLAPI_MODRDN_EXISTING_ENTRY, original_entry->ep_entry) prior to original_entry overwritten (DS 47897)
- Resolves: bug 1150694 - Encoding of SearchResultEntry is missing tag (DS 47920)
- Resolves: bug 1150695 - ldbm_back_modify SLAPI_PLUGIN_BE_PRE_MODIFY_FN does not return even if one of the preop plugins fails. (DS 47919)
- Resolves: bug 1139882 - Fix remaining compiler warnings (DS 47892)
- Resolves: bug 1150206 - result of dna_dn_is_shared_config is incorrectly used (DS 47918)

* Wed Oct  1 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-5
- release 1.3.3.1-5
- Resolves: bug 1139882 - coverity defects found in 1.3.3.x (DS 47892)

* Wed Oct  1 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-4
- release 1.3.3.1-4
- Resolves: bug 1080186 - Creating a glue fails if one above level is a conflict or missing  (DS 47750)
- Resolves: bug 1145846 - 389-ds 1.3.3.0 does not adjust cipher suite configuration on upgrade, breaks itself and pki-server (DS 47908)
- Resolves: bug 1117979 - harden the list of ciphers available by default (phase 2) (DS 47838)
                        - provide enabled ciphers as search result (DS 47880)

* Fri Sep 12 2014 Rich Megginson <nhosoi@redhat.com> - 1.3.3.1-3
- release 1.3.3.1-3
- Resolves: bug 1139882 - coverity defects found in 1.3.3.1

* Thu Sep 11 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-2
- release 1.3.3.1-2
- Resolves: bug 1079099 - Simultaneous adding a user and binding as the user could fail in the password policy check (DS 47748)
- Resolves: bug 1080186 - Creating a glue fails if one above level is a conflict or missing (DS 47834)
- Resolves: bug 1139882 - coverity defects found in 1.3.3.1 (DS 47890)
- Resolves: bug 1112702 - Broken dereference control with the FreeIPA 4.0 ACIs (DS 47885 - deref plugin should not return references with noc access rights)
- Resolves: bug 1117979 - harden the list of ciphers available by default (DS 47838, DS 47895)
- Resolves: bug 1080186 - Creating a glue fails if one above level is a conflict or missing (DS 47889 - DS crashed during ipa-server-install on test_ava_filter)

* Fri Sep  5 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-1
- release 1.3.3.1-1
- Resolves: bug 746646 - RFE: easy way to configure which users and groups to sync with winsync
- Resolves: bug 881372 - nsDS5BeginReplicaRefresh attribute accepts any value and it doesn't throw any error when server restarts.
- Resolves: bug 920597 - Possible to add invalid ACI value
- Resolves: bug 921162 - Possible to add nonexistent target to ACI
- Resolves: bug 923799 - if nsslapd-cachememsize set to the number larger than the RAM available, should result in proper error message.
- Resolves: bug 924937 - Attribute "dsOnlyMemberUid" not allowed when syncing nested posix groups from AD with posixWinsync
- Resolves: bug 951754 - Self entry access ACI not working properly
- Resolves: bug 952517 - Dirsrv instance failed to start with Segmentation fault (core dump) after modifying 7-bit check plugin
- Resolves: bug 952682 - nsslapd-db-transaction-batch-val turns to -1
- Resolves: bug 966443 - Plugin library path validation
- Resolves: bug 975176 - Non-directory manager can change the individual userPassword's storage scheme
- Resolves: bug 979465 - IPA replica's - "SASL encrypted packet length exceeds maximum allowed limit"
- Resolves: bug 982597 - Some attributes in cn=config should not be multivalued
- Resolves: bug 987009 - 389-ds-base - shebang with /usr/bin/env
- Resolves: bug 994690 - RFE: Allow dynamically adding/enabling/disabling/removing plugins without requiring a server restart
- Resolves: bug 1012991 - errorlog-level 16384 is listed as 0 in cn=config
- Resolves: bug 1013736 - Enabling/Disabling DNA plug-in throws "ldap_modify: Server Unwilling to Perform (53)" error
- Resolves: bug 1014380 - setup-ds.pl doesn't lookup the "root" group correctly
- Resolves: bug 1020459 - rsa_null_sha should not be enabled by default
- Resolves: bug 1024541 - start dirsrv after ntpd
- Resolves: bug 1029959 - Managed Entries betxnpreoperation - transaction not aborted upon failure to create managed entry
- Resolves: bug 1031216 - add dbmon.sh
- Resolves: bug 1044133 - Indexed search with filter containing '&' and "!" with attribute subtypes gives wrong result
- Resolves: bug 1044134 - should set LDAP_OPT_X_SASL_NOCANON to LDAP_OPT_ON by default
- Resolves: bug 1044135 - make connection buffer size adjustable
- Resolves: bug 1044137 - posix winsync should support ADD user/group entries from DS to AD
- Resolves: bug 1044138 - mep_pre_op: Unable to fetch origin entry
- Resolves: bug 1044139 - [RFE] Support RFC 4527 Read Entry Controls
- Resolves: bug 1044140 - Allow search to look up 'in memory RUV'
- Resolves: bug 1044141 - MMR stress test with dna enabled causes a deadlock
- Resolves: bug 1044142 - winsync doesn't sync DN valued attributes if DS DN value doesn't exist
- Resolves: bug 1044143 - modrdn + NSMMReplicationPlugin - Consumer failed to replay change
- Resolves: bug 1044144 - resurrected entry is not correctly indexed
- Resolves: bug 1044146 - Add a warning message when a connection hits the max number of threads
- Resolves: bug 1044147 - 7-bit check plugin does not work for userpassword attribute
- Resolves: bug 1044148 - The backend name provided to bak2db is not validated
- Resolves: bug 1044149 - Winsync should support range retrieval
- Resolves: bug 1044150 - 7-bit checking is not necessary for userPassword
- Resolves: bug 1044151 - With SeLinux, ports can be labelled per range. setup-ds.pl or setup-ds-admin.pl fail to detect already ranged labelled ports
- Resolves: bug 1044152 - ChainOnUpdate: "cn=directory manager" can modify userRoot on consumer without changes being chained or replicated. Directory integrity compromised.
- Resolves: bug 1044153 - mods optimizer
- Resolves: bug 1044154 - multi master replication allows schema violation
- Resolves: bug 1044156 - DS crashes with some 7-bit check plugin configurations
- Resolves: bug 1044157 - Some updates of "passwordgraceusertime" are useless when updating "userpassword"
- Resolves: bug 1044159 - [RFE] Support 'Content Synchronization Operation' (SyncRepl) - RFC 4533
- Resolves: bug 1044160 - remove-ds.pl should remove /var/lock/dirsrv
- Resolves: bug 1044162 - enhance retro changelog
- Resolves: bug 1044163 - updates to ruv entry are written to retro changelog
- Resolves: bug 1044164 - Password administrators should be able to violate password policy
- Resolves: bug 1044168 - Schema replication between DS versions may overwrite newer base schema
- Resolves: bug 1044169 - ACIs do not allow attribute subtypes in targetattr keyword
- Resolves: bug 1044170 - Allow memberOf suffixes to be configurable
- Resolves: bug 1044171 - Allow referential integrity suffixes to be configurable
- Resolves: bug 1044172 - Plugin library path validation prevents intentional loading of out-of-tree modules
- Resolves: bug 1044173 - make referential integrity configuration more flexible
- Resolves: bug 1044177 - allow configuring changelog trim interval
- Resolves: bug 1044179 - objectclass may, must lists skip rest of objectclass once first is found in sup
- Resolves: bug 1044180 - memberOf on a user is converted to lowercase
- Resolves: bug 1044181 - report unindexed internal searches
- Resolves: bug 1044183 - With 1.3.04 and subtree-renaming OFF, when a user is deleted after restarting the server, the same entry can't be added
- Resolves: bug 1044185 - dbscan on entryrdn should show all matching values
- Resolves: bug 1044187 - logconv.pl - RFE - add on option for a minimum etime for unindexed search stats
- Resolves: bug 1044188 - Recognize compressed log files
- Resolves: bug 1044191 - support TLSv1.1 and TLSv1.2, if supported by NSS
- Resolves: bug 1044193 - default nsslapd-sasl-max-buffer-size should be 2MB
- Resolves: bug 1044194 - Complex filter in a search request doen't work as expected.
- Resolves: bug 1044196 - Automember plug-in should treat MODRDN operations as ADD operations
- Resolves: bug 1044198 - Replication of the schema may overwrite consumer 'attributetypes' even if consumer definition is a superset
- Resolves: bug 1044202 - db2bak.pl issue when specifying non-default directory
- Resolves: bug 1044203 - Allow referint plugin to use an alternate config area
- Resolves: bug 1044205 - Allow memberOf to use an alternate config area
- Resolves: bug 1044210 - idl switch does not work
- Resolves: bug 1044211 - make old-idl tunable
- Resolves: bug 1044212 - IDL-style can become mismatched during partial restoration
- Resolves: bug 1044213 - backend performance - introduce optimization levels
- Resolves: bug 1044215 - using transaction batchval violates durability
- Resolves: bug 1044216 - examine replication code to reduce amount of stored state information
- Resolves: bug 1048980 - 7-bit check plugin not checking MODRDN operation
- Resolves: bug 1049030 - Windows Sync group issues
- Resolves: bug 1052751 - Page control does not work if effective rights control is specified
- Resolves: bug 1052754 - Allow nsDS5ReplicaBindDN to be a group DN
- Resolves: bug 1057803 - logconv errors when search has invalid bind dn
- Resolves: bug 1060032 - [RFE] Update lastLoginTime also in Account Policy plugin if account lockout is based on passwordExpirationTime.
- Resolves: bug 1061060 - betxn: retro changelog broken after cancelled transaction
- Resolves: bug 1061572 - improve dbgen rdn generation, output and man page.
- Resolves: bug 1063990 - single valued attribute replicated ADD does not work
- Resolves: bug 1064006 - Size returned by slapi_entry_size is not accurate
- Resolves: bug 1064986 - Replication retry time attributes cannot be added
- Resolves: bug 1067090 - Missing warning for invalid replica backoff configuration
- Resolves: bug 1072032 - Updating nsds5ReplicaHost attribute in a replication agreement fails with error 53
- Resolves: bug 1074306 - Under heavy stress, failure of turning a tombstone into glue makes the server hung
- Resolves: bug 1074447 - Part of DNA shared configuration is deleted after server restart
- Resolves: bug 1076729 - Continuous add/delete of an entry in MMR setup causes entryrdn-index conflict
- Resolves: bug 1077884 - ldap/servers/slapd/back-ldbm/dblayer.c: possible minor problem with sscanf
- Resolves: bug 1077897 - Memory leak with proxy auth control
- Resolves: bug 1079099 - Simultaneous adding a user and binding as the user could fail in the password policy check
- Resolves: bug 1080186 - Creating a glue fails if one above level is a conflict or missing
- Resolves: bug 1082967 - attribute uniqueness plugin fails when set as a chaining component
- Resolves: bug 1085011 - Directory Server crash reported from reliab15 execution
- Resolves: bug 1086890 - empty modify returns LDAP_INVALID_DN_SYNTAX
- Resolves: bug 1086902 - mem leak in do_bind when there is an error
- Resolves: bug 1086904 - mem leak in do_search - rawbase not freed upon certain errors
- Resolves: bug 1086908 - Performing deletes during tombstone purging results in operation errors
- Resolves: bug 1090178 - #481 breaks possibility to reassemble memberuid list
- Resolves: bug 1092099 - A replicated MOD fails (Unwilling to perform) if it targets a tombstone
- Resolves: bug 1092342 - nsslapd-ndn-cache-max-size accepts any invalid value.
- Resolves: bug 1092648 - Negative value of nsSaslMapPriority is not reset to lowest priority
- Resolves: bug 1097004 - Problem with deletion while replicated
- Resolves: bug 1098654 - db2bak.pl error with changelogdb
- Resolves: bug 1099654 - Normalization from old DN format to New DN format doesnt handel condition properly when there is space in a suffix after the seperator operator.
- Resolves: bug 1108405 - find a way to remove replication plugin errors messages "changelog iteration code returned a dummy entry with csn %s, skipping ..."
- Resolves: bug 1108407 - managed entry plugin fails to update managed entry pointer on modrdn operation
- Resolves: bug 1108865 - memory leak in ldapsearch filter objectclass=*
- Resolves: bug 1108870 - ACI warnings in error log
- Resolves: bug 1108872 - Logconv.pl with an empty access log gives lots of errors
- Resolves: bug 1108874 - logconv.pl memory continually grows
- Resolves: bug 1108881 - rsearch filter error on any search filter
- Resolves: bug 1108895 - [RFE - RHDS9] CLI report to monitor replication
- Resolves: bug 1108902 - rhds91 389-ds-base-1.2.11.15-31.el6_5.x86_64 crash in db4 __dbc_get_pp env = 0x0 ?
- Resolves: bug 1108909 - single valued attribute replicated ADD does not work
- Resolves: bug 1109334 - 389 Server crashes if uniqueMember is invalid syntax and memberOf plugin is enabled.
- Resolves: bug 1109336 - Parent numsubordinate count can be incorrectly updated if an error occurs
- Resolves: bug 1109339 - Nested tombstones become orphaned after purge
- Resolves: bug 1109354 - Tombstone purging can crash the server if the backend is stopped/disabled
- Resolves: bug 1109357 - Coverity issue in 1.3.3
- Resolves: bug 1109364 - valgrind - value mem leaks, uninit mem usage
- Resolves: bug 1109375 - provide default syntax plugin
- Resolves: bug 1109378 - Environment variables are not passed when DS is started via service
- Resolves: bug 1111364 - Updating winsync one-way sync does not affect the behaviour dynamically
- Resolves: bug 1112824 - Broken dereference control with the FreeIPA 4.0 ACIs
- Resolves: bug 1113605 - server restart wipes out index config if there is a default index
- Resolves: bug 1115177 - attrcrypt_generate_key calls slapd_pk11_TokenKeyGenWithFlags with improper macro
- Resolves: bug 1117021 - Server deadlock if online import started while server is under load
- Resolves: bug 1117975 - paged results control is not working in some cases when we have a subsuffix.
- Resolves: bug 1117979 - harden the list of ciphers available by default
- Resolves: bug 1117981 - Fix various typos in manpages & code
- Resolves: bug 1117982 - Fix hyphens used as minus signed and other manpage mistakes
- Resolves: bug 1118002 - server crashes deleting a replication agreement
- Resolves: bug 1118006 - RFE - forcing passwordmustchange attribute by non-cn=directory manager
- Resolves: bug 1118007 - [RFE] Make it possible for privileges to be provided to an admin user to import an LDIF file containing hashed passwords
- Resolves: bug 1118014 - Enhance ACIs to have more control over MODRDN operations
- Resolves: bug 1118021 - Return all attributes in rootdse without explicit request
- Resolves: bug 1118025 - Slow ldapmodify operation time for large quantities of multi-valued attribute values
- Resolves: bug 1118032 - Schema Replication Issue
- Resolves: bug 1118034 - 389 DS Server crashes and dies while handles paged searches from clients
- Resolves: bug 1118043 - Failed deletion of aci: no such attribute
- Resolves: bug 1118048 - If be_txn plugin fails in ldbm_back_add, adding entry is double freed.
- Resolves: bug 1118051 - Add switch to disable pre-hashed password checking
- Resolves: bug 1118054 - Make ldbm_back_seq independently support transactions
- Resolves: bug 1118055 - Add operations rejected by betxn plugins remain in cache
- Resolves: bug 1118057 - online import crashes server if using verbose error logging
- Resolves: bug 1118059 - add fixup-memberuid.pl script
- Resolves: bug 1118060 - winsync plugin modify is broken
- Resolves: bug 1118066 - memberof scope: allow to exclude subtrees
- Resolves: bug 1118069 - 389-ds production segfault: __memcpy_sse2_unaligned () at ../sysdeps/x86_64/multiarch/memcpy-sse2-unaligned.S:144
- Resolves: bug 1118074_DELETE_FN - plugin returned error" messages
- Resolves: bug 1118076 - ds logs many "Operation error fetching Null DN" messages
- Resolves: bug 1118077 - Improve import logging and abort handling
- Resolves: bug 1118079 - Multi master replication initialization incomplete after restore of one master
- Resolves: bug 1118080 - Don't add unhashed password mod if we don't have an unhashed value
- Resolves: bug 1118081 - Investigate betxn plugins to ensure they return the correct error code
- Resolves: bug 1118082 - The error result text message should be obtained just prior to sending result
- Resolves: bug 1123865 - CVE-2014-3562 389-ds-base: 389-ds: unauthenticated information disclosure [rhel-7.1] 

* Fri May  2 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-26
- release 1.3.1.6-26
- Resolves: bug 1085011 - Directory Server crash reported from reliab15 execution (Ticket 346)

* Mon Mar 31 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-25
- release 1.3.1.6-25
- Resolves: bug 1082740 - ns-slapd crash in reliability 15

* Thu Mar 13 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-24
- release 1.3.1.6-24
- Resolves: bug 1074084 - e_uniqueid fails to set if an entry is a conflict entry (Ticket 47735); regression - sub-type length in attribute type was mistakenly subtracted.

* Tue Mar 11 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-23
- Resolves: bug 1074850 - EMBARGOED CVE-2014-0132 389-ds-base: 389-ds: flaw in parsing authzid can lead to privilege escalation [rhel-7.0] (Ticket 47739 - directory server is insecurely misinterpreting authzid on a SASL/GSSAPI bind) (Added 0095-Ticket-47739-directory-server-is-insecurely-misinter.patch)

  Tue Mar 11 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-23
- release 1.3.1.6-22
- Resolves: bug 1074850 - EMBARGOED CVE-2014-0132 389-ds-base: 389-ds: flaw in parsing authzid can lead to privilege escalation [rhel-7.0] (Ticket 47739 - directory server is insecurely misinterpreting authzid on a SASL/GSSAPI bind)

* Mon Mar 10 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-22
- release 1.3.1.6-22
- Resolves: bug 1074084 - e_uniqueid fails to set if an entry is a conflict entry (Ticket 47735)

* Tue Feb 25 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-21
- release 1.3.1.6-21
- Resolves: bug 918694 - Fix covscan defect FORWARD_NULL (Ticket 408)
- Resolves: bug 918717 - Fix covscan defect COMPILER WARNINGS (Ticket 571)

* Tue Feb 25 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-20
- release 1.3.1.6-20
- Resolves: bug 1065242 - 389-ds-base, conflict occurs at yum installation if multilib_policy=all. (Ticket 47709)

* Tue Feb 18 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-19
- release 1.3.1.6-19
- Resolves: bug 1065971 - Enrolling a host into IdM/IPA always takes two attempts (Ticket 47704)

* Mon Feb  3 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-18
- release 1.3.1.6-18
- Resolves: bug 838656 - logconv.pl tool removes the access logs contents if "-M" is not correctly used (Ticket 471)
- Resolves: bug 922538 - improve dbgen rdn generation, output (Ticket 47374)
- Resolves: bug 970750 - flush.pl is not included in perl5 (Ticket 47374)
- Resolves: bug 1013898 - Fix various issues with logconv.pl (Ticket 471)

* Wed Jan 29 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-17
- release 1.3.1.6-17
- Resolves: bug 853106 - Deleting attribute present in nsslapd-allowed-to-delete-attrs returns Operations error (Ticket 443)
- Resolves: bug 1049525 - Server hangs in cos_cache when adding a user entry (Ticket 47649)
    
* Wed Jan 29 2014 Daniel Mach <dmach@redhat.com> - 1.3.1.6-16
- Mass rebuild 2014-01-24

* Tue Jan 21 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-15
- release 1.3.1.6-15
- Resolves: bug 918702 -  better error message when cache overflows (Ticket 342)
- Resolves: bug 1009679 - replication stops with excessive clock skew (Ticket 47516)
- Resolves: bug 1042855 - Unable to delete protocol timeout attribute (Ticket 47620)
- Resolves: bug 918694 - Fix crash when disabling/enabling the setting (Ticket 408)
- Resolves: bug 853355 - config_set_allowed_to_delete_attrs: Valgrind reports Invalid read (Ticket 47660)

* Wed Jan  8 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-14
- release 1.3.1.6-14
- Resolves: bug 853355 - Possible to add invalid attribute to nsslapd-allowed-to-delete-attrs (Ticket 447) 
- Resolves: bug 1034739 - Impossible to configure nsslapd-allowed-sasl-mechanisms (Ticket 47613)
- Resolves: bug 1038639 - 389-ds rejects nsds5ReplicaProtocolTimeout attribut; Fix logically dead code; Fix dereferenced NULL pointer in agmtlist_modify_callback(); Fix missing left brackete (Ticket 47620)
- Resolves: bug 1042855 - nsds5ReplicaProtocolTimeout attribute is not validated when added to replication agreement; Config value validation improvement (Ticket 47620)
- Resolves: bug 918717 - server does not accept 0 length LDAP Control sequence (Ticket 571)
- Resolves: bug 1034902 - replica init/bulk import errors should be more verbose (Ticket 47606)
- Resolves: bug 1044219 - fix memleak caused by 47347 (Ticket 47623)
- Resolves: bug 1049522 - Crash after replica is installed; Fix cherry-pick error for 1.3.2 and 1.3.1 (Ticket 47620)
- Resolves: bug 1049568 - changelog iteration should ignore cleaned rids when getting the minCSN (Ticket 47627) 

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.3.1.6-13
- Mass rebuild 2013-12-27

* Tue Dec 10 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-12
- release 1.3.1.6-12
- Resolves: bug 1038639 - 389-ds rejects nsds5ReplicaProtocolTimeout attribute (Ticket 47620)
- Resolves: bug 1034898 - automember plugin task memory leaks (Ticket 47592)
- Resolves: bug 1034451 - Possible to specify invalid SASL mechanism in nsslapd-allowed-sasl-mechanisms (Ticket 47614)
- Resolves: bug 1032318 - entries with empty objectclass attribute value can be hidden (Ticket 47591)
- Resolves: bug 1032316 - attrcrypt fails to find unlocked key (Ticket 47596)
- Resolves: bug 1031227 - Reduce lock scope in retro changelog plug-in (Ticket 47599)
- Resolves: bug 1031226 - Convert ldbm_back_seq code to be transaction aware (Ticket 47598)
- Resolves: bug 1031225 - Convert retro changelog plug-in to betxn (Ticket 47597)
- Resolves: bug 1031223 - hard coded limit of 64 masters in agreement and changelog code (Ticket 47587)
- Resolves: bug 1034739 - Impossible to configure nsslapd-allowed-sasl-mechanisms (Ticket 47613)
- Resolves: bug 1035824 - Automember betxnpreoperation - transaction not aborted when group entry does not exist (Ticket 47622)

* Thu Nov 21 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.6-11
- Resolves: bug 1024979 - CVE-2013-4485 389-ds-base: DoS due to improper handling of ger attr searches

* Tue Nov 12 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.6-10
- release 1.3.1.6-10
- Resolves: bug 1018893 DS91: ns-slapd stuck in DS_Sleep
-     had to revert earlier change - does not work and breaks ipa

* Tue Nov 12 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-9
- release 1.3.1.6-9
- Resolves: bug 1028440 - Winsync replica initialization and incremental updates from DS to AD fails on RHEL
- Resolves: bug 1027502 - Replication Failures related to skipped entries due to cleaned rids
- Resolves: bug 1027047 - Winsync plugin segfault during incremental backoff

* Wed Nov  6 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-8
- release 1.3.1.6-8
- Resolves: bug 971111 - DNA plugin failed to fetch replication agreement 
- Resolves: bug 1026931 - 1.2.11.29 crash when removing entries from cache

* Mon Oct 21 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.6-7
- Resolves: bug 1018893 DS91: ns-slapd stuck in DS_Sleep
- Resolves: bug 1018914 fixup memberof task does not work: task entry not added 

* Fri Oct 11 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.6-6
- Resolves: bug 1013900 - logconv: some stats do not work across server restarts
-  previous patch introduced regressions
-  fixed by c2eced0 ticket #47550 and e2a880b Ticket #47550 and 8b10f83 Ticket #47551
- Resolves: bug 1008610 - tmpfiles.d references /var/lock when they should reference /run/lock
-  previous patch not complete, fixed by a11be5c Ticket 47513
- Resolves: bug 1016749 - DS crashes when "cn=Directory Manager" is changing it's password
-  cherry picked upstream f786600 Ticket 47329 and b67e230 Coverity Fixes
- Resolves: bug 1015252 locale "nl" not supported by collation plugin
- Resolves: bug 1016317 Need to update supported locales
- Resolves: bug 1016722 memory leak in range searches

* Tue Oct  1 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.6-5
- Resolves: bug 1013896 - logconv.pl - Use of comma-less variable list is deprecated
- Resolves: bug 1008256 - backend txn plugin fixup tasks should be done in a txn
- Resolves: bug 1013738 - CLEANALLRUV doesnt run across all replicas
- Resolves: bug 1011220 - PassSync removes User must change password flag on the Windows side
- Resolves: bug 1008610 - tmpfiles.d references /var/lock when they should reference /run/lock
- Resolves: bug 1012125 - Set up replcation/agreement before initializing the sub suffix, the sub suffix is not found by ldapsearch
- Resolves: bug 1013063 - RUV tombstone search with scope "one" doesn`t work
- Resolves: bug 1013893 - Indexed search are logged with 'notes=U' in the access logs
- Resolves: bug 1013894 - improve logconv.pl performance with large access logs
- Resolves: bug 1013898 - Fix various issues with logconv.pl
- Resolves: bug 1013897 - logconv.pl uses /var/tmp for BDB temp files
- Resolves: bug 1013900 - logconv: some stats do not work across server restarts
- Resolves: bug 1014354 - Coverity fixes - 12023, 12024, and 12025

* Fri Sep 13 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-4
- bump version to 1.3.1.6-4
- Resolves Bug 1007988 - Under specific values of nsDS5ReplicaName, replication may get broken or updates missing (Ticket 47489)
- Resolves Bug 853931 - Allow macro aci keywords to be case-insensitive (Ticket 449)
- Resolves Bug 1006563 - automember rebuild task not working as expected (Ticket 47507)

* Fri Sep  6 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.6-3
- Ticket #47455 - valgrind - value mem leaks, uninit mem usage
- Ticket 47500 - start-dirsrv/restart-dirsrv/stop-disrv do not register with systemd correctly

* Mon Aug 26 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-2
- bump version to 1.3.1.6-2
- Resolves Bug 1000633 - ns-slapd crash due to bogus DN
- Ticket #47488 - Users from AD sub OU does not sync to IPA

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

* Tue Jul 30 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.5-1
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
- Ticket 47435 - Very large entryusn values after enabling the USN plugin and the lastusn value is negat
- Ticket 47424 - Replication problem with add-delete requests on single-valued attributes
- Ticket 47367 - (phase 2) ldapdelete returns non-leaf entry error while trying to remove a leaf entry
- Ticket 47367 - (phase 1) ldapdelete returns non-leaf entry error while trying to remove a leaf entry
- Ticket 47421 - memory leaks in set_krb5_creds
- Ticket 346 - version 4 Slow ldapmodify operation time for large quantities of multi-valued attribute v
- Ticket 47369  version2 - provide default syntax plugin
- Ticket 47427 - Overflow in nsslapd-disk-monitoring-threshold
- Ticket 47339 - RHDS denies MODRDN access if ACI list contains any DENY rule
- Ticket 47427 - Overflow in nsslapd-disk-monitoring-threshold
- Ticket 47428 - Memory leak in 389-ds-base 1.2.11.15
- Ticket 47392 - ldbm errors when adding/modifying/deleting entries
- Ticket 47385 - Disk Monitoring is not triggered as expected.
- Ticket 47410 - changelog db deadlocks with DNA and replication

* Fri Jul 19 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.3-1
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

* Fri Jul 12 2013 Jan Safranek <jsafrane@redhat.com> - 1.3.1.2-2
- Rebuilt for new net-snmp

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
Ticket #28 	MOD operations with chained delete/add get back error 53 on backend config
Ticket #173 	ds-logpipe.py script's man page and script help should be updated for -t option.
Ticket #196 	RFE: Interpret IPV6 addresses for ACIs, replication, and chaining 
Ticket #218 	RFE - Make RIP working with Replicated Entries 
Ticket #328 	make sure all internal search filters are properly escaped 
Ticket #329 	389-admin build fails on F-18 with new apache 	
Ticket #344 	deadlock in replica_write_ruv
Ticket #351 	use betxn plugins by default
Ticket #352 	make cos, roles, views betxn aware 
Ticket #356 	logconv.pl - RFE - track bind info
Ticket #365 	Audit log - clear text password in user changes 
Ticket #370 	Opening merge qualifier CoS entry using RHDS console changes the entry. 
Ticket #372 	Setting nsslapd-listenhost or nsslapd-securelistenhost breaks ACI processing 	
Ticket #386 	Overconsumption of memory with large cachememsize and heavy use of ldapmodify 	
Ticket #402 	unhashedTicket #userTicket #password in entry extension 	
Ticket #408 	Create a normalized dn cache 	
Ticket #453 	db2index with -tattrname:type,type fails 	
Ticket #461 	fix build problem with mozldap c sdk 	
Ticket #462 	add test for include file mntent.h 	
Ticket #463 	different parameters of getmntent in Solaris

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
- Resolves: bug 656541 - use %ghost on files in /var/lock

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
- added template-initconfig to %files
- %posttrans now runs update to update the server instances
- servers are shutdown, then restarted if running before install
- scriptlets mostly use lua now to pass data among scriptlet phases

* Tue Sep 01 2009 Caolán McNamara <caolanm@redhat.com> - 1.2.2-2
- rebuild with new openssl to fix dependencies

* Tue Aug 25 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.2-1
- backed out - added template-initconfig to %files - this change is for the next major release
- bump version to 1.2.2
- fix reopened 509472 db2index all does not reindex all the db backends correctly
- fix 518520 -  pre hashed salted passwords do not work
- see https://bugzilla.redhat.com/show_bug.cgi?id=518519 for the list of
- bugs fixed in 1.2.2

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.1-5
- rebuilt with new openssl

* Wed Aug 19 2009 Noriko Hosoi <nhosoi@redhat.com> - 1.2.1-4
- added template-initconfig to %files

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
