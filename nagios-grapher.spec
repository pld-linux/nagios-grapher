#TODO
# -file in BUILD/.../{contrib,doc,tools}
# - noarch?
Summary:	Plugins for Nagios to integration with RRDTool
Summary(pl):	Wtyczka dla Nagiosa integruj±ca z RRDTool
Name:		nagios-grapher
Version:	1.6
Release:	0.3
License:	GPL
Group:		Applications/System
Source0:	NagiosGrapher-%{version}-rc1.tar.bz2
# Source0-md5:	fdcc43b490f5d3f66d42e4305c61fdbb
Patch0:		%{name}-install.patch
Patch1:		%{name}-install_init.patch
Patch2:		%{name}-init.patch
URL:		http://tinyurl.com/ad67c
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	nagios-cgi
Requires:	rrdtool
Requires:	perl-XML-Simple
Requires:	perl-rrdtool
Requires:	perl-GD
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/nagios/grapher

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
%setup -q -n NagiosGrapher-%{version}-rc1
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
%configure \
	--with-web-user=http \
	--with-web-group=http \
	--with-nagios-user=nagios \
	--with-nagios-group=nagios \
	--with-ng-interface=network \
	--with-ng-srvext-type=MULTIPLE \
	--with-ng-loglevel=INT 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d/
install -d $RPM_BUILD_ROOT/%{_var}/log

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	NAGIOS_IMAGES=%{_datadir}/nagios/images/ \
	NAGIOS_IMAGES_LOGOS=%{_datadir}/nagios/images/ \
	NG_CONFIG=%{_sysconfdir}/nagios/ \
	NG_CONFIG_SUB=%{_sysconfdir}/nagios/ \
	NG_CONFIG_CGI=%{_sysconfdir}/nagios/ \
	NAGIOS_FOLDER_CGI=%{_datadir}/nagios/cgi \
	PERL_INC=%{perl_vendorlib} \
	NAGIOS_CONTRIBUTION=%{_plugindir} \
	NG_LOGFILE=%{_var}/log \
	
#NG_SRVEXT_DIR=/dir1 \
#NG_RRD=/dir \
#NAGIOS_BIN=/dir
#NG_SRVEXT_DIR/dir
rm $RPM_BUILD_ROOT/etc/rc.d/init.d/nagios_grapher
install contrib/nagios_grapher.redhat	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
#ln -s %{_plugindir}/NagiosGrapher.pm $RPM_BUILD_ROOT%{_libdir}/nagios/cgi/NagiosGrapher.pm

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
#%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nagios/extra/*.ncfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nagios/standard/*.ncfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nagios/*.ncfg
%dir %{_plugindir}
%attr(755,root,root) %{_plugindir}/*
%attr(755,root,root) %{_datadir}/nagios/cgi/*
%attr(755,root,root) %{perl_vendorlib}/*
%{_datadir}/nagios/images/*
