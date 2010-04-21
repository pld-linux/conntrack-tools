Summary:	The userspace connection tracking table administration program
Summary(pl.UTF-8):	Program przestrzeni użytkownika do zarządzania tablicą śledzenia połączeń
Name:		conntrack-tools
Version:	0.9.14
Release:	2
License:	GPL v2
Group:		Applications/Networking
Source0:	http://www.netfilter.org/projects/conntrack-tools/files/%{name}-%{version}.tar.bz2
# Source0-md5:	7e9344fe85bb68bcf65c35034add6655
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.conf
Patch0:		%{name}-limits.patch
URL:		http://people.netfilter.org/pablo/conntrack-tools/
BuildRequires:	autoconf
BuildRequires:	automake >= 1.6
BuildRequires:	bison
BuildRequires:	flex >= 2.5.33
BuildRequires:	libnetfilter_conntrack-devel >= 0.0.101
BuildRequires:	libnfnetlink-devel >= 1.0.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	libnetfilter_conntrack >= 0.0.101
Requires:	libnfnetlink >= 1.0.0
Obsoletes:	conntrack
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

%description -l pl.UTF-8
conntrack-tools to zbiór narzędzi przeznaczonych dla administratorów
systemów. Są to conntrack (interfejs przestrzeni użytkownika
obsługiwany z linii poleceń) i conntrackd (demon przestrzeni
użytkownika). Narzędzie conntrack udostępnia pełny interfejs mający za
zadanie zastąpić stary interfejs /proc/net/ip_conntrack. Przy użyciu
conntracka można oglądać i zarządzać z przestrzeni użytkownika tablicą
stanów śledzienia połączeń w jądrze. Z drugiej strony conntrackd
pokrywa specyficzne aspekty firewalli stanowych udostępniając
scenariusze wysokiej dostępności; może także służyć do zbierania
statystyk.

%prep
%setup -q
%patch0 -p1
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
%doc AUTHORS TODO
%attr(755,root,root) %{_sbindir}/conntrack
%attr(755,root,root) %{_sbindir}/conntrackd
%{_mandir}/man8/conntrack.8*
%{_mandir}/man8/conntrackd.8*
%attr(754,root,root) /etc/rc.d/init.d/conntrackd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conntrackd/conntrackd.conf
%dir %{_sysconfdir}/conntrackd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/conntrackd
