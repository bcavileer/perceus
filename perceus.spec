#
# Copyright (c) 2006-2008, Greg M. Kurtzer, Arthur A. Stevens and
# Infiscale, Inc. All rights reserved
#

%{expand:%%global use_gcc4 %(which gcc4 >/dev/null 2>&1 && echo 1 || echo 0)}
%if %{use_gcc4}
%define set_cc CC=gcc4 CXX=gcc4
%endif

Name: perceus
Summary: Provision Enterprise Resources & Clusters, Enabling Uniform Systems
Version: 1.6.0
Release: 0.2402M
License: GPL
Group: System Environment/Provisioning
Source: %{name}-%{version}.tar.gz
ExclusiveOS: linux
#BuildSuggests: perl-DBI, perl-Unix-Syslog, perl-IO-Interface, perl-Net-ARP
BuildRequires: perl, perl(DBI), perl(Unix::Syslog), perl(IO::Interface), perl(Net::ARP)
BuildRequires: make >= 3.80, autoconf >= 2.59, nasm, openssl-devel, elfutils-libelf-devel
BuildRequires: gettext, /usr/include/uuid/uuid.h
Requires(pre): grep, /usr/sbin/groupadd
Requires: /sbin/chkconfig, /sbin/service, rsync
Requires: perl, perl(DBI), perl(Unix::Syslog), perl(IO::Interface), perl(Net::ARP)
Prefix: %{_prefix}
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

%description
Provision Enterprise Resources & Clusters, Enabling Uniform Systems with
PERCEUS

%package provisiond
Summary: PERCEUS provisiond client (for the nodes)
Group: System Environment/Provisioning

%description provisiond
This is the node client application used to connect and pull commands from
a Perceus master.

%package cgi
Summary: PERCEUS web configuration tool
Group: System Environment/Provisioning
Requires: %{name} = %{version}-%{release}
Requires: httpd

%description cgi
This is the web interface to PERCEUS.

%prep
%setup -q

%build
%{?set_cc:export %{set_cc}}
%configure %{?set_cc}
%{__make} %{?set_cc} %{?mflags}

%install
test "x%{buildroot}" != "x" && rm -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} %{?mflags_install} install
cp -a src/provisiond/provisiond %{buildroot}/%{_sbindir}/

%pre
grep -q "^perceus:" /etc/group || /usr/sbin/groupadd -r perceus || :

%preun
if [ "$1" = 0 ]; then
   /sbin/service perceus stop > /dev/null 2>&1 || :
   /sbin/chkconfig --del perceus >/dev/null 2>&1 || :
fi

%preun provisiond
if [ "$1" = 0 ]; then
   /sbin/service provisiond stop > /dev/null 2>&1 || :
   /sbin/chkconfig --del provisiond >/dev/null 2>&1 || :
fi

%post
/sbin/chkconfig --add perceus >/dev/null 2>&1 || :
/sbin/service perceus condrestart > /dev/null 2>&1 || :

%post provisiond
/sbin/chkconfig --add provisiond >/dev/null 2>&1 || :
/sbin/service provisiond condrestart > /dev/null 2>&1 || :

%post cgi
/sbin/service httpd condrestart > /dev/null 2>&1 || :

%postun cgi
/sbin/service httpd condrestart > /dev/null 2>&1 || :


%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README MODULES docs
%dir /etc/perceus
%config(noreplace) /etc/perceus/perceus.conf
%config(noreplace) /etc/perceus/defaults.conf
%config(noreplace) /etc/sysconfig/perceus
/etc/perceus/Perceus_Include.pm
/etc/perceus/nodescripts
/etc/perceus/vnfs
/etc/bash_completion.d/*
/etc/init.d/perceus
%{_prefix}/lib/perceus
%{_datadir}/perceus
%{_localstatedir}/lib/perceus
%{_sbindir}/perceusd
%{_sbindir}/perceus-init
%{_includedir}/*
%{_libexecdir}/perceus
%{_mandir}/*/*
%{_bindir}/perceus
%{_bindir}/ssh-perceus

%files cgi
%defattr(-,root,root)
%{_datadir}/perceus/cgi
/etc/httpd/conf.d/*
%{_sbindir}/perceus-htpasswd

%files provisiond
%defattr(-,root,root)
/etc/init.d/provisiond
%{_sbindir}/provisiond
%{_sbindir}/ethinfo

%clean
%__rm -rf $RPM_BUILD_ROOT

%changelog
