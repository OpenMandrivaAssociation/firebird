%if %mdkversion >= 200910
%define Werror_cflags %{nil}
%endif

%define	major 2.1.3
%define pkgname Firebird-2.1.3.18185-0
%define version 2.1.3.18185.0
%define somajor 2
%define libfbclient %mklibname fbclient %somajor
%define libfbembed %mklibname fbembed %somajor

%define fbroot %{_libdir}/%{name}

Summary:	Firebird SQL database management system
Name:		firebird
Version:	%{version}
Release:	%mkrel 3
Group:		Databases
License:	IPL
URL:		http://www.firebirdsql.org/
#Source0:	http://downloads.sourceforge.net/firebird/%{pkgname}.tar.bz2
Source0:	http://firebirdsql.org/downloads/prerelease/source/%{pkgname}.RC2.tar.bz2
Source1:	firebird-logrotate
Source2:	firebird.mdv.releasenote
Patch0:		firebird-mcpu-to-mtune.patch
Patch1:		firebird.init.d.mandrake.in.patch
Patch2:		Firebird-edit_fix.diff
Patch3:		firebird_lock-file-location.patch
Patch4:		firebird-gcc-icu.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	libtool
BuildRequires:  libncurses-devel
BuildRequires:  libtermcap-devel
BuildRequires:  icu-devel
BuildRequires:  edit-devel
BuildRequires:	gcc-c++
Requires:	%{name}-arch = %{version}-%{release}
Requires:	grep
Requires:	sed
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is the Firebird SQL Database shared files.

%files
%defattr(0644,root,root,0755)
%doc doc/license/IDPL.txt
%doc doc/license/README.license.usage.txt
%doc gen/buildroot-classic%{fbroot}/doc
%doc gen/buildroot-classic%{fbroot}/examples
%doc gen/buildroot-classic%{fbroot}/README
%doc gen/buildroot-classic%{fbroot}/misc/intl.sql
%doc gen/buildroot-classic%{fbroot}/misc/upgrade

#
# Meta packages for allowing urpmi asking only once
#
%package	classic
Summary:	Meta-package for Firebird SQL Classic Database (xinetd based)
Group:		Databases
Provides:	%{name}-arch = %{version}-%{release}
Requires:	%{name}-server-classic = %{version}
Requires:	%{name}-utils-classic = %{version}
# Yes, we need force this. Otherwise, only direct local access wil be available.
Requires:	%libfbclient
Conflicts:	%{name}-superserver

%description	classic
This is a meta-package for easy selecting the Classic arch for Firebird 2

%files		classic

%package	superserver
Summary:	Meta-package for Firebird SQL SuperServer Database (standalone)
Group:		Databases
Provides:	%{name}-arch = %{version}-%{release}
Requires:	%{name}-server-superserver = %{version}
Requires:	%{name}-utils-superserver = %{version}
Conflicts:	%{name}-classic

%description	superserver
This is a meta-package for easy selecting the SuperServer arch for Firebird 2

%files		superserver

#
# Development headers and static libraries
#
%package	devel
Summary:	Development Libraries for Firebird SQL Database
Group:		Development/Databases
Requires:	%libfbclient
Requires:	%libfbembed

%description	devel
Development libraries for firebird.

%files devel
%defattr(0644,root,root,0755)
%dir %{fbroot}/include
%{fbroot}/include/*
%{fbroot}/lib/*.so
%{_includedir}/*
%{_libdir}/*.so

#
# Standard client programs
#

#
# Utils programs (classic)
#
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
%defattr(0755,root,root,0755)
%dir %{fbroot}/tools-classic
%{fbroot}/tools-classic/gbak
%{fbroot}/tools-classic/fbsvcmgr
%{fbroot}/tools-classic/isql
%{fbroot}/tools-classic/qli

#
# Utils programs (superserver)
#
%package	utils-superserver
Summary:	Client programs for Firebird SQL Database
Group:		Databases
Provides:	%{name}-utils-arch = %{version}-%{release}
Requires:	%{name}-utils-common = %{version}
Conflicts:	%{name}-utils-classic

%description	utils-superserver
Client access tools for firebird.

%files		utils-superserver
%defattr(0755,root,root,0755)
%dir %{fbroot}/tools-superserver
%{fbroot}/tools-superserver/gbak
%{fbroot}/tools-superserver/fbsvcmgr
%{fbroot}/tools-superserver/isql
%{fbroot}/tools-superserver/qli

%package	utils-common
Summary:	Client programs for Firebird SQL Database
Group:		Databases
Requires:	%{name}-utils-arch = %{version}-%{release}

%description	utils-common
Common client access tools for firebird.

%files			utils-common
%defattr(0644,root,root,0755)
%doc doc/license/IDPL.txt
%doc doc/license/README.license.usage.txt
%defattr(0755,root,root,0755)
%dir %{fbroot}
%dir %{fbroot}/bin
%ghost %{fbroot}/tools
%{_bindir}/isql-fb
%{_bindir}/gbak
%{_bindir}/fbsvcmgr
%{_bindir}/qli
%{fbroot}/bin/gbak
%{fbroot}/bin/fbsvcmgr
%{fbroot}/bin/isql
%{fbroot}/bin/qli
%defattr(0644,root,root,0755)
%{fbroot}/*.msg

#
# Multi-threaded, independant client libraries
#
%package -n %libfbclient
Summary: Multi-threaded, non-local client libraries for Firebird SQL Database
Group: System/Libraries

%description -n %libfbclient
Multi-threaded, non-local client libraries for Firebird SQL Database

%files -n %libfbclient
%defattr(0644,root,root,0755)
%dir %{fbroot}/lib
%{_libdir}/libfbclient.so.*
%{_libdir}/libgds.so.0
%{fbroot}/lib/libfbclient.so.*

#
# Multi-process, independant client libraries
#
%package -n %libfbembed
Summary: Multi-process, local client libraries for Firebird SQL Database
Group: System/Libraries

%description -n %libfbembed
Multi-process, local client libraries for Firebird SQL Database

%files -n %libfbembed
%defattr(0644,root,root,0755)
%dir %{fbroot}/lib
%{_libdir}/libfbembed.so.*
%{fbroot}/lib/libfbembed.so.*

#
# Classic server programs
#
%package	server-classic
Summary:	Classic (xinetd) server for Firebird SQL Database
Group:		Databases
Provides:	firebird-server = %{version}-%{release}
Requires:	xinetd
Requires:	%{name}-server-common = %{version}
Conflicts:	%{name}-server-superserver

%description	server-classic
This is the classic (xinetd) server for the Firebird SQL Database.
It can also be used as an embedded server, when paired with the
client-embedded package.

It does not include any client access tools, nor does it include the
multi-threaded client library. 

%files		server-classic
%defattr(0644,root,root,0755)
%dir %{fbroot}/bin
%dir %{fbroot}/tools-classic
%dir %{fbroot}/UDF/classic
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%defattr(0755,root,root,0755)
%{fbroot}/bin/fb_inet_server
%attr(6550,root,firebird) %{fbroot}/bin/fb_lock_mgr
%{fbroot}/bin/gds_drop
%{fbroot}/tools-classic/fb_lock_print
%{fbroot}/tools-classic/gsec
%{fbroot}/tools-classic/gdef
%{fbroot}/tools-classic/gfix
%{fbroot}/tools-classic/gpre
%{fbroot}/tools-classic/gsplit
%{fbroot}/tools-classic/gstat
%{fbroot}/tools-classic/nbackup
%{fbroot}/tools-classic/*.sh
%{fbroot}/tools-classic/fb_config
%defattr(0644,root,root,-)
%{fbroot}/UDF/classic/*.so

#
# Super server programs
#
%package	server-superserver
Summary:	Superserver (single process) server for Firebird SQL Database
Group:		Databases
Provides:	firebird-server = %{version}-%{release}
Requires:	%{name}-server-common = %{version}-%{release}
Conflicts:	%{name}-server-classic

%description	server-superserver
This is the Superserver (single process) for the Firebird SQL Database.

It does not include any client access tools, nor does it include the
multi-threaded client library.

%files		server-superserver
%defattr(0644,root,root,0755)
%dir %attr(0775,%{name},%{name}) %{_var}/run/%{name}
%dir %{fbroot}/bin
%dir %{fbroot}/tools-superserver
%dir %{fbroot}/UDF/superserver
%defattr(0755,root,root,0755)
%{_initrddir}/%{name}
%{fbroot}/bin/fbguard
%{fbroot}/bin/fbmgr
%{fbroot}/bin/fbmgr.bin
%{fbroot}/bin/fbserver
%{fbroot}/tools-superserver/fb_lock_print
%{fbroot}/tools-superserver/gsec
%{fbroot}/tools-superserver/gdef
%{fbroot}/tools-superserver/gfix
%{fbroot}/tools-superserver/gpre
%{fbroot}/tools-superserver/gsplit
%{fbroot}/tools-superserver/gstat
%{fbroot}/tools-superserver/nbackup
%{fbroot}/tools-superserver/*.sh
%{fbroot}/tools-superserver/fb_config
%defattr(0644,root,root,755)
%{fbroot}/UDF/superserver/*.so

#
# Server's common files
#
%package		server-common
Summary:		Common files for Firebird SQL Database servers
Group:			Databases
# Due to moved files.
Conflicts:		firebird-server-classic < 2.0
Requires:		firebird-server = %{version}-%{release}
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Requires(pre):		/usr/sbin/groupadd
Requires(pre):		/usr/sbin/useradd
Requires:		logrotate
Obsoletes:		%{name}-server-superserver < 2.0.1.12855.0-3mdk

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
%dir %attr(0770,%{name},%{name}) %{_localstatedir}/lib/%{name}/data
%attr(0660,%{name},%{name})	%{_localstatedir}/lib/%{name}/data/employee.fdb
%dir %attr(0775,%{name},%{name}) %{_localstatedir}/log/%{name}
%{fbroot}/%{name}.log
%dir %{fbroot}/intl
%ghost %{fbroot}/tools
%dir %{fbroot}/UDF
%dir %{_sysconfdir}/%{name}
%dir %attr(0770,%{name},%{name}) %{_localstatedir}/lib/%{name}/system
%config(noreplace) %attr (0600,%{name},%{name}) %{_localstatedir}/lib/%{name}/system/security2.fdb
%{fbroot}/security2.fdb
%config(noreplace) %attr (0664,%{name},%{name}) %{_sysconfdir}/%{name}/fbintl.conf
%config(noreplace) %attr (0664,%{name},%{name}) %{_sysconfdir}/%{name}/aliases.conf
%config(noreplace) %attr (0664,%{name},%{name}) %{_sysconfdir}/%{name}/firebird.conf
%{fbroot}/aliases.conf
%{fbroot}/firebird.conf
%{fbroot}/intl/fbintl.conf
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/%{name}
%{fbroot}/*.msg
%{fbroot}/help
%{_libdir}/libib_util.so
%{fbroot}/lib/libib_util.so
%defattr(0644,root,root,0644)
%{fbroot}/UDF/*.sql
%defattr(0644,root,root,0755)
%ghost %{fbroot}/UDF/*.so
%{fbroot}/intl/fbintl
%dir %attr(0755,%{name},%{name}) %{_var}/run/%{name}
%defattr(0755,root,root,0755)
%{_bindir}/gsec
%{_bindir}/gfix
%{_bindir}/nbackup
%{_bindir}/gstat-fb
%{fbroot}/run
%{fbroot}/bin/fb_lock_print
%{fbroot}/bin/gsec
%{fbroot}/bin/gdef
%{fbroot}/bin/gfix
%{fbroot}/bin/gpre
%{fbroot}/bin/gsplit
%{fbroot}/bin/gstat
%{fbroot}/bin/nbackup
%{fbroot}/bin/*.sh
%{fbroot}/bin/fb_config


%prep
%setup -q -n %{pkgname}
# convert intl character to UTF-8
iconv -f ISO-8859-1 -t utf-8 -c ./doc/README.intl -o ./doc/README.intl
%patch0 -p0
%patch1	-p0
%patch2 -p1
%patch3 -p0
%patch4 -p0

# -----------------------------------------------------------------------------

%build
# Fix permissions
chmod +x ./autogen.sh ./src/misc/writeBuildNum.sh

# <mrl> For reference, the proccess fb_lock_mgr that keeps executing after
# building finish is started at gen/Makefile.codes, line 60 (target
# build_codes) but I can't do nothing for it without major hacking.

# classic
NOCONFIGURE=1 ./autogen.sh
%configure --prefix=%{fbroot} --with-system-editline --with-system-icu
# Can't use %%make as itsparallel build is broken
make
cd gen
./install/makeInstallImage.sh
mv ./buildroot/ buildroot-classic
chmod 644 ./buildroot-classic%{fbroot}/help/help.fdb
cd ..

# superserver
make clean
NOCONFIGURE=1 ./autogen.sh
%configure --prefix=%{fbroot} --enable-superserver --with-system-editline --with-system-icu
# Can't use %%make as itsparallel build is broken
make
cd gen
./install/makeInstallImage.sh
mv ./buildroot/ buildroot-superserver
chmod 644 ./buildroot-superserver%{fbroot}/help/help.fdb

cd %{_builddir}/%{pkgname}
sed "s@%%{fbroot}@%{fbroot}@g" %{SOURCE2} > firebird.mdv.releasenote

cat > README.urpmi <<EOF
You just installed or update %{name} server.
You can found important informations about mandriva %{name} rpms and database
management in:

%{_defaultdocdir}/%{name}-server-common/firebird.mdv.releasenote

Please, read it.
EOF

# -----------------------------------------------------------------------------

%install
# we wanted to setup both Classic and Superserver, we need to do all here
rm -rf %{buildroot}
install	-d	%{buildroot}
cd	%{buildroot}

mkdir	-p	%{buildroot}%{_sysconfdir}/%{name}
mkdir	-p	%{buildroot}%{_initrddir} 
mkdir	-p	%{buildroot}%{_sysconfdir}/xinetd.d
mkdir	-p	%{buildroot}%{_sysconfdir}/profile.d
mkdir	-p	%{buildroot}%{_sysconfdir}/logrotate.d
mkdir	-p	%{buildroot}%{_var}/run/%{name}
mkdir	-p	%{buildroot}%{_localstatedir}/lib/%{name}
mkdir	-p	%{buildroot}%{_localstatedir}/lib/%{name}/data
mkdir	-p	%{buildroot}%{_localstatedir}/lib/%{name}/system
mkdir	-p	%{buildroot}%{_localstatedir}/log/%{name}
mkdir	-p	%{buildroot}%{_includedir}/%{name}
mkdir	-p	%{buildroot}%{_libdir}
mkdir	-p	%{buildroot}%{fbroot}
mkdir	-p	%{buildroot}%{fbroot}/help
mkdir	-p	%{buildroot}%{fbroot}/intl
mkdir	-p	%{buildroot}%{fbroot}/lib
mkdir	-p	%{buildroot}%{fbroot}/include
mkdir	-p	%{buildroot}%{fbroot}/bin
mkdir	-p	%{buildroot}%{fbroot}/UDF
mkdir	-p	%{buildroot}%{fbroot}/tools
mkdir	-p	%{buildroot}%{fbroot}/tools-classic
mkdir	-p	%{buildroot}%{fbroot}/UDF/classic
mkdir	-p	%{buildroot}%{fbroot}/tools-superserver
mkdir	-p	%{buildroot}%{fbroot}/UDF/superserver
mkdir	-p	%{buildroot}%{_bindir} 

cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/examples/empbuild/employee.fdb		%{buildroot}%{_localstatedir}/lib/%{name}/data/employee.fdb
cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/help/help.fdb		%{buildroot}%{fbroot}/help/help.fdb
cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/*.msg		%{buildroot}%{fbroot}/
cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/intl/fbintl		%{buildroot}%{fbroot}/intl/fbintl
cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/lib/libib_util.so		%{buildroot}%{fbroot}/lib/
cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/lib/libfbclient.so.%{major}		%{buildroot}%{fbroot}/lib/
cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/lib/libfbembed.so.%{major}		%{buildroot}%{fbroot}/lib/
for f in fb_inet_server fb_lock_mgr gds_drop; do
	mv {%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/bin,%{buildroot}%{fbroot}/bin}/$f
done	
cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/bin/*		%{buildroot}%{fbroot}/tools-classic/
cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/UDF/*.so		%{buildroot}%{fbroot}/UDF/classic/
cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/UDF/*.so		%{buildroot}%{fbroot}/UDF/
cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/UDF/*.sql		%{buildroot}%{fbroot}/UDF/
for f in fbguard fbmgr.bin fbserver; do
	mv {%{_builddir}/%{pkgname}/gen/buildroot-superserver%{fbroot}/bin,%{buildroot}%{fbroot}/bin}/$f
done	
cp	%{_builddir}/%{pkgname}/gen/buildroot-superserver%{fbroot}/bin/*		%{buildroot}%{fbroot}/tools-superserver/
cp	%{_builddir}/%{pkgname}/gen/buildroot-superserver%{fbroot}/UDF/*.so		%{buildroot}%{fbroot}/UDF/superserver/

cd	%{buildroot}%{fbroot}/bin
ln	-s	fbmgr.bin	fbmgr
for f in $(ls -1 %{buildroot}%{fbroot}/tools-superserver);do
	ln -s %{fbroot}/tools/$f $f
done	
cd	%{buildroot}

major2=`echo %{major} | sed 's|\.[0-9]*$||'`
major1=`echo ${major2} | sed 's|\.[0-9]*$||'`
cd	%{buildroot}%{fbroot}/lib/
ln	-s	%{fbroot}/lib/libfbembed.so.%{major}	libfbembed.so.${major2}
ln	-s	%{fbroot}/lib/libfbembed.so.${major2}	libfbembed.so
ln	-s	%{fbroot}/lib/libfbclient.so.%{major}	libfbclient.so.${major1}
ln	-s	%{fbroot}/lib/libfbclient.so.${major1}	libfbclient.so
cd	%{buildroot}

cd	%{buildroot}%{_libdir}
ln	-s	%{fbroot}/lib/libfbembed.so	libfbembed.so
ln	-s	%{fbroot}/lib/libfbembed.so.${major2}	libfbembed.so.${major2}
ln	-s	%{fbroot}/lib/libfbembed.so.%{major}	libfbembed.so.%{major}
ln	-s	%{fbroot}/lib/libfbclient.so	libfbclient.so
ln	-s	%{fbroot}/lib/libfbclient.so.${major1}	libfbclient.so.${major1}
ln	-s	%{fbroot}/lib/libfbclient.so.%{major}	libfbclient.so.%{major}
ln	-s	%{fbroot}/lib/libfbclient.so.%{major}	libgds.so.0
ln	-s	%{fbroot}/lib/libfbclient.so	libgds.so
ln	-s	%{fbroot}/lib/libib_util.so	libib_util.so
cd	%{buildroot}

ln	-sf	%{_localstatedir}/log/%{name}/%{name}.log	.%{fbroot}/%{name}.log	
sed	"s@%{name}.log@%{_localstatedir}/log/%{name}/%{name}.log@g"	%{SOURCE1}	>	%{buildroot}%{_sysconfdir}/logrotate.d/%{name}

cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/include/*		%{buildroot}%{_includedir}/%{name}/
cd	%{buildroot}%{fbroot}/include/
ln	-s	%{_includedir}/%{name}/ibase.h	ibase.h
ln	-s	%{_includedir}/%{name}/iberror.h	iberror.h
ln	-s	%{_includedir}/%{name}/ib_util.h	ib_util.h
ln	-s	%{_includedir}/%{name}/perf.h	perf.h
cd	%{buildroot}%{_includedir}
ln	-s	%{_includedir}/%{name}/ibase.h	ibase.h
ln	-s	%{_includedir}/%{name}/iberror.h	iberror.h
ln	-s	%{_includedir}/%{name}/ib_util.h	ib_util.h
ln	-s	%{_includedir}/%{name}/perf.h	perf.h
cd	%{buildroot}

cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/aliases.conf	.%{_sysconfdir}/%{name}/aliases.conf
sed	"s@%{fbroot}/examples/empbuild@%{_localstatedir}/lib/%{name}/data@"	-i	.%{_sysconfdir}/%{name}/aliases.conf	
cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/firebird.conf	.%{_sysconfdir}/%{name}/firebird.conf
cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/intl/fbintl.conf	.%{_sysconfdir}/%{name}/fbintl.conf
cp	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/security2.fdb	.%{_localstatedir}/lib/%{name}/system/security2.fdb

ln	-s	%{_sysconfdir}/%{name}/aliases.conf	.%{fbroot}/aliases.conf
ln	-s	%{_sysconfdir}/%{name}/firebird.conf	.%{fbroot}/firebird.conf
ln	-s	%{_localstatedir}/lib/%{name}/system/security2.fdb	.%{fbroot}/security2.fdb
ln	-s	%{_sysconfdir}/%{name}/fbintl.conf	.%{fbroot}/intl/fbintl.conf

sed	"s@= root@= %{name}@"	%{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/misc/%{name}.xinetd	>	%{buildroot}%{_sysconfdir}/xinetd.d/%{name}
cp	%{_builddir}/%{pkgname}/gen/buildroot-superserver%{fbroot}/misc/%{name}.init.d.mandrake	%{buildroot}%{_initrddir}/%{name}

ln	-s	%{_var}/run/%{name}	.%{fbroot}/run
ln	-s	%{fbroot}/bin/isql	.%{_bindir}/isql-fb
ln	-s	%{fbroot}/bin/gbak	.%{_bindir}/gbak
ln	-s	%{fbroot}/bin/gfix	.%{_bindir}/gfix
ln	-s	%{fbroot}/bin/gsec	.%{_bindir}/gsec
ln	-s	%{fbroot}/bin/nbackup	.%{_bindir}/nbackup
ln	-s	%{fbroot}/bin/gstat	.%{_bindir}/gstat-fb
ln	-s	%{fbroot}/bin/fbsvcmgr	.%{_bindir}/fbsvcmgr
ln	-s	%{fbroot}/bin/qli	.%{_bindir}/qli


# -----------------------------------------------------------------------------

%clean
rm -rf %{buildroot}

# -----------------------------------------------------------------------------
# lib scripts
# -----------------------------------------------------------------------------
# While using -p flag, you can't leave comments until the next tag.
%if %mdkversion < 200900
%post -n %libfbclient -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libfbclient -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%post -n %libfbembed -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libfbembed -p /sbin/ldconfig
%endif

%post	server-classic
type=classic
for dir in tools;do
	[ -L %{fbroot}/$dir ] || rm -rf %{fbroot}/$dir
	ln -sf $dir-$type %{fbroot}/$dir
done 
for f in $(ls 1 %{fbroot}/UDF/$type/);do
	cp -f %{fbroot}/UDF/$type/$f %{fbroot}/UDF/$f
done

%preun	server-classic
if [ $1 -eq 0 ]; then
	if /sbin/service xinetd status >& /dev/null; then
		/sbin/service xinetd reload &>/dev/null || :
	fi
fi


# -----------------------------------------------------------------------------
# superserver scripts
# -----------------------------------------------------------------------------
%post	server-superserver
type=superserver
for dir in tools;do
	[ -L %{fbroot}/$dir ] || rm -rf %{fbroot}/$dir
	ln -sf $dir-$type %{fbroot}/$dir
done
for f in $(ls 1 %{fbroot}/UDF/$type/);do
	cp -f %{fbroot}/UDF/$type/$f %{fbroot}/UDF/$f
done

if [ ! -f /etc/gds_hosts.equiv ]; then
	echo localhost > /etc/gds_hosts.equiv
fi
%_post_service %{name}

%preun server-superserver
if [ $1 -eq 0 ]; then
	if /sbin/service firebird status >& /dev/null; then
		/sbin/service firebird stop
	fi
	chkconfig --del firebird
fi
%_preun_service %{name} 

# -----------------------------------------------------------------------------
# server-common scripts
# -----------------------------------------------------------------------------
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

%preun server-common
%_post_userdel %{name}

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

