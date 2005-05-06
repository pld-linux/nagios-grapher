Summary:	Plugins for Nagios to integrations with RRDTool
Summary(pl):	Wtyczka dla Nagiosa integrująca z RRDTool
Name:		nagios-grapher
Version:	1.0a1
Release:	0.1
License:	GPL
Group: 		Applications/System
Source0:	nagios_grapher-%{version}.tar.bz2
# Source0-md5:	ebde01f5ec38925b3a6ad6c6b3b5f8c3
URL:		http://www.nagiosexchange.org/Charts.42.0.html?&tx_netnagext_pi1[p_view]=195	
Requires:	nagios
Requires:	nagios-cgi
Requires:	rrdtool

BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_plugindir	%{_libdir}/nagios/grapher
%description
This plugin allow you to 

%description -l pl
Ta wtyczka pozwala na 

%prep
%setup -q -n nagios_grapher-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_plugindir},%{_datadir}/nagios/images,%{_sysconfdir}/rc.d/init.d,%{_libdir}/nagios/cgi/,%{_sysconfdir}/nagios}

install collect2.pl	$RPM_BUILD_ROOT%{_plugindir}/collect2.pl
install dot.png		$RPM_BUILD_ROOT%{_datadir}/nagios/images/dot.png
install fifo_write.pl	$RPM_BUILD_ROOT%{_plugindir}/fifo_write.pl
install graph.png	$RPM_BUILD_ROOT%{_datadir}/nagios/images/graph.png
install graphs.cgi	$RPM_BUILD_ROOT%{_libdir}/nagios/cgi/graphs.cgi
install nagios_grapher	$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/nagios_grapher
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
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/nagios_grapher
%attr(755,root,root) %{_libdir}/nagios/cgi/*
%{_datadir}/nagios/images/*
