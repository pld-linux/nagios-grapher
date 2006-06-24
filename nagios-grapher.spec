#TODO
# -file in BUILD/.../{contrib,doc,tools}
# - read INSTALL: deps, 
# - send directory layout for PLD to author
# - bconds
# - remowe/subpackage *.c contrib files
Summary:	Plugins for Nagios to integration with RRDTool
Summary(pl):	Wtyczka dla Nagiosa integruj±ca z RRDTool
Name:		nagios-grapher
Version:	1.6
Release:	0.6
License:	GPL
Group:		Applications/System
Source0:	NagiosGrapher-%{version}-rc1.tar.bz2
# Source0-md5:	fdcc43b490f5d3f66d42e4305c61fdbb
Patch0:		%{name}-install.patch
Patch1:		%{name}-install_init.patch
Patch2:		%{name}-init.patch
Patch3:		%{name}-dirlayout.patch
URL:		http://tinyurl.com/ad67c
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	ImageMagick-perl
Requires:	nagios-cgi
Requires:	perl-GD
Requires:	perl-XML-Simple
Requires:	perl-rrdtool
Requires:	perl-Time-HiRes
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

%description -l pl
NagiosGrapher gromadzi wyj¶cie z wtyczek Nagiosa i generuje wykresy.

- pobieranie warto¶ci z Nagiosa bez ³atania (np. poprzez
  "process-service-perfdata")
- wykresy w czasie rzeczywistym (maksymalne opó¼nienie 5 minut)
- rozpoznawanie nowych hostów/us³ug i automatyczne rysowanie ich
- automatyczne czyszczenie i wyci±ganie zapisanych warto¶ci
- bardzo lekki backend - nie wymagaj±cy systemów baz danych 
- ³atwy w instalacji

%prep
%setup -q -n NagiosGrapher-%{version}-rc1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure \
	--with-web-user=http \
	--with-web-group=http \
	--with-nagios-user=nagios \
	--with-nagios-group=nagios \
	--with-ng-interface=network \
	--with-ng-srvext-type=MULTIPLE \
	--with-ng-loglevel=255 \
	--with-layout=PLD \
	--with-ng-interface=pipe

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/etc/nagios/serviceext
install -d $RPM_BUILD_ROOT%{_var}/log/nagios

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT/etc/rc.d/init.d/nagios_grapher
install contrib/nagios_grapher.redhat	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(754,root,root) /etc/rc.d/init.d/%{name}
#%%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,nagios) %{_sysconfdir}/nagios/ngraph.d/*
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,nagios) %{_sysconfdir}/nagios/*.ncfg
%dir %{_sysconfdir}/nagios/serviceext
#%%config(noreplace) %verify(not md5 mtime size) %attr(640,root,nagios) %{_sysconfdir}/nagios/serviceext/*
%dir %{_plugindir}
%attr(755,root,root) %{_plugindir}/*
%attr(755,root,root) %{_libdir}/nagios/cgi/*
%attr(755,root,root) %{perl_vendorlib}/*
%{_datadir}/nagios/images/*
%config(noreplace) %verify(not md5 mtime size) %attr(660,root,nagios) %{_var}/log/nagios/ngraph.log
