Summary:	Plugins for Nagios to integration with RRDTool
Summary(pl):	Wtyczka dla Nagiosa integruj±ca z RRDTool
Name:		nagios-grapher
Version:	1.0a1
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	nagios_grapher-%{version}.tar.bz2
# Source0-md5:	ebde01f5ec38925b3a6ad6c6b3b5f8c3
URL:		http://tinyurl.com/ad67c
Requires:	nagios-cgi
Requires:	rrdtool
Requires:	perl-XML-Simple
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildArch:      noarch

%define	_plugindir	%{_libdir}/nagios/grapher

%description
NagiosGrapher collects the output of NagiosPlugins and generates
graphs.

- get values from nagios without patching (eg. through
  "process-service-perfdata")
- realtime graphing (5 minutes delay at maximum)
- recognizing new hosts/services and automatic graphing of these
- auto pruning and abstracting of stored values
- very slim backend - no need of a database systems rrdtool
- easy to install 

%description -l pl
NagiosGrapher gromadzi wyj¶cie z wtyczek Nagiosa i generuje wykresy.

- pobieranie warto¶ci z nagiosa bez ³atania (np. poprzez
  "process-service-perfdata")
- wykresy w czasie rzeczywistym (maksymalne opó¼nienie 5 minut)
- rozpoznawanie nowych hostów/us³ug i automatyczne rysowanie ich
- automatyczne czyszczenie i wyci±ganie zapisanych warto¶ci
- bardzo lekki backend - nie wymagaj±cy systemów baz danych 
- ³atwy w instalacji

%prep
%setup -q -n nagios_grapher-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_plugindir},%{_datadir}/nagios/images,/etc/rc.d/init.d,%{_libdir}/nagios/cgi/,%{_sysconfdir}/nagios}

install collect2.pl	$RPM_BUILD_ROOT%{_plugindir}/collect2.pl
install dot.png		$RPM_BUILD_ROOT%{_datadir}/nagios/images/dot.png
install fifo_write.pl	$RPM_BUILD_ROOT%{_plugindir}/fifo_write.pl
install graph.png	$RPM_BUILD_ROOT%{_datadir}/nagios/images/graph.png
install graphs.cgi	$RPM_BUILD_ROOT%{_libdir}/nagios/cgi/graphs.cgi
install nagios_grapher	$RPM_BUILD_ROOT/etc/rc.d/init.d/nagios_grapher
install NagiosGrapher.pm $RPM_BUILD_ROOT%{_plugindir}/NagiosGrapher.pm
install ngraph.cfg	$RPM_BUILD_ROOT%{_sysconfdir}/nagios/ngraph.cfg
install rrd2-graph.cgi	$RPM_BUILD_ROOT%{_libdir}/nagios/cgi/rrd2-graph.cgi

cd $RPM_BUILD_ROOT%{_libdir}/nagios/cgi
ln -sf	%{_plugindir}/NagiosGrapher.pm NagiosGrapher.pm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
#%doc
%attr(755,root,root) %{_plugindir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nagios/ngraph.cfg
%attr(754,root,root) /etc/rc.d/init.d/nagios_grapher
%attr(755,root,root) %{_libdir}/nagios/cgi/*
%{_datadir}/nagios/images/*
