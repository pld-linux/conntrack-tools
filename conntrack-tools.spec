Summary:	The userspace connection tracking table administration program
Name:		conntrack-tools
Version:	0.9.3
Release:	0.1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://www.netfilter.org/projects/conntrack-tools/files/%{name}-%{version}.tar.bz2
# Source0-md5:	b8a0297c538bd1fb708b2c9ed3f31676
#Source1:	%{name}.init
#Source2:	%{name}.sysconfig
#Source3:	%{name}.conf
URL:		http://people.netfilter.org/pablo/conntrack-tools/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libnetfilter_conntrack-devel >= 0.0.75
BuildRequires:	libnfnetlink-devel >= 0.0.25-1
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The conntrack-tools are a set of tools targeted at system
administrators. They are conntrack, the userspace command line
interface, and conntrackd, the userspace daemon. The tool conntrack
provides a full featured interface that is intended to replace the old
/proc/net/ip_conntrack interface. Using conntrack, you can view and
manage the in-kernel connection tracking state table from userspace.
On the other hand, conntrackd covers the specific aspects of stateful
firewalls to enable highly available scenarios, and can be used as
statistics collector as well.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
        DESTDIR=$RPM_BUILD_ROOT

#install -D %{SOURCE1}		$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
#install -D %{SOURCE2}		$RPM_BUILD_ROOT/etc/sysconfig/%{name}
#install -D %{SOURCE3}		$RPM_BUILD_ROOT%{_sysconfdir}/

%clean
rm -rf $RPM_BUILD_ROOT

%post
#/sbin/chkconfig --add %{name}
#%service %{name} restart

%preun
#if [ "$1" = "0" ]; then
#	%service -q %{name} stop
#	/sbin/chkconfig --del %{name}
#fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README NEWS TODO
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
#%attr(754,root,root) /etc/rc.d/init.d/%{name}
#%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/
#%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
