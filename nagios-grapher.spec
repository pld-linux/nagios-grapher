# TODO
# - path for rrd font from config.layout (patch for configure.ac and ngraph.ncfg.in)
# - bconds for network/pipe
# - service nagios-grapher does not support chkconfig
# - logrotate config
# - !! patch for collect2.pl - user,group,permision for files/dirs
#	defined in ngraph.ncfg (look %files section)
# - !!	patch for lib/NagiosGrapher/Hooks/SrvExtWriteHostextInfo.pm line 94

%define		_rc	rc2
%define		_rel	0.1
%include	/usr/lib/rpm/macros.perl
Summary:	Plugins for Nagios to integration with RRDTool
Summary(pl.UTF-8):   Wtyczka dla Nagiosa integrująca z RRDTool
Name:		nagios-grapher
Version:	1.6.1
Release:	0.%{_rc}.%{_rel}
License:	GPL
Group:		Applications/System
Source0:	NagiosGrapher-%{version}-%{_rc}.tar.bz2
# Source0-md5:	d0a5257203851c168e776f597bfbd56b
Patch0:		%{name}-install.patch
Patch1:		%{name}-install_init.patch
Patch2:		%{name}-init.patch
Patch3:		%{name}-perl_path.patch
Patch4:		%{name}-rrdfont_path.patch
URL:		http://tinyurl.com/ad67c
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	ImageMagick-perl
Requires:	nagios-cgi
Requires:	rc-scripts
Requires:	rrdtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/nagios/grapher

%description
NagiosGrapher collects the output of NagiosPlugins and generates
graphs.

- get values from Nagios without patching (eg. through
  "process-service-perfdata")
- realtime graphing (5 minutes delay at maximum)
- recognizing new hosts/services and automatic graphing of these
- auto pruning and abstracting of stored values
- very slim backend - no need of a database systems rrdtool
- easy to install

%description -l pl.UTF-8
NagiosGrapher gromadzi wyjście z wtyczek Nagiosa i generuje wykresy.

- pobieranie wartości z Nagiosa bez łatania (np. poprzez
  "process-service-perfdata")
- wykresy w czasie rzeczywistym (maksymalne opóźnienie 5 minut)
- rozpoznawanie nowych hostów/usług i automatyczne rysowanie ich
- automatyczne czyszczenie i wyciąganie zapisanych wartości
- bardzo lekki backend - nie wymagający systemów baz danych - rrdtool
- łatwy w instalacji

%prep
%setup -q -n NagiosGrapher-%{version}-%{_rc}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__autoconf}

%configure \
	--with-web-user=http \
	--with-web-group=http \
	--with-nagios-user=nagios \
	--with-nagios-group=nagios-data \
	--with-ng-srvext-type=MULTIPLE \
	--with-ng-loglevel=355 \
	--with-layout=PLD \
	--with-ng-interface=network

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/nagios/{serviceext,hostext}
install -d $RPM_BUILD_ROOT/var/log/nagios
install -d $RPM_BUILD_ROOT/var/lib/nagios/nagios_grapher

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/etc/rc.d/init.d/nagios_grapher
rm -f $RPM_BUILD_ROOT%{_plugindir}/*.c

install contrib/nagios_grapher.redhat	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install contrib/fifo_write/tcp/fifo_write_from_tcp.pl	$RPM_BUILD_ROOT%{_plugindir}/
install contrib/fifo_write/udpsend.pl       $RPM_BUILD_ROOT%{_plugindir}/
install contrib/rrd_commix/*[yl]       $RPM_BUILD_ROOT%{_plugindir}/
cp contrib/rrd_commix/README contrib/rrd_commix/README-rrd_commix

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	if [ ! -f /var/log/nagios/ngraph.log ]; then
		touch /var/log/nagios/ngraph.log
		chown nagios:nagios-data /var/log/nagios/ngraph.log
		chmod 660 /var/log/nagios/ngraph.log
	fi
fi
#/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
#	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README doc contrib/rrd_commix/README-rrd_commix
%attr(754,root,root) /etc/rc.d/init.d/%{name}
#%%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%config(noreplace) %verify(not md5 mtime size) %attr(640,nagios,nagios-data) %{_sysconfdir}/nagios/ngraph.d/*
%config(noreplace) %verify(not md5 mtime size) %attr(640,nagios,nagios-data) %{_sysconfdir}/nagios/*.ncfg
%dir  %attr(775,nagios,nagios-data) %{_sysconfdir}/nagios/serviceext
%dir  %attr(775,nagios,nagios-data) %{_sysconfdir}/nagios/hostext
#%%config(noreplace) %verify(not md5 mtime size) %attr(640,nagios,nagios-data) %{_sysconfdir}/nagios/serviceext/*
%dir %{_plugindir}
%attr(755,root,root) %{_plugindir}/*
%attr(755,root,root) %{_libdir}/nagios/cgi/*
%attr(755,root,root) %{perl_vendorlib}/*
%{_datadir}/nagios/images/*
%dir %attr(755,nagios,nagios-data) /var/lib/nagios/nagios_grapher
%ghost /var/log/nagios/ngraph.log
