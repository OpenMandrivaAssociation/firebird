%define Werror_cflags %{nil}

%define	major	2.5.2
%define pkgname Firebird-2.5.2.26540-0
%define somajor	2
%define libfbclient %mklibname fbclient %{somajor}
%define libfbembed %mklibname fbembed %{somajor}

%define fbroot %{_libdir}/%{name}

Summary:	SQL database management system
Name:		firebird
Version:	2.5.2.26540.0
Release:	3
Group:		Databases
License:	IPL
Url:		http://www.firebirdsql.org/
Source0:	http://downloads.sourceforge.net/firebird/%{pkgname}.tar.bz2
Source1:	firebird-logrotate
Source2:	firebird.mdv.releasenote
Source100:	firebird.rpmlintrc

BuildRequires:	bison
BuildRequires:	libtool
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  icu-devel
BuildRequires:  edit-devel
BuildRequires:	gcc-c++
BuildRequires:	libstdc++-static-devel
Requires:	%{name}-arch = %{version}-%{release}
Requires:	grep
Requires:	sed

%description
This is the Firebird SQL Database shared files.

%files
%doc doc/license/IDPL.txt
%doc doc/license/README.license.usage.txt
%doc gen/buildroot-classic%{_defaultdocdir}/%{name}
%doc gen/buildroot-classic%{fbroot}/misc/intl.sql
%doc gen/buildroot-classic%{fbroot}/misc/upgrade
%doc gen/buildroot-classic%{_sysconfdir}/%{name}/README
%doc gen/buildroot-classic%{_sysconfdir}/%{name}/WhatsNew

%package	classic
Summary:	Meta-package for Firebird SQL Classic Database (xinetd based)
Group:		Databases
Provides:	%{name}-arch = %{version}-%{release}
Requires:	%{name}-server-classic = %{version}
Requires:	%{name}-utils-classic = %{version}
Requires:	xinetd
# Yes, we need force this. Otherwise, only direct local access wil be available.
Requires:	%{libfbclient}
Conflicts:	%{name}-superserver
Conflicts:	%{name}-superclassic

%description	classic
This is a meta-package for easy selecting the Classic arch for Firebird 2

%files		classic
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}

%package	superclassic
Summary:	Meta-package for Firebird SQL SuperClassic Database 
Group:		Databases
Provides:	%{name}-arch = %{version}-%{release}
Requires:	%{name}-server-classic = %{version}
Requires:	%{name}-utils-classic = %{version}
# Yes, we need force this. Otherwise, only direct local access wil be available.
Requires:	%{libfbclient}
Requires:	%{libfbembed}
Requires(pre):  rpm-helper
Conflicts:	%{name}-superserver
Conflicts:	%{name}-classic

%description	superclassic
This is a meta-package for easy selecting the SuperClassic arch for Firebird 2

%files		superclassic
%{_initrddir}/%{name}-superclassic

%package	superserver
Summary:	Meta-package for Firebird SQL SuperServer Database (standalone)
Group:		Databases
Provides:	%{name}-arch = %{version}-%{release}
Requires:	%{name}-server-superserver = %{version}
Requires:	%{name}-utils-superserver = %{version}
Conflicts:	%{name}-classic
Conflicts:	%{name}-superclassic

%description	superserver
This is a meta-package for easy selecting the SuperServer arch for Firebird 2

%files		superserver

%package	devel
Summary:	Development Libraries for Firebird SQL Database
Group:		Development/Databases
Requires:	%{libfbclient}
Requires:	%{libfbembed}

%description	devel
Development libraries for firebird.

%files devel
%dir %{_includedir}/%{name}
%{_includedir}/*.h
%{_includedir}/%{name}/*.h
%{_libdir}/libfb*.so
%{_libdir}/libgds.so

%package	utils-classic
Summary:	Client programs for Firebird SQL Database
Group:		Databases
Provides:	%{name}-utils-arch = %{version}-%{release}
Requires:	%{name}-utils-common = %{version}
Conflicts:	%{name}-utils-superserver
Obsoletes:	%{name}-client-embedded <= 2.0

%description	utils-classic
Client access tools for firebird embeded only.

%files		utils-classic
%dir %{fbroot}/bin-classic
%{fbroot}/bin-classic/gbak
%{fbroot}/bin-classic/fbsvcmgr
%{fbroot}/bin-classic/isql
%{fbroot}/bin-classic/qli
%{fbroot}/bin-classic/fbtracemgr

%package	utils-superserver
Summary:	Client programs for Firebird SQL Database
Group:		Databases
Provides:	%{name}-utils-arch = %{version}-%{release}
Requires:	%{name}-utils-common = %{version}
Conflicts:	%{name}-utils-classic

%description	utils-superserver
Client access tools for firebird.

%files		utils-superserver
%dir %{fbroot}/bin-superserver
%{fbroot}/bin-superserver/gbak
%{fbroot}/bin-superserver/fbsvcmgr
%{fbroot}/bin-superserver/isql
%{fbroot}/bin-superserver/qli
%{fbroot}/bin-superserver/fbtracemgr

%package	utils-common
Summary:	Client programs for Firebird SQL Database
Group:		Databases
Requires:	%{name}-utils-arch = %{version}-%{release}

%description	utils-common
Common client access tools for firebird.

%files		utils-common
%doc doc/license/IDPL.txt
%doc doc/license/README.license.usage.txt
%dir %{fbroot}
%ghost %{fbroot}/bin
%{_bindir}/isql-fb
%{_bindir}/gbak
%{_bindir}/fbsvcmgr
%{_bindir}/qli
%{_bindir}/fbtracemgr
%{_localstatedir}/lib/%{name}/system/*.msg
%{_localstatedir}/lib/%{name}/system/help.fdb

%package -n %{libfbclient}
Summary:	Multi-threaded, non-local client libraries for Firebird SQL Database
Group:		System/Libraries

%description -n %{libfbclient}
Multi-threaded, non-local client libraries for Firebird SQL Database

%files -n %{libfbclient}
%{_libdir}/libfbclient.so.*
%{_libdir}/libgds.so.0

%package -n %{libfbembed}
Summary:	Multi-process, local client libraries for Firebird SQL Database
Group:		System/Libraries

%description -n %{libfbembed}
Multi-process, local client libraries for Firebird SQL Database

%files -n %{libfbembed}
%{_libdir}/libfbembed.so.*

%package	server-classic
Summary:	Classic (xinetd) server for Firebird SQL Database
Group:		Databases
Provides:	firebird-server = %{version}-%{release}
Requires:	%{name}-server-common = %{version}
Conflicts:	%{name}-server-superserver
Requires(pre):  %{name}-server-common = %{version}
Requires(pre):  /usr/sbin/groupadd
Requires(pre):  /usr/sbin/useradd
Requires(pre):  rpm-helper

%description	server-classic
This package contains the command line utilities and files common
to classic and superclassic Firebird servers.

%files		server-classic
%dir %{fbroot}/bin-classic
%dir %{fbroot}/plugins-classic
%{_sbindir}/fb_inet_server
%{_sbindir}/fb_smp_server
%{fbroot}/plugins-classic/*
%{fbroot}/bin-classic/gsec
%{fbroot}/bin-classic/gdef
%{fbroot}/bin-classic/gfix
%{fbroot}/bin-classic/gpre
%{fbroot}/bin-classic/gsplit
%{fbroot}/bin-classic/gstat
%{fbroot}/bin-classic/nbackup
%{fbroot}/bin-classic/fb_config

%package	server-superserver
Summary:	Superserver (single process) server for Firebird SQL Database
Group:		Databases
Provides:	firebird-server = %{version}-%{release}
Requires:	%{name}-server-common = %{version}-%{release}
Conflicts:	%{name}-server-classic
Conflicts:	%{name}-server-superclassic
Requires(pre):	%{name}-server-common = %{version}
Requires(pre):	rpm-helper

%description	server-superserver
This is the Superserver (single process) for the Firebird SQL Database.

It does not include any client access tools, nor does it include the
multi-threaded client library.

%files		server-superserver
%dir %{fbroot}/bin-superserver
%dir %{fbroot}/plugins-superserver
%{_initrddir}/%{name}-superserver
%{fbroot}/bin-superserver/gsec
%{fbroot}/bin-superserver/gdef
%{fbroot}/bin-superserver/gfix
%{fbroot}/bin-superserver/gpre
%{fbroot}/bin-superserver/gsplit
%{fbroot}/bin-superserver/gstat
%{fbroot}/bin-superserver/nbackup
%{fbroot}/bin-superserver/fb_config
%{fbroot}/plugins-superserver/*.so
%{_sbindir}/fbserver

%package	server-common
Summary:	Common files for Firebird SQL Database servers
Group:		Databases
# Due to moved files.
Conflicts:	firebird-server-classic < 2.0
Requires:	firebird-server = %{version}-%{release}
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	logrotate
Requires(pre): 	rpm-helper

%description		server-common
This package contains common files between firebird-server-classic and
firebird-server-superserver. You will need this if you want to use either one.

%files			server-common
%defattr(0644,root,root,0755)
%doc doc/license/IDPL.txt
%doc doc/license/README.license.usage.txt
%doc firebird.mdv.releasenote
%doc README.urpmi
%defattr(0644,root,root,0755)
%dir %attr(0755,root,root) %{_localstatedir}/lib/%{name}
%dir %attr(0775,%{name},%{name}) %{_localstatedir}/lib/%{name}/data
%attr(0660,%{name},%{name})	%{_localstatedir}/lib/%{name}/data/employee.fdb
%dir %attr(0775,%{name},%{name}) %{_localstatedir}/log/%{name}
%dir %{fbroot}/intl
%dir %{fbroot}/UDF
%{fbroot}/UDF/*
%ghost %{fbroot}/bin
%dir %{_sysconfdir}/%{name}
%dir %attr(0755,%{name},%{name}) %{_localstatedir}/lib/%{name}/system
%config(noreplace) %attr (0600,%{name},%{name}) %{_localstatedir}/lib/%{name}/system/security2.fdb
%config(noreplace) %attr (0664,%{name},%{name}) %{_sysconfdir}/%{name}/fbintl.conf
%config(noreplace) %attr (0664,%{name},%{name}) %{_sysconfdir}/%{name}/aliases.conf
%config(noreplace) %attr (0664,%{name},%{name}) %{_sysconfdir}/%{name}/firebird.conf
%config(noreplace) %attr (0664,%{name},%{name}) %{_sysconfdir}/%{name}/fbtrace.conf
%{fbroot}/intl/fbintl.conf
%config(noreplace) %attr(0664,%{name},%{name})  %{_localstatedir}/log/%{name}/%{name}.log
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/%{name}
%attr(0755,root,root) %{_libdir}/libib_util.so
%defattr(0755,root,root,0750)
%{fbroot}/intl/fbintl
%defattr(0755,root,root,0755)
%{_bindir}/gsec
%{_bindir}/gfix
%{_bindir}/nbackup
%{_bindir}/gstat-fb
%{_bindir}/gpre
%{_bindir}/gdef
%{_bindir}/gsplit
%{_bindir}/fb_config
%{_sbindir}/fbguard
%{_sbindir}/fb_lock_print
%dir %attr(0775,%{name},%{name}) %{_var}/run/%{name}

%prep
%setup -qn %{pkgname}
# convert intl character to UTF-8
iconv -f ISO-8859-1 -t utf-8 -c ./doc/README.intl -o ./doc/README.intl

%build
# disable -Wl,--no-undefined to avoid fail build of fbintl
# when fbintl is loaded, one of the modules (libfbembed or fbserver) for sure exports
# gds__log()
%define _disable_ld_no_undefined 1

# classic
NOCONFIGURE=1 ./autogen.sh
%configure \
	--prefix=%{fbroot} \
	--with-system-icu \
	--with-system-editline \
	--with-fbbin=%{fbroot}/bin-classic \
	--with-fbinclude=%{_includedir}/%{name} \
	--with-fbsbin=%{_sbindir} \
	--with-fbconf=%{_sysconfdir}/%{name} \
	--with-fblib=%{_libdir} \
	--with-fbdoc=%{_defaultdocdir}/%{name} \
	--with-fbudf=%{fbroot}/UDF \
	--with-fbsample=%{_defaultdocdir}/%{name}/examples \
	--with-fbsample-db=%{_localstatedir}/lib/%{name}/data/ \
	--with-fbhelp=%{_localstatedir}/lib/%{name}/system/ \
	--with-fbintl=%{fbroot}/intl \
	--with-fbmisc=%{fbroot}/misc \
	--with-fbsecure-db=%{_localstatedir}/lib/%{name}/system \
	--with-fbmsg=%{_localstatedir}/lib/%{name}/system \
	--with-fblog=%{_localstatedir}/log/%{name} \
	--with-fbglock=%{_var}/run/%{name} \
	--with-fbplugins=%{fbroot}/plugins-classic
# Can't use %%make as itsparallel build is broken
make
cd gen
sed "s@exit 1@# exit 1@" -i ./install/makeInstallImage.sh
sed "s@chown@echo ""# chown@g" -i ./install/makeInstallImage.sh
sed "s@chmod@echo ""# chmod@g" -i ./install/makeInstallImage.sh
./install/makeInstallImage.sh
mv ./buildroot/ buildroot-classic
cd ..

# superserver
make clean
NOCONFIGURE=1 ./autogen.sh
%configure \
	--prefix=%{fbroot} \
	--with-system-icu \
	--with-system-editline \
	--enable-superserver \
	--with-fbbin=%{fbroot}/bin-superserver \
	--with-fbinclude=%{_includedir}/%{name} \
	--with-fbsbin=%{_sbindir} \
	--with-fbconf=%{_sysconfdir}/%{name} \
	--with-fblib=%{_libdir} \
	--with-fbdoc=%{_defaultdocdir}/%{name} \
	--with-fbudf=%{fbroot}/UDF \
	--with-fbsample=%{_defaultdocdir}/%{name}/examples \
	--with-fbsample-db=%{_localstatedir}/lib/%{name}/data/ \
	--with-fbhelp=%{_localstatedir}/lib/%{name}/system/ \
	--with-fbintl=%{fbroot}/intl \
	--with-fbmisc=%{fbroot}/misc \
	--with-fbsecure-db=%{_localstatedir}/lib/%{name}/system \
	--with-fbmsg=%{_localstatedir}/lib/%{name}/system \
	--with-fblog=%{_localstatedir}/log/%{name} \
	--with-fbglock=%{_var}/run/%{name} \
	--with-fbplugins=%{fbroot}/plugins-superserver
# Can't use %%make as itsparallel build is broken
make
cd gen
sed "s@exit 1@echo ""# exit 1@" -i ./install/makeInstallImage.sh
sed "s@chown@echo ""# chown@g" -i ./install/makeInstallImage.sh
sed "s@chmod@echo ""# chmod@g" -i ./install/makeInstallImage.sh
./install/makeInstallImage.sh

cd %{_builddir}/%{pkgname}
sed "s@%%{fbroot}@%{fbroot}@g" %{SOURCE2} > firebird.mdv.releasenote

cat > README.urpmi <<EOF
You just installed or update %{name} server.
You can found important informations about mandriva %{name} rpms and database
management in:

%{_defaultdocdir}/%{name}-server-common/firebird.mdv.releasenote

Please, read it.
EOF

%install
# we wanted to setup both Classic and Superserver, we need to do all here
install -d %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{fbroot}/bin-superserver
mkdir -p %{buildroot}%{fbroot}/bin-classic
mkdir -p %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{fbroot}/UDF
mkdir -p %{buildroot}%{fbroot}/intl
mkdir -p %{buildroot}%{fbroot}/bin
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/data
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/system
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
mkdir -p %{buildroot}%{_var}/run/%{name}
mkdir -p %{buildroot}%{fbroot}/plugins-superserver
mkdir -p %{buildroot}%{fbroot}/plugins-classic
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sysconfdir}/xinetd.d
mkdir -p %{buildroot}%{_initrddir} 
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_bindir}

cd %{buildroot}
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{_sysconfdir}/%{name}/* %{buildroot}%{_sysconfdir}/%{name}
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/bin-classic/* %{buildroot}%{fbroot}/bin-classic
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{_sbindir}/fb_config %{buildroot}%{fbroot}/bin-classic/fb_config
sed "s@-classic@-superserver@" %{_builddir}/%{pkgname}/gen/buildroot-classic%{_sbindir}/fb_config > %{buildroot}%{fbroot}/bin-superserver/fb_config
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{_sbindir}/fbguard %{buildroot}%{_sbindir}/fbguard
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{_sbindir}/fb_inet_server %{buildroot}%{_sbindir}/fb_inet_server
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{_sbindir}/fb_lock_print %{buildroot}%{_sbindir}/fb_lock_print
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{_sbindir}/fb_smp_server %{buildroot}%{_sbindir}/fb_smp_server
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{_sbindir}/fbserver %{buildroot}%{_sbindir}/fbserver
rm -f %{_builddir}/%{pkgname}/gen/buildroot%{fbroot}/bin-superserver/fb_inet_server
rm -f %{_builddir}/%{pkgname}/gen/buildroot%{fbroot}/bin-superserver/fb_smp_server
rm -f %{_builddir}/%{pkgname}/gen/buildroot%{fbroot}/bin-superserver/changeMultiConnectMode.sh
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{fbroot}/bin-superserver/* %{buildroot}%{fbroot}/bin-superserver
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{_includedir}/*.h %{buildroot}%{_includedir}
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{_includedir}/%{name}/* %{buildroot}%{_includedir}/%{name}
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{_sysconfdir}/%{name}/* %{buildroot}%{_sysconfdir}/%{name}
rm -f %{buildroot}%{_sysconfdir}/%{name}/README
rm -f %{buildroot}%{_sysconfdir}/%{name}/WhatsNew
rm -f %{buildroot}%{_sysconfdir}/%{name}/IDPLicense.txt
rm -f %{buildroot}%{_sysconfdir}/%{name}/IPLicense.txt

cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{_libdir}/lib* %{buildroot}%{_libdir}
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{fbroot}/UDF/* %{buildroot}%{fbroot}/UDF
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{_localstatedir}/lib/%{name}/data/* %{buildroot}%{_localstatedir}/lib/%{name}/data
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{_localstatedir}/lib/%{name}/system/* %{buildroot}%{_localstatedir}/lib/%{name}/system
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{fbroot}/plugins-superserver/* %{buildroot}%{fbroot}/plugins-superserver
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/plugins-classic/* %{buildroot}%{fbroot}/plugins-classic
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/intl/fbintl %{buildroot}%{fbroot}/intl/fbintl
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/intl/fbintl.conf %{buildroot}%{_sysconfdir}/%{name}/fbintl.conf
ln -s %{_sysconfdir}/%{name}/fbintl.conf .%{fbroot}/intl/fbintl.conf


cd %{buildroot}%{_libdir}
ln -s libfbclient.so	libgds.so
ln -s libfbclient.so.%{major}	libgds.so.0
cd %{buildroot}

echo 1 > %{buildroot}%{_localstatedir}/log/%{name}/%{name}.log
sed	"s@%{name}.log@%{_localstatedir}/log/%{name}/%{name}.log@g"	%{SOURCE1}	>	%{buildroot}%{_sysconfdir}/logrotate.d/%{name}

sed	"s@= root@= %{name}@"	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/misc/%{name}.xinetd	>	%{buildroot}%{_sysconfdir}/xinetd.d/%{name}
cp	%{_builddir}/%{pkgname}/gen/buildroot%{fbroot}/misc/%{name}.init.d.mandrake	%{buildroot}%{_initrddir}/%{name}-superserver
cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/misc/%{name}.init.d.mandrake	%{buildroot}%{_initrddir}/%{name}-superclassic

cd	%{buildroot}
ln -s %{fbroot}/bin/fbsvcmgr .%{_bindir}/fbsvcmgr
ln -s %{fbroot}/bin/fbtracemgr .%{_bindir}/fbtracemgr
ln -s %{fbroot}/bin/gbak .%{_bindir}/gbak
ln -s %{fbroot}/bin/gdef .%{_bindir}/gdef
ln -s %{fbroot}/bin/gfix .%{_bindir}/gfix
ln -s %{fbroot}/bin/gpre .%{_bindir}/gpre
ln -s %{fbroot}/bin/gsec .%{_bindir}/gsec
ln -s %{fbroot}/bin/gsplit .%{_bindir}/gsplit
ln -s %{fbroot}/bin/gstat .%{_bindir}/gstat-fb
ln -s %{fbroot}/bin/isql .%{_bindir}/isql-fb
ln -s %{fbroot}/bin/nbackup .%{_bindir}/nbackup
ln -s %{fbroot}/bin/qli .%{_bindir}/qli
ln -s %{fbroot}/bin/fb_config .%{_bindir}/fb_config

# -----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# to bypass the rpm possible bug that don't do pre server-common
#----------------------------------------------------------------------------
%pre	server-classic
%_pre_useradd %{name} %{_localstatedir}/lib/%{name}/data /sbin/nologin

%post	server-classic
if [ "$(readlink %{fbroot}/bin 2> /dev/null)" \!= "%{fbroot}/bin-classic" ]; then 
 [ -e %{fbroot}/bin ] && rm -f %{fbroot}/bin
 ln -s %{fbroot}/bin{-classic,}
fi

%post   utils-classic
if [ "$(readlink %{fbroot}/bin 2> /dev/null)" \!= "%{fbroot}/bin-classic" ]; then
  [ -e %{fbroot}/bin ] && rm -f %{fbroot}/bin
  ln -s %{fbroot}/bin{-classic,}
fi

%preun	classic
if [ $1 -eq 0 ]; then
	if /sbin/service xinetd status >& /dev/null; then
		/sbin/service xinetd reload &>/dev/null || :
	fi
fi

%preun server-classic
if [ $1 -eq 0 ]; then
 if [ "$(readlink %{fbroot}/bin 2> /dev/null)" = "%{fbroot}/bin-classic" ]; then
  rm -f %{fbroot}/bin
 fi
fi

%preun utils-classic
if [ $1 -eq 0 ]; then
 if [ "$(readlink %{fbroot}/bin 2> /dev/null)" = "%{fbroot}/bin-classic" ]; then
 rm -f %{fbroot}/bin
 fi
fi

%post superclassic
if [ "$(readlink %{fbroot}/bin 2> /dev/null)" \!= "%{fbroot}/bin-classic" ]; then 
 [ -e %{fbroot}/bin ] && rm -f %{fbroot}/bin
 ln -s %{fbroot}/bin{-classic,}
fi

if [ ! -f /etc/gds_hosts.equiv ]; then
	echo localhost > /etc/gds_hosts.equiv
fi
%_post_service %{name}-superclassic

%preun superclassic
if [ $1 -eq 0 ]; then
 if /sbin/service firebird-superclassic status >& /dev/null; then
 /sbin/service firebird-superclassic stop
 fi
 chkconfig --del firebird-superclassic
fi
%_preun_service %{name}-superclassic 

%post	server-superserver
if [ "$(readlink %{fbroot}/bin 2> /dev/null)" \!= "%{fbroot}/bin-superserver" ]; then 
 [ -e %{fbroot}/bin ] && rm -f %{fbroot}/bin
 ln -s %{fbroot}/bin{-superserver,}
fi

if [ ! -f /etc/gds_hosts.equiv ]; then
	echo localhost > /etc/gds_hosts.equiv
fi
%_post_service %{name}-superserver

%post   utils-superserver
if [ "$(readlink %{fbroot}/bin 2> /dev/null)" \!= "%{fbroot}/bin-superserver" ]; then
 [ -e %{fbroot}/bin ] && rm -f %{fbroot}/bin
 ln -s %{fbroot}/bin{-superserver,}
fi

%preun server-superserver
if [ $1 -eq 0 ]; then
 if /sbin/service firebird-superserver status >& /dev/null; then
  /sbin/service firebird-superserver stop
 fi
 chkconfig --del firebird-superserver
 if [ "$(readlink %{fbroot}/bin 2> /dev/null)" = "%{fbroot}/bin-superserver" ]; then
  rm -f %{fbroot}/bin
 fi
fi
%_preun_service %{name}-superserver 

%pre server-common
# Create the firebird user and group if it doesn't exist
%_pre_useradd %{name} %{_localstatedir}/lib/%{name}/data /sbin/nologin
# Add gds_db to /etc/services if needed
FileName=/etc/services
newLine="gds_db          3050/tcp  # Firebird SQL Database Remote Protocol"
oldLine=`grep "^gds_db" $FileName`
if [ -z "$oldLine" ]; then
	echo $newLine >> $FileName
fi

%postun server-common
%_postun_userdel %{name}

