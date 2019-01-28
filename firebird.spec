%define		oversion 3.0.4
%define		major 2
%define		pkgversion Firebird-%{version}-0
%define		libfbclient %mklibname fbclient %{major}
%define		libfbclient_devel %mklibname fbclient -d

%define __noautoreq '/usr/bin/sh'

Summary:	Firebird SQL database management system
Name:		firebird
Version:	%{oversion}.33054
Release:	3
Group:		Databases
License:	MPLv1.1-like
URL:		http://www.firebirdsql.org/
Source0:	https://github.com/FirebirdSQL/firebird/releases/download/R3_0_4/%{pkgversion}.tar.bz2
Source1:	firebird-logrotate
Source2:	README.OMV
Source3:	firebird.conf
Source4:	fb_config

# from OpenSuse
Patch101:	add-pkgconfig-files.patch
Patch103:	Provide-sized-global-delete-operators-when-compiled.patch

# from Debian to be sent upstream
Patch201:	obsolete-syslogd.target.patch
Patch202:	honour-buildflags.patch
Patch203:	no-copy-from-icu.patch
Patch205:	cloop-honour-build-flags.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	tommath-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	icu-devel
BuildRequires:	pkgconfig(libedit)
BuildRequires:	gcc-c++
BuildRequires:	libstdc++-static-devel
BuildRequires:	pkgconfig(atomic_ops)
BuildRequires:	chrpath
BuildRequires:	pkgconfig(zlib)
BuildRequires:	procmail
BuildRequires:	sed

Requires(post):		systemd
Requires(pre):		rpm-helper
Requires(postun):	rpm-helper

Requires:	%{libfbclient} = %{EVRD}
Requires:	libib-util = %{EVRD}
Requires:	%{name}-utils = %{EVRD}

Obsoletes:	firebird-arch < 3.0
Obsoletes:	firebird-filesystem < 3.0
Obsoletes:	firebird-server-common < 3.0
Obsoletes:	firebird-classic < 3.0
Obsoletes:	firebird-classic-common < 3.0
Obsoletes:	firebird-server-classic < 3.0
Obsoletes:	firebird-server-superserver < 3.0
Obsoletes:	firebird-superclassic < 3.0
Obsoletes:	firebird-superserver < 3.0
Conflicts:	firebird-arch < 3.0
Conflicts:	firebird-filesystem < 3.0
Conflicts:	firebird-server-common < 3.0
Conflicts:	firebird-classic < 3.0
Conflicts:	firebird-classic-common < 3.0
Conflicts:	firebird-server-classic < 3.0
Conflicts:	firebird-server-superserver < 3.0
Conflicts:	firebird-superclassic < 3.0
Conflicts:	firebird-superserver < 3.0

%description
Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.

%files
%{_docdir}/%{name}/IDPLicense.txt
%{_docdir}/%{name}/IPLicense.txt
%{_docdir}/%{name}/README.OMV
%{_bindir}/fbtracemgr
%{_sbindir}/firebird
%{_sbindir}/fbguard
%{_sbindir}/fb_lock_print
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/databases.conf
%config(noreplace) %{_sysconfdir}/%{name}/fbtrace.conf
%config(noreplace) %{_sysconfdir}/%{name}/firebird.conf
%config(noreplace) %{_sysconfdir}/%{name}/plugins.conf
%dir %{_libdir}/%{name}
%dir %{_datadir}/%{name}
%{_libdir}/%{name}/intl
%{_libdir}/%{name}/plugins
%{_libdir}/%{name}/udf
%{_datadir}/%{name}/misc

%dir %attr(0755,%{name},%{name}) %{_localstatedir}/lib/%{name}
%dir %attr(0750,%{name},%{name}) %{_localstatedir}/lib/%{name}/secdb
%dir %attr(0750,%{name},%{name}) %{_localstatedir}/lib/%{name}/data
%dir %attr(0755,%{name},%{name}) %{_localstatedir}/lib/%{name}/system
%attr(0600,%{name},%{name}) %config(noreplace) %{_localstatedir}/lib/%{name}/secdb/security3.fdb
%attr(0644,%{name},%{name}) %{_localstatedir}/lib/%{name}/system/help.fdb
%attr(0644,%{name},%{name}) %{_localstatedir}/lib/%{name}/system/firebird.msg
%attr(0644,root,root) %{_tmpfilesdir}/firebird.conf 
%dir %{_localstatedir}/log/%{name}
%config(noreplace) %attr(0664,%{name},%{name})  %{_localstatedir}/log/%{name}/%{name}.log
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/%{name}

%defattr(0755,root,root,0755)
%{_unitdir}/%{name}-superserver.service

%pre
# Create the firebird user and group if it doesn't exist
%_pre_useradd %{name} %{_localstatedir}/lib/%{name}/data /sbin/nologin 

# Add gds_db to /etc/services if needed
FileName=/etc/services
newLine="gds_db 3050/tcp  # Firebird SQL Database Remote Protocol"
oldLine=`grep "^gds_db" $FileName`
if [ -z "$oldLine" ]; then
 echo $newLine >> $FileName
fi


%post
%tmpfiles_create %{name}
%_post_service %{name}-superserver

%postun
%_postun_userdel %{name}

%preun
%_preun_service %{name}-superserver 

#---------------------------------------------------------------------------

%package devel
Group:		Development/Databases
Requires:	%{name} = %{EVRD}
Summary:	UDF support library for Firebird SQL server

%description devel
This package is needed for development of client applications and user
defined functions (UDF) for Firebird SQL server.

Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.

%files devel
%{_includedir}/*.h
%{_includedir}/%{name}
%{_libdir}/fb_config
%{_sbindir}/fb_config

#---------------------------------------------------------------------------

%package -n libib-util
Group:		System/Libraries
Summary:	Firebird SQL UDF support library

%description -n libib-util
libib_util contains utility functions used by
User-Defined Functions (UDF) for memory management etc.

Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.

%files -n libib-util
%{_libdir}/libib_util.so

#---------------------------------------------------------------------------

%package -n %{libfbclient}
%define old_fbclient %mklibname fbclient 2.5
%define old_fbembed %mklibname fbembed 2.5
Group:		System/Libraries
Summary:	Firebird SQL server client library
Obsoletes:	%{old_fbclient} < %{EVRD}
Obsoletes:	%{old_fbembed} < %{EVRD}
Conflicts:	%{old_fbclient} < %{EVRD}
Conflicts:	%{old_fbembed} < %{EVRD}

%description -n %{libfbclient}
Shared client library for Firebird SQL server.

Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.

%files -n %{libfbclient}
%{_libdir}/libfbclient.so.%{major}
%{_libdir}/libfbclient.so.%{oversion}

#---------------------------------------------------------------------------

%package -n %{libfbclient_devel}
Group:          System/Libraries
Summary:        Development libraries and headers for Firebird SQL server
Requires:       %{name}-devel = %{EVRD}
Requires:       %{libfbclient} = %{EVRD}

%description -n %{libfbclient_devel}
Development files for Firebird SQL server client library.

Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.

%files -n %{libfbclient_devel}
%{_libdir}/libfbclient.so
%{_libdir}/pkgconfig/fbclient.pc

#---------------------------------------------------------------------------

%package doc
Group:		Databases
Requires:	%{name} = %{EVRD}
Summary:	Documentation for Firebird SQL server
BuildArch:      noarch

%description doc
Documentation for Firebird SQL server.

Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.

%files doc
%{_docdir}/%{name}
%exclude %{_docdir}/%{name}/sample
%exclude %{_docdir}/%{name}/IDPLicense.txt
%exclude %{_docdir}/%{name}/IPLicense.txt
%exclude %{_docdir}/%{name}/README.OMV

#---------------------------------------------------------------------------

%package utils
Group:		Databases
Requires:	%{libfbclient} = %{version}-%{release}
Summary:	Firebird SQL user utilities
Obsoletes:	firebird-utils-classic < 3.0
Conflicts:	firebird-utils-classic < 3.0
Obsoletes:	firebird-utils-common < 3.0
Conflicts:	firebird-utils-common < 3.0
Obsoletes:	firebird-utils-superserver < 3.0
Conflicts:	firebird-utils-superserver < 3.0

%description utils
Firebird SQL user utilities.

Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.

%files utils
%{_bindir}/gstat-fb
%{_bindir}/fbsvcmgr
%{_bindir}/gbak
%{_bindir}/gfix
%{_bindir}/gpre
%{_bindir}/gsec
%{_bindir}/isql-fb
%{_bindir}/nbackup
%{_bindir}/qli
%{_bindir}/gsplit

#---------------------------------------------------------------------------

%package examples
Group:		Databases
Requires:	%{name}-doc = %{EVRD}
Summary:	Examples for Firebird SQL server
BuildArch:	noarch

%description examples
Examples for Firebird SQL server.

Firebird is a relational database offering many ANSI SQL standard
features that runs on Linux, Windows, and a variety of Unix platforms.
Firebird offers excellent concurrency, high performance, and powerful
language support for stored procedures and triggers. It has been used
in production systems, under a variety of names, since 1981.

%files examples
%{_docdir}/%{name}/sample
%attr(0660,%{name},%{name}) %{_localstatedir}/lib/%{name}/data/employee.fdb

#---------------------------------------------------------------------------

%prep
%setup -q -n %{pkgversion}
%patch101 -p1
%patch103 -p1
%patch201 -p1
%patch202 -p1
%patch203 -p1
%patch205 -p1

%build
NOCONFIGURE=1 ./autogen.sh
export CFLAGS="%{optflags} -I/usr/include/tommath"
export CXXFLAGS="%{optflags} -fno-delete-null-pointer-checks -I/usr/include/tommath"
%configure2_5x --prefix=%{_prefix} \
  --disable-binreloc \
  --with-system-editline \
  --with-fbbin=%{_bindir} --with-fbsbin=%{_sbindir} \
  --with-fbconf=%{_sysconfdir}/%{name} \
  --with-fblib=%{_libdir} --with-fbinclude=%{_includedir} \
  --with-fbdoc=%{_defaultdocdir}/%{name} \
  --with-fbudf=%{_libdir}/%{name}/udf \
  --with-fbsample=%{_defaultdocdir}/%{name}/sample \
  --with-fbsample-db=%{_localstatedir}/lib/%{name}/data/ \
  --with-fbhelp=%{_localstatedir}/lib/%{name}/system/ \
  --with-fbintl=%{_libdir}/%{name}/intl \
  --with-fbmisc=%{_datadir}/%{name}/misc \
  --with-fbsecure-db=%{_localstatedir}/lib/%{name}/secdb/ \
  --with-fbmsg=%{_localstatedir}/lib/%{name}/system/ \
  --with-fblog=%{_localstatedir}/log/%{name} \
  --with-fbglock=%{_var}/run/%{name} \
  --with-fbplugins=%{_libdir}/%{name}/plugins

# Can't use %%make_build as it seems that sometimes parallel build is broken
make
cd gen
make -f Makefile.install buildRoot
chmod -R u+w buildroot%{_docdir}/%{name}

%install
ls gen
ls gen/buildroot
#chmod u+rw,a+rx gen/buildroot/usr/include/firebird/impl
cp -r gen/buildroot/* %{buildroot}/
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp -v gen/install/misc/*.pc %{buildroot}%{_libdir}/pkgconfig/

cd %{buildroot}
rm -vf .%{_sbindir}/*.sh
mv -v .%{_sbindir}/fb_config .%{_libdir}/
install -p -m 0755 %{SOURCE4} %{buildroot}%{_sbindir}/fb_config
rm -vf .%{_includedir}/perf.h
rm -vf .%{_libdir}/libicu*.so
chmod -R u+w .%{_docdir}/%{name}
rm -vf .%{_datadir}/%{name}/misc/firebird.init.*
rm -vf .%{_datadir}/%{name}/misc/firebird.xinetd
rm -vf .%{_datadir}/%{name}/misc/rc.config.firebird
mv -v .%{_sysconfdir}/%{name}/README .%{_sysconfdir}/%{name}/WhatsNew \
  .%{_docdir}/%{name}/
mv -v .%{_sysconfdir}/%{name}/IDPLicense.txt .%{_docdir}/%{name}/
mv -v .%{_sysconfdir}/%{name}/IPLicense.txt .%{_docdir}/%{name}/
install -p -m 0644 -D %{SOURCE2} .%{_docdir}/%{name}/README.OMV
mv -v .%{_bindir}/gstat .%{_bindir}/gstat-fb
mv -v .%{_bindir}/isql .%{_bindir}/isql-fb

mkdir -p .%{_localstatedir}/log/%{name}
mkdir -p .%{_sysconfdir}/logrotate.d
echo 1 > .%{_localstatedir}/log/%{name}/%{name}.log
sed "s@%{name}.log@%{_localstatedir}/log/%{name}/%{name}.log@g" %{SOURCE1} > .%{_sysconfdir}/logrotate.d/%{name}

mkdir -p .%{_tmpfilesdir}
cp %{SOURCE3} .%{_tmpfilesdir}/

mkdir -p .%{_unitdir}
cp .%{_datadir}/%{name}/misc/%{name}-superserver.service .%{_unitdir}/%{name}-superserver.service
