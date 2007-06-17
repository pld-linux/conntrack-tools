Summary:	The userspace connection tracking table administration program
Name:		conntrack-tools
Version:	0.9.3
Release:	0.1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://www.netfilter.org/projects/conntrack-tools/files/%{name}-%{version}.tar.bz2
# Source0-md5:	b8a0297c538bd1fb708b2c9ed3f31676
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.conf
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
find -name .svn -print0 | xargs -0 rm -rf

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
CFLAGS="%{rpmcflags} -D__KERNEL_STRICT_NAMES=1"
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
        DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/conntrackd
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/conntrackd
install -D %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/conntrackd/conntrackd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add conntrackd
%service conntrackd restart

%preun
if [ "$1" = "0" ]; then
	%service -q conntrackd stop
	/sbin/chkconfig --del conntrackd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog TODO examples
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/ct_proto*.so
%{_mandir}/man8/*
%attr(754,root,root) /etc/rc.d/init.d/conntrackd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conntrackd/conntrackd.conf
%dir %{_sysconfdir}/conntrackd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/conntrackd
