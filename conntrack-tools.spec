#
# Conditional build:
%bcond_without	systemd		# systemd integration
#
Summary:	The userspace connection tracking table administration program
Summary(pl.UTF-8):	Program przestrzeni użytkownika do zarządzania tablicą śledzenia połączeń
Name:		conntrack-tools
Version:	1.4.5
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	https://netfilter.org/projects/conntrack-tools/files/%{name}-%{version}.tar.bz2
# Source0-md5:	9356a0cd4df81a597ac26d87ccfebac4
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.conf
URL:		http://conntrack-tools.netfilter.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.6
BuildRequires:	bison
BuildRequires:	flex >= 2.5.33
BuildRequires:	libmnl-devel >= 1.0.3
BuildRequires:	libnetfilter_conntrack-devel >= 1.0.7
BuildRequires:	libnetfilter_cthelper-devel >= 1.0.0
BuildRequires:	libnetfilter_cttimeout-devel >= 1.0.0
BuildRequires:	libnetfilter_queue-devel >= 1.0.2
BuildRequires:	libnfnetlink-devel >= 1.0.1
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.228
%{?with_systemd:BuildRequires:	systemd-devel >= 1:227}
Requires(post,preun):	/sbin/chkconfig
Requires:	libmnl >= 1.0.3
Requires:	libnetfilter_conntrack >= 1.0.7
Requires:	libnetfilter_cthelper >= 1.0.0
Requires:	libnetfilter_cttimeout >= 1.0.0
Requires:	libnetfilter_queue >= 1.0.2
Requires:	libnfnetlink >= 1.0.1
%{?with_systemd:Requires:	systemd-libs >= 1:227}
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

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/conntrackd
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/conntrackd
install -D %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/conntrackd/conntrackd.conf

# dlopened modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/conntrack-tools/*.la

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
%doc AUTHORS TODO doc/helper doc/stats doc/sync
%attr(755,root,root) %{_sbindir}/conntrack
%attr(755,root,root) %{_sbindir}/conntrackd
%attr(755,root,root) %{_sbindir}/nfct
%dir %{_libdir}/conntrack-tools
%attr(755,root,root) %{_libdir}/conntrack-tools/ct_helper_amanda.so
%attr(755,root,root) %{_libdir}/conntrack-tools/ct_helper_dhcpv6.so
%attr(755,root,root) %{_libdir}/conntrack-tools/ct_helper_ftp.so
%attr(755,root,root) %{_libdir}/conntrack-tools/ct_helper_mdns.so
%attr(755,root,root) %{_libdir}/conntrack-tools/ct_helper_rpc.so
%attr(755,root,root) %{_libdir}/conntrack-tools/ct_helper_sane.so
%attr(755,root,root) %{_libdir}/conntrack-tools/ct_helper_ssdp.so
%attr(755,root,root) %{_libdir}/conntrack-tools/ct_helper_tftp.so
%attr(755,root,root) %{_libdir}/conntrack-tools/ct_helper_tns.so
%dir %{_sysconfdir}/conntrackd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conntrackd/conntrackd.conf
%attr(754,root,root) /etc/rc.d/init.d/conntrackd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/conntrackd
%{_mandir}/man5/conntrackd.conf.5*
%{_mandir}/man8/conntrack.8*
%{_mandir}/man8/conntrackd.8*
%{_mandir}/man8/nfct.8*
