# TODO
# - logrotate config
# - !! patch for collect2.pl - user,group,permision for files/dirs
#	defined in ngraph.ncfg (look %files section)
# - !!	patch for lib/NagiosGrapher/Hooks/SrvExtWriteHostextInfo.pm line 94

%define		subver	rc5
%define		subver2	0.5
%define		rel		0.18
Summary:	Plugins for Nagios to integration with RRDTool
Summary(pl.UTF-8):	Wtyczka dla Nagiosa integrująca z RRDTool
Name:		nagios-grapher
Version:	1.6.1
Release:	0.%{subver}.%{rel}
License:	GPL
Group:		Applications/System
Source0:	https://www.nagiosforge.org/gf/download/frsrelease/101/44/NagiosGrapher-%{version}-%{subver}-%{subver2}.tar.gz
# Source0-md5:	4c7ce3a350a5be900bb75c2c5f4ae170
Source1:	%{name}.init
Patch0:		%{name}-install.patch
Patch1:		%{name}-layout.patch
Patch2:		%{name}-init.patch
Patch3:		%{name}-perl_path.patch
Patch4:		%{name}-hashes.patch
URL:		http://www.netways.de/de/produkte/nagios_addons/nagiosgrapher/
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	ImageMagick-coder-png
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
%setup -q -n NagiosGrapher-%{version}-%{subver}-%{subver2}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# pointless to include in %doc
rm -f doc/gpl.txt

for a in cfg/templates/*/*_disabled; do
	mv $a ${a%_disabled}
done

cat <<'EOF' > plugin.cfg
# Enable in nagios.cfg one based on the interface you are using,
# updecho for network, fifo_write for pipe:
#   service_perfdata_command=process-service-perfdata-ngraph-udpecho
#   service_perfdata_command=process-service-perfdata-ngraph-fifo_write

define command {
	command_name process-service-perfdata-ngraph-udpecho
	command_line %{_plugindir}/udpecho
}

define command {
	command_name process-service-perfdata-ngraph-fifo_write
# NOTE: tabs are important here!
	command_line %{_plugindir}/fifo_write /var/lib/nagios/rw/ngraph.pipe '$HOSTNAME$	$SERVICEDESC$	$SERVICEOUTPUT$	$SERVICEPERFDATA$' 3
}
EOF

%build
%{__autoconf}
bash %configure \
	--with-web-user=http \
	--with-web-group=http \
	--with-nagios-user=nagios \
	--with-nagios-group=nagios-data \
	--with-perl-include=%{perl_vendorlib} \
	--with-ng-srvext-type=MULTIPLE \
	--with-ng-loglevel=355 \
	--with-layout=pld_linux \
	--with-ng-interface=network

%{__make} -j1 all-install-messages > README

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/nagios/{serviceext,hostext}
install -d $RPM_BUILD_ROOT/var/log/nagios
install -d $RPM_BUILD_ROOT/var/lib/nagios/nagios_grapher
install -d $RPM_BUILD_ROOT/var/lib/nagios/rrd

%{__make} install -j1 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	NAGIOS_PROC_USER=%(id -un) \
	NAGIOS_PROC_GROUP=%(id -gn) \
	APACHE_GROUP=%(id -gn) \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_plugindir}/*.c

rm -f $RPM_BUILD_ROOT/etc/rc.d/init.d/nagios_grapher
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install contrib/fifo_write/tcp/fifo_write_from_tcp.pl $RPM_BUILD_ROOT%{_plugindir}
install contrib/fifo_write/udpsend.pl $RPM_BUILD_ROOT%{_plugindir}
install contrib/rrd_commix/*[yl] $RPM_BUILD_ROOT%{_plugindir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/nagios/plugins
cp -a plugin.cfg $RPM_BUILD_ROOT%{_sysconfdir}/nagios/plugins/ngraph.cfg
cp contrib/rrd_commix/README contrib/rrd_commix/README-rrd_commix

# copies in %doc
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/nagios/ngraph.d/templates/{standard,extra}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /var/log/nagios/ngraph.log ]; then
	touch /var/log/nagios/ngraph.log
	chown nagios:nagios-data /var/log/nagios/ngraph.log
	chmod 660 /var/log/nagios/ngraph.log
fi
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README doc/* contrib/rrd_commix/README-rrd_commix cfg/templates
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%dir %{_sysconfdir}/nagios/ngraph.d
%dir %{_sysconfdir}/nagios/ngraph.d/templates
%dir %{_sysconfdir}/nagios/ngraph.d/templates/extra
%dir %{_sysconfdir}/nagios/ngraph.d/templates/standard

%config(noreplace) %verify(not md5 mtime size) %attr(640,root,nagios) %{_sysconfdir}/nagios/ngraph.d/nmgraph.ncfg
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,nagios) %{_sysconfdir}/nagios/ngraph.ncfg
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,nagios) %{_sysconfdir}/nagios/plugins/ngraph.cfg
%dir %{_plugindir}
%attr(755,root,root) %{_plugindir}/*
%attr(755,root,root) %{_libdir}/nagios/cgi/*
%{_datadir}/nagios/images/*

%dir %attr(775,root,nagios) /var/lib/nagios/nagios_grapher
%dir %attr(775,root,nagios) /var/lib/nagios/rrd
%ghost /var/log/nagios/ngraph.log
