%if %mdkversion >= 200910
%define Werror_cflags %{nil}
%endif

%define major 2.1.2.18118
%define minor 0
%define version %{major}.%{minor}
%define pkgname Firebird
%define pkgversion %{major}-%{minor}

%define somajor 2
%define libfbclient %mklibname fbclient %somajor
%define libfbembed %mklibname fbembed %somajor

%define fbroot		%{_libdir}/%{name}

Summary:	Firebird SQL database management system
Name:		firebird
Version:	%{version}
Release:	%mkrel 2
Group:		Databases
License:	IPL
URL:		http://www.firebirdsql.org/
Source0:	http://downloads.sourceforge.net/firebird/%{pkgname}-%{pkgversion}.tar.bz2
# Source0:	http://aleron.dl.sourceforge.net/sourceforge/firebird/%{pkgname}-%{pkgversion}.tar.bz2
Source1:	firebird-2.0.0-profile.sh
Source2:	firebird-2.0.0-profile.csh
Patch0:		firebird-mcpu-to-mtune.patch
Patch1:		firebird-2.0.3-fix-initscript.patch
Patch2:		Firebird-edit_fix.diff
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	libtool
BuildRequires:  libncurses-devel
BuildRequires:  libtermcap-devel
BuildRequires:  icu-devel
BuildRequires:  edit-devel
Requires:	%{name}-arch = %{version}
Requires:	grep
Requires:	sed
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is the Firebird SQL Database shared files.

%files
%defattr(0644,root,root,0755)
%doc %{fbroot}/README
%doc %{fbroot}/WhatsNew
%doc %{fbroot}/doc/
%doc %{fbroot}/examples/
%attr (0660,%{name},%{name}) %{fbroot}/examples/empbuild/employee.fdb

#
# Meta packages for allowing urpmi asking only once
#
%package	classic
Summary:	Meta-package for Firebird SQL Classic Database (xinetd based)
Group:		Databases
Provides:	%{name}-arch = %{version}-%{release}
Requires:	%{name}-server-classic = %{version}
Requires:	%{name}-utils-classic = %{version}
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
Requires:	%{name} = %{version}
# Yes, we need force this. Otherwise, clients with this flavor will fail to build.
Requires:	%libfbclient

%description	devel
Development libraries for firebird.

%files devel
%defattr(0644,root,root,0755)
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
Requires:	%{name}-server-common = %{version}
Provides:	%{name}-utils = %{version}-%{release}
Conflicts:	%{name}-utils-superserver
Obsoletes:	%{name}-client-embedded <= 2.0

%description	utils-classic
Client access tools for firebird.

%files		utils-classic
%defattr(0755,root,root,0755)
%dir %{fbroot}/tools-classic
%dir %{fbroot}/bin
%{fbroot}/bin/gbak
%{fbroot}/tools-classic/gdef
%{fbroot}/bin/gfix
%{fbroot}/tools-classic/gpre
%{fbroot}/bin/gstat
%{fbroot}/bin/isql
%{fbroot}/bin/qli

#
# Utils programs (superserver)
#
%package	utils-superserver
Summary:	Client programs for Firebird SQL Database
Group:		Databases
Requires:	%{name}-server-common = %{version}
Provides:	%{name}-utils = %{version}-%{release}
Conflicts:	%{name}-utils-classic

%description	utils-superserver
Client access tools for firebird.

%files		utils-superserver
%defattr(0755,root,root,0755)
%dir %{fbroot}/tools-superserver
%dir %{fbroot}/bin
%{fbroot}/bin/gbak
%{fbroot}/tools-superserver/gdef
%{fbroot}/bin/gfix
%{fbroot}/tools-superserver/gpre
%{fbroot}/bin/gstat
%{fbroot}/bin/isql
%{fbroot}/bin/qli

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
%{fbroot}/lib/libfbclient.so.*

#
# Multi-process, independant client libraries
#
%package -n %libfbembed
Summary: Multi-process, non-local client libraries for Firebird SQL Database
Group: System/Libraries

%description -n %libfbembed
Multi-process, non-local client libraries for Firebird SQL Database

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
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%defattr(0755,root,root,0755)
%{fbroot}/bin/changeGdsLibraryCompatibleLink.sh
%{fbroot}/bin/fb_inet_server
%{fbroot}/bin/fb_lock_mgr
%{fbroot}/bin/fb_lock_print
%{fbroot}/bin/gds_drop
%{fbroot}/bin/fbsvcmgr
%{fbroot}/tools-classic/gsec
%{fbroot}/tools-classic/changeDBAPassword.sh
%{fbroot}/tools-classic/changeRunUser.sh
%{fbroot}/tools-classic/restoreRootRunUser.sh

#
# Super server programs
#
%package	server-superserver
Summary:	Superserver (single process) server for Firebird SQL Database
Group:		Databases
Provides:	firebird-server = %{version}-%{release}
#Requires:	%{name}
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
%defattr(0755,root,root,0755)
%{_sysconfdir}/rc.d/init.d/%{name}
%{fbroot}/bin/fb_lock_print
%{fbroot}/bin/fbguard
%{fbroot}/bin/fbmgr
%{fbroot}/bin/fbmgr.bin
%{fbroot}/bin/fbserver
%{fbroot}/tools-superserver/gsec
%{fbroot}/tools-superserver/changeDBAPassword.sh
%{fbroot}/tools-superserver/changeRunUser.sh
%{fbroot}/tools-superserver/restoreRootRunUser.sh

#
# Server's common files
#
%package		server-common
Summary:		Common files for Firebird SQL Database servers
Group:			Databases
# Due to moved files.
Conflicts:		firebird-server-classic < 2.0
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Requires(pre):		/usr/sbin/groupadd
Requires(pre):		/usr/sbin/useradd
Obsoletes:		%{name}-server-superserver < 2.0.1.12855.0-3mdk

%description		server-common
This package contains common files between firebird-server-classic and
firebird-server-superserver. You will need this if you want to use either one.

%files			server-common
%defattr(0644,root,root,0755)
%dir %attr(0775,%{name},%{name}) %{fbroot}
%dir %attr(0775,%{name},%{name}) %{_var}/lib/firebird/backup
%dir %attr(0775,%{name},%{name}) %{_var}/lib/firebird
%dir %{fbroot}/UDF
%dir %{fbroot}/intl
%config %attr (0660,%{name},%{name}) %{fbroot}/security2.fdb
%config(noreplace) %{fbroot}/aliases.conf
%config(noreplace) %{fbroot}/firebird.conf
%config(noreplace) %{fbroot}/intl/fbintl.conf
%{_sysconfdir}/%{name}/aliases.conf
%{_sysconfdir}/%{name}/firebird.conf
%attr(0660,%{name},%{name}) %{fbroot}/firebird.log
%{fbroot}/*.msg
%{fbroot}/help
%{fbroot}/UDF/fbudf.so
%{fbroot}/UDF/fbudf.sql
%{fbroot}/UDF/ib_udf.so
%{fbroot}/UDF/ib_udf.sql
%{fbroot}/UDF/ib_udf2.sql
%{_libdir}/libib_util.so
#%{_var}/lib/firebird/backup/no_empty
#%{_var}/lib/firebird/data/no_empty
#%{_var}/lib/firebird/system/help.fdb
#%{_var}/lib/firebird/system/security.fdb
%defattr(0755,root,root,0755)
%{_sysconfdir}/profile.d/firebird.csh
%{_sysconfdir}/profile.d/firebird.sh
%{fbroot}/intl/fbintl
%{fbroot}/bin/changeDBAPassword.sh
%{fbroot}/bin/changeRunUser.sh
%{fbroot}/bin/createAliasDB.sh
%{fbroot}/bin/fb_config
%{fbroot}/bin/gdef
%{fbroot}/bin/gpre
%{fbroot}/bin/gsec
%{fbroot}/bin/gsplit
%{fbroot}/bin/nbackup
%{fbroot}/bin/restoreRootRunUser.sh

%prep
%setup -q -n %{pkgname}-%{pkgversion}
%patch0 -p0
%patch1 -p0
%patch2 -p1

# -----------------------------------------------------------------------------

%build
# Fix permissions
chmod +x ./autogen.sh ./src/misc/writeBuildNum.sh

# <mrl> For reference, the proccess fb_lock_mgr that keeps executing after
# building finish is started at gen/Makefile.codes, line 60 (target
# build_codes) but I can't do nothing for it without major hacking.

autoreconf -fis

# server-classic
NOCONFIGURE=1 ./autogen.sh
%configure --prefix=%{fbroot} --with-system-editline --with-system-icu
# Can't use %%make as itsparallel build is broken
make
cd gen
./install/makeInstallImage.sh
mv ./buildroot/ buildroot-classic
chmod 644 ./buildroot-classic%{fbroot}/help/help.fdb
mkdir ./buildroot-classic%{fbroot}/tools-classic
for f in changeDBAPassword.sh changeRunUser.sh gdef \
	gpre gsec restoreRootRunUser.sh; do
	mv ./buildroot-classic%{fbroot}/{bin,tools-classic}/$f
	ln -s ../tools/$f ./buildroot-classic%{fbroot}/bin/$f
done
cd ..

# server-superserver
%configure --prefix=%{fbroot} --enable-superserver --with-system-editline --with-system-icu
# Can't use %%make as itsparallel build is broken
make
cd gen
./install/makeInstallImage.sh
mv ./buildroot/ buildroot-superserver
chmod 644 ./buildroot-superserver%{fbroot}/help/help.fdb
mkdir ./buildroot-superserver%{fbroot}/tools-superserver
for f in changeDBAPassword.sh changeRunUser.sh gdef \
	gpre gsec restoreRootRunUser.sh; do
	mv ./buildroot-superserver%{fbroot}/{bin,tools-superserver}/$f
done
cd ..

# -----------------------------------------------------------------------------

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}

# this is fugly and broken...
cp -a %{_builddir}/%{pkgname}-%{pkgversion}/gen/buildroot-superserver/* \
	%{buildroot}
cp -a %{_builddir}/%{pkgname}-%{pkgversion}/gen/buildroot-classic/* \
	%{buildroot}

cd %{buildroot}
mkdir -p .%{_sysconfdir}/%{name}
mkdir -p .%{_sysconfdir}/rc.d/init.d/
mkdir -p .%{_sysconfdir}/xinetd.d
mkdir -p .%{_sysconfdir}/profile.d
mkdir -p .%{_var}/run/%{name}
ln -s %{fbroot}/aliases.conf .%{_sysconfdir}/%{name}/
ln -s %{fbroot}/firebird.conf .%{_sysconfdir}/%{name}/
ln -s fbmgr.bin .%{fbroot}/bin/fbmgr
mv .%{fbroot}/misc/%{name}.xinetd .%{_sysconfdir}/xinetd.d/%{name}
mv .%{fbroot}/misc/%{name}.init.d.mandrake .%{_sysconfdir}/rc.d/init.d/%{name}
rm -rf .%{fbroot}/misc
sed "s@%%{fbroot}@%{fbroot}@g" %{_sourcedir}/firebird-2.0.0-profile.sh > .%{_sysconfdir}/profile.d/firebird.sh
sed "s@%%{fbroot}@%{fbroot}@g" %{_sourcedir}/firebird-2.0.0-profile.csh > .%{_sysconfdir}/profile.d/firebird.csh
touch .%{fbroot}/firebird.log

mkdir -p %{buildroot}%{_var}/lib/firebird/backup

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

%post server-classic
if test ! -e %{fbroot}/tools; then
	ln -s %{fbroot}/tools{-classic,}
fi
if /sbin/service xinetd status >& /dev/null; then
	/sbin/service xinetd reload
fi
if [ ! -f /etc/gds_hosts.equiv ]; then
	echo localhost > /etc/gds_hosts.equiv
fi


%preun server-classic
if [ $1 -eq 0 ]; then
	if /sbin/service xinetd status >& /dev/null; then
		/sbin/service xinetd reload
	fi
	if [ "$(readlink %{fbroot}/tools 2> /dev/null)" == "%{fbroot}/tools-classic" ]; then
		rm -f %{fbroot}/tools
	fi
fi

# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# server-superserver scripts
# -----------------------------------------------------------------------------
%post server-superserver
if test ! -e %{fbroot}/tools; then
	ln -s %{fbroot}/tools{-superserver,}
fi
if [ $1 -eq 2 ]; then
	if /sbin/service firebird status >& /dev/null; then
		/sbin/service firebird restart
	fi
fi
if [ $1 -eq 1 ]; then
	chkconfig firebird off
fi
if [ ! -f /etc/gds_hosts.equiv ]; then
	echo localhost > /etc/gds_hosts.equiv
fi

%preun server-superserver
if [ $1 -eq 0 ]; then
	if /sbin/service firebird status >& /dev/null; then
		/sbin/service firebird stop
	fi
	chkconfig --del firebird
	if [ "$(readlink %{fbroot}/tools >& /dev/null)" == "%{fbroot}/tools-superserver" ]; then
		rm -f %{fbroot}/tools
	fi
fi

# -----------------------------------------------------------------------------
# server-common scripts
# -----------------------------------------------------------------------------
%pre server-common
# Create the firebird group if it doesn't exist
grep -q %{name} /etc/group || /usr/sbin/groupadd -r %{name} || true
grep -q %{name} /etc/passwd || /usr/sbin/useradd -d / -g %{name} -s /sbin/sh -r %{name} || true

# Add gds_db to /etc/services if needed
FileName=/etc/services
newLine="gds_db          3050/tcp  # Firebird SQL Database Remote Protocol"
oldLine=`grep "^gds_db" $FileName`
if [ -z "$oldLine" ]; then
	echo $newLine >> $FileName
fi

%if %mdkversion < 200900
%post server-common -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun server-common -p /sbin/ldconfig
%endif


