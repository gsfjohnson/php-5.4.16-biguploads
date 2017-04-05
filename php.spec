# API/ABI check
%global apiver      20100412
%global zendver     20100525
%global pdover      20080721
# Extension version
%global fileinfover 1.0.5
%global pharver     2.0.1
%global zipver      1.11.0
%global jsonver     1.2.1

# Adds -z now to the linker flags
%global _hardened_build 1

# version used for php embedded library soname
%global embed_version 5.4

%global mysql_sock %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest: %{expand: %%global runselftest 1}}

# Use the arch-specific mysql_config binary to avoid mismatch with the
# arch detection heuristic used by bindir/mysql_config.
%global mysql_config %{_libdir}/mysql/mysql_config

%global with_fpm 1

# Build mysql/mysqli/pdo extensions using libmysqlclient or only mysqlnd
%global with_libmysql 1

# Build ZTS extension or only NTS
%global with_zts 0

%if 0%{?__isa_bits:1}
%global isasuffix -%{__isa_bits}
%else
%global isasuffix %nil
%endif

# /usr/sbin/apsx with httpd < 2.4 and defined as /usr/bin/apxs with httpd >= 2.4
%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:     %{expand: %%global _httpd_moddir     %%{_libdir}/httpd/modules}}
%{!?_httpd_contentdir: %{expand: %%global _httpd_contentdir /var/www}}

%if 0%{?fedora} < 17 && 0%{?rhel} < 7
%global with_zip     0
%global with_libzip  0
%global zipmod       %nil
%else
%global with_zip     1
%global with_libzip  1
%global zipmod       zip
%endif

%if 0%{?fedora} < 18 && 0%{?rhel} < 7
%global db_devel  db4-devel
%else
%global db_devel  libdb-devel
%endif

%global _performance_build 1

#global rcver RC2

Summary: PHP scripting language for creating dynamic web sites
Name: php54bu
Version: 5.4.16
Release: 42.zendto%{?dist}
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM is licensed under BSD
License: PHP and Zend and BSD
Group: Development/Languages
URL: http://www.php.net/

Source0: http://www.php.net/distributions/php-%{version}%{?rcver}.tar.bz2
Source1: php.conf
Source2: php.ini
Source3: macros.php
Source4: php-fpm.conf
Source5: php-fpm-www.conf
Source6: php-fpm.service
Source7: php-fpm.logrotate
Source8: php-fpm.sysconfig
Source9: php.modconf
Source10: php.ztsmodconf

# Build fixes
Patch5: php-5.2.0-includedir.patch
Patch6: php-5.2.4-embed.patch
Patch7: php-5.3.0-recode.patch
Patch8: php-5.4.7-libdb.patch

# Fixes for extension modules
# https://bugs.php.net/63171 no odbc call during timeout
Patch21: php-5.4.7-odbctimer.patch
# Fixed Bug #64949 (Buffer overflow in _pdo_pgsql_error)
Patch22: php-5.4.16-pdopgsql.patch
# Fixed bug #64960 (Segfault in gc_zval_possible_root)
Patch23: php-5.4.16-gc.patch
# Fixed Bug #64915 (error_log ignored when daemonize=0)
Patch24: php-5.4.16-fpm.patch
# https://bugs.php.net/65143 php-cgi man page
# https://bugs.php.net/65142 phar man page
Patch25: php-5.4.16-man.patch
# https://bugs.php.net/66987 fileinfo / bigendian
Patch26: php-5.4.16-bug66987.patch
# https://bugs.php.net/50444 pdo_odbc / x86_64
Patch27: php-5.4.16-bug50444.patch
# https://bugs.php.net/63595 gmp memory allocator
Patch28: php-5.4.16-bug63595.patch
# https://bugs.php.net/62129 session rfc1867
Patch29: php-5.4.16-bug62129.patch
# https://bugs.php.net/66762 mysqli segfault
Patch30: php-5.4.16-bug66762.patch
# https://bugs.php.net/65641 fpm script name
Patch31: php-5.4.6-bug65641.patch
# https://bugs.php.net/71089 duplicate ext
Patch32: php-5.4.16-bug71089.patch
# https://bugs.php.net/66833 default digest algo
Patch33: php-5.4.16-bug66833.patch
# fixed variable corruption
Patch34: php-5.4.16-wddx.patch
# bad logic in sapi header callback routine
Patch35: php-5.4.16-bug66375.patch

# Functional changes
Patch40: php-5.4.0-dlopen.patch
Patch41: php-5.4.0-easter.patch
Patch42: php-5.3.1-systzdata-v10.patch
# See http://bugs.php.net/53436
Patch43: php-5.4.0-phpize.patch
# Use system libzip instead of bundled one
Patch44: php-5.4.15-system-libzip.patch
# Use -lldap_r for OpenLDAP
Patch45: php-5.4.8-ldap_r.patch
# Make php_config.h constant across builds
Patch46: php-5.4.9-fixheader.patch
# drop "Configure command" from phpinfo output
Patch47: php-5.4.9-phpinfo.patch
# Fix php_select on aarch64 (http://bugs.php.net/67406)
Patch48: php-5.4.16-aarch64-select.patch
Patch49: php-5.4.16-curltls.patch

# Fixes for tests
Patch60: php-5.4.16-pdotests.patch

# Security fixes
Patch100: php-5.4.17-CVE-2013-4013.patch
Patch101: php-5.4.16-CVE-2013-4248.patch
Patch102: php-5.4.16-CVE-2013-6420.patch
Patch104: php-5.4.16-CVE-2014-1943.patch
Patch105: php-5.4.16-CVE-2013-6712.patch
Patch107: php-5.4.16-CVE-2014-2270.patch
Patch108: php-5.4.16-CVE-2013-7345.patch
Patch109: php-5.4.16-CVE-2014-0237.patch
Patch110: php-5.4.16-CVE-2014-0238.patch
Patch111: php-5.4.16-CVE-2014-3479.patch
Patch112: php-5.4.16-CVE-2014-3480.patch
Patch113: php-5.4.16-CVE-2014-4721.patch
Patch114: php-5.4.16-CVE-2014-4049.patch
Patch115: php-5.4.16-CVE-2014-3515.patch
Patch116: php-5.4.16-CVE-2014-0207.patch
Patch117: php-5.4.16-CVE-2014-3487.patch
Patch118: php-5.4.16-CVE-2014-2497.patch
Patch119: php-5.4.16-CVE-2014-3478.patch
Patch120: php-5.4.16-CVE-2014-3538.patch
Patch121: php-5.4.16-CVE-2014-3587.patch
Patch122: php-5.4.16-CVE-2014-5120.patch
Patch123: php-5.4.16-CVE-2014-4698.patch
Patch124: php-5.4.16-CVE-2014-4670.patch
Patch125: php-5.4.16-CVE-2014-3597.patch
Patch126: php-5.4.16-CVE-2014-3668.patch
Patch127: php-5.4.16-CVE-2014-3669.patch
Patch128: php-5.4.16-CVE-2014-3670.patch
Patch129: php-5.4.16-CVE-2014-3710.patch
Patch130: php-5.4.16-CVE-2014-8142.patch
Patch131: php-5.4.16-CVE-2015-0231.patch
Patch132: php-5.4.16-CVE-2015-0232.patch
Patch133: php-5.4.16-CVE-2014-9652.patch
Patch134: php-5.4.16-CVE-2014-9709.patch
Patch135: php-5.4.16-CVE-2015-0273.patch
Patch136: php-5.4.16-CVE-2014-9705.patch
Patch137: php-5.4.16-CVE-2015-2301.patch
Patch138: php-5.4.16-bug69085.patch
Patch139: php-5.4.16-CVE-2015-2787.patch
Patch140: php-5.4.16-CVE-2015-2348.patch
Patch145: php-5.4.16-CVE-2015-4022.patch
Patch146: php-5.4.16-CVE-2015-4021.patch
Patch147: php-5.4.16-CVE-2015-4024.patch
Patch148: php-5.4.16-CVE-2015-4025.patch
Patch149: php-5.4.16-CVE-2015-3330.patch
Patch150: php-5.4.16-bug69353.patch
Patch151: php-5.4.16-CVE-2015-2783.patch
Patch152: php-5.4.16-CVE-2015-3329.patch
Patch153: php-5.4.16-bug68819.patch
Patch154: php-5.4.16-bug69152.patch
Patch155: php-5.4.16-CVE-2016-5385.patch
Patch156: php-5.4.16-CVE-2016-5766.patch
Patch157: php-5.4.16-CVE-2016-5767.patch
Patch158: php-5.4.16-CVE-2016-5768.patch
Patch159: php-5.4.16-CVE-2016-5399.patch
Patch160: php-biguploads.patch


BuildRequires: bzip2-devel, curl-devel >= 7.9, gmp-devel
BuildRequires: httpd-devel >= 2.0.46-1, pam-devel
BuildRequires: libstdc++-devel, openssl-devel
BuildRequires: sqlite-devel >= 3.6.0
BuildRequires: zlib-devel, sendmail, libedit-devel
BuildRequires: pcre-devel >= 6.6
BuildRequires: bzip2, perl, libtool >= 1.4.3, gcc-c++
BuildRequires: libtool-ltdl-devel
%if %{with_libzip}
BuildRequires: libzip-devel >= 0.10
%endif

Obsoletes: php-dbg, php3, phpfi, stronghold-php
%if %{with_zts}
Obsoletes: php-zts < 5.3.7
Provides: php-zts = %{version}-%{release}
Provides: php-zts%{?_isa} = %{version}-%{release}
%endif

Requires: httpd-mmn = %{_httpd_mmn}
Provides: mod_php = %{version}-%{release}
Requires: php-common%{?_isa} = %{version}-%{release}
# For backwards-compatibility, require php-cli for the time being:
Requires: php-cli%{?_isa} = %{version}-%{release}
# To ensure correct /var/lib/php/session ownership:
Requires(pre): httpd


# Don't provides extensions, which are not shared library, as .so
%{?filter_provides_in: %filter_provides_in %{_libdir}/php/modules/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{_libdir}/php-zts/modules/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{_httpd_moddir}/.*\.so$}
%{?filter_setup}


%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts. 

The php package contains the module (often referred to as mod_php)
which adds support for the PHP language to Apache HTTP Server.

%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-cgi = %{version}-%{release}, php-cgi%{?_isa} = %{version}-%{release}
Provides: php-pcntl, php-pcntl%{?_isa}
Provides: php-readline, php-readline%{?_isa}

%description cli
The php-cli package contains the command-line interface 
executing PHP scripts, /usr/bin/php, and the CGI interface.


%if %{with_fpm}
%package fpm
Group: Development/Languages
Summary: PHP FastCGI Process Manager
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM and fpm are licensed under BSD
License: PHP and Zend and BSD
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: systemd-devel
BuildRequires: systemd-units
Requires: systemd-units
Requires(pre): /usr/sbin/useradd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# This is actually needed for the %%triggerun script but Requires(triggerun)
# is not valid.  We can use %%post because this particular %%triggerun script
# should fire just after this package is installed.
Requires(post): systemd-sysv

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.
%endif

%package common
Group: Development/Languages
Summary: Common files for PHP
# All files licensed under PHP version 3.01, except
# fileinfo is licensed under PHP version 3.0
# regex, libmagic are licensed under BSD
# main/snprintf.c, main/spprintf.c and main/rfc1867.c are ASL 1.0
License: PHP and BSD and ASL 1.0
# ABI/API check - Arch specific
Provides: php-api = %{apiver}%{isasuffix}, php-zend-abi = %{zendver}%{isasuffix}
Provides: php(api) = %{apiver}%{isasuffix}, php(zend-abi) = %{zendver}%{isasuffix}
Provides: php(language) = %{version}, php(language)%{?_isa} = %{version}
# Provides for all builtin/shared modules:
Provides: php-bz2, php-bz2%{?_isa}
Provides: php-calendar, php-calendar%{?_isa}
Provides: php-core = %{version}, php-core%{?_isa} = %{version}
Provides: php-ctype, php-ctype%{?_isa}
Provides: php-curl, php-curl%{?_isa}
Provides: php-date, php-date%{?_isa}
Provides: php-ereg, php-ereg%{?_isa}
Provides: php-exif, php-exif%{?_isa}
Provides: php-fileinfo, php-fileinfo%{?_isa}
Provides: php-pecl-Fileinfo = %{fileinfover}, php-pecl-Fileinfo%{?_isa} = %{fileinfover}
Provides: php-pecl(Fileinfo) = %{fileinfover}, php-pecl(Fileinfo)%{?_isa} = %{fileinfover}
Provides: php-filter, php-filter%{?_isa}
Provides: php-ftp, php-ftp%{?_isa}
Provides: php-gettext, php-gettext%{?_isa}
Provides: php-gmp, php-gmp%{?_isa}
Provides: php-hash, php-hash%{?_isa}
Provides: php-mhash = %{version}, php-mhash%{?_isa} = %{version}
Provides: php-iconv, php-iconv%{?_isa}
Provides: php-json, php-json%{?_isa}
Provides: php-pecl-json = %{jsonver}, php-pecl-json%{?_isa} = %{jsonver}
Provides: php-pecl(json) = %{jsonver}, php-pecl(json)%{?_isa} = %{jsonver}
Provides: php-libxml, php-libxml%{?_isa}
Provides: php-openssl, php-openssl%{?_isa}
Provides: php-pecl-phar = %{pharver}, php-pecl-phar%{?_isa} = %{pharver}
Provides: php-pecl(phar) = %{pharver}, php-pecl(phar)%{?_isa} = %{pharver}
Provides: php-phar, php-phar%{?_isa}
Provides: php-pcre, php-pcre%{?_isa}
Provides: php-reflection, php-reflection%{?_isa}
Provides: php-session, php-session%{?_isa}
Provides: php-shmop, php-shmop%{?_isa}
Provides: php-simplexml, php-simplexml%{?_isa}
Provides: php-sockets, php-sockets%{?_isa}
Provides: php-spl, php-spl%{?_isa}
Provides: php-standard = %{version}, php-standard%{?_isa} = %{version}
Provides: php-tokenizer, php-tokenizer%{?_isa}
%if %{with_zip}
Provides: php-zip, php-zip%{?_isa}
Provides: php-pecl-zip = %{zipver}, php-pecl-zip%{?_isa} = %{zipver}
Provides: php-pecl(zip) = %{zipver}, php-pecl(zip)%{?_isa} = %{zipver}
Obsoletes: php-pecl-zip < 1.11
%endif
Provides: php-zlib, php-zlib%{?_isa}
Obsoletes: php-openssl
Obsoletes: php-pecl-json < 1.2.2
Obsoletes: php-pecl-phar < 1.2.4
Obsoletes: php-pecl-Fileinfo < 1.0.5
Obsoletes: php-mhash < 5.3.0
%description common
The php-common package contains files used by both the php
package and the php-cli package.

%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: php-cli%{?_isa} = %{version}-%{release}, autoconf, automake
Requires: pcre-devel%{?_isa}
Obsoletes: php-pecl-pdo-devel
%if %{with_zts}
Provides: php-zts-devel = %{version}-%{release}
Provides: php-zts-devel%{?_isa} = %{version}-%{release}
%endif

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package ldap
Summary: A module for PHP applications that use LDAP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Obsoletes: mod_php3-ldap, stronghold-php-ldap
BuildRequires: cyrus-sasl-devel, openldap-devel, openssl-devel

%description ldap
The php-ldap adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language.

%package pdo
Summary: A database access abstraction module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-pdo-sqlite, php-pecl-pdo
# ABI/API check - Arch specific
Provides: php-pdo-abi = %{pdover}%{isasuffix}
Provides: php(pdo-abi) = %{pdover}%{isasuffix}
Provides: php-sqlite3, php-sqlite3%{?_isa}
Provides: php-pdo_sqlite, php-pdo_sqlite%{?_isa}

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other 
databases.

%if %{with_libmysql}
%package mysql
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-mysqli = %{version}-%{release}
Provides: php-mysqli%{?_isa} = %{version}-%{release}
Provides: php-pdo_mysql, php-pdo_mysql%{?_isa}
Obsoletes: mod_php3-mysql, stronghold-php-mysql
BuildRequires: mysql-devel >= 4.1.0
Conflicts: php-mysqlnd

%description mysql
The php-mysql package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.
%endif

%package mysqlnd
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-mysql = %{version}-%{release}
Provides: php-mysql%{?_isa} = %{version}-%{release}
Provides: php-mysqli = %{version}-%{release}
Provides: php-mysqli%{?_isa} = %{version}-%{release}
Provides: php-pdo_mysql, php-pdo_mysql%{?_isa}
%if ! %{with_libmysql}
Obsoletes: php-mysql < %{version}-%{release}
%endif

%description mysqlnd
The php-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

This package use the MySQL Native Driver

%package pgsql
Summary: A PostgreSQL database module for PHP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-pdo_pgsql, php-pdo_pgsql%{?_isa}
Obsoletes: mod_php3-pgsql, stronghold-php-pgsql
BuildRequires: krb5-devel, openssl-devel, postgresql-devel

%description pgsql
The php-pgsql add PostgreSQL database support to PHP.
PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package process
Summary: Modules for PHP script using system process interfaces
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-posix, php-posix%{?_isa}
Provides: php-sysvsem, php-sysvsem%{?_isa}
Provides: php-sysvshm, php-sysvshm%{?_isa}
Provides: php-sysvmsg, php-sysvmsg%{?_isa}

%description process
The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

%package odbc
Summary: A module for PHP applications that use ODBC databases
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# pdo_odbc is licensed under PHP version 3.0
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-pdo_odbc, php-pdo_odbc%{?_isa}
Obsoletes: stronghold-php-odbc
BuildRequires: unixODBC-devel

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%package soap
Summary: A module for PHP applications that use the SOAP protocol
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: libxml2-devel

%description soap
The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}, net-snmp
BuildRequires: net-snmp-devel

%description snmp
The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package xml
Summary: A module for PHP applications which use XML
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Obsoletes: php-domxml, php-dom
Provides: php-dom, php-dom%{?_isa}
Provides: php-xsl, php-xsl%{?_isa}
Provides: php-domxml, php-domxml%{?_isa}
Provides: php-wddx, php-wddx%{?_isa}
Provides: php-xmlreader, php-xmlreader%{?_isa}
Provides: php-xmlwriter, php-xmlwriter%{?_isa}
BuildRequires: libxslt-devel >= 1.0.18-1, libxml2-devel >= 2.4.14-1

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package xmlrpc
Summary: A module for PHP applications which use the XML-RPC protocol
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libXMLRPC is licensed under BSD
License: PHP and BSD
Requires: php-common%{?_isa} = %{version}-%{release}

%description xmlrpc
The php-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libmbfl is licensed under LGPLv2
# onigurama is licensed under BSD
# ucgendat is licensed under OpenLDAP
License: PHP and LGPLv2 and BSD and OpenLDAP
Requires: php-common%{?_isa} = %{version}-%{release}

%description mbstring
The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package gd
Summary: A module for PHP applications for using the gd graphics library
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libgd is licensed under BSD
License: PHP and BSD
Requires: php-common%{?_isa} = %{version}-%{release}
# Required to build the bundled GD library
BuildRequires: libjpeg-devel, libpng-devel, freetype-devel
BuildRequires: libXpm-devel, t1lib-devel

%description gd
The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libbcmath is licensed under LGPLv2+
License: PHP and LGPLv2+
Requires: php-common%{?_isa} = %{version}-%{release}

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package dba
Summary: A database abstraction layer module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: %{db_devel}, tokyocabinet-devel
Requires: php-common%{?_isa} = %{version}-%{release}

%description dba
The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%package embedded
Summary: PHP library for embedding in applications
Group: System Environment/Libraries
Requires: php-common%{?_isa} = %{version}-%{release}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides: php-embedded-devel = %{version}-%{release}
Provides: php-embedded-devel%{?_isa} = %{version}-%{release}

%description embedded
The php-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.

%package pspell
Summary: A module for PHP applications for using pspell interfaces
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0

%description pspell
The php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.

%package recode
Summary: A module for PHP applications for using the recode library
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: recode-devel

%description recode
The php-recode package contains a dynamic shared object that will add
support for using the recode library to PHP.

%package intl
Summary: Internationalization extension for PHP applications
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: libicu-devel >= 3.6

%description intl
The php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%package enchant
Summary: Enchant spelling extension for PHP applications
Group: System Environment/Libraries
# All files licensed under PHP version 3.0
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: enchant-devel >= 1.2.4

%description enchant
The php-enchant package contains a dynamic shared object that will add
support for using the enchant library to PHP.


%prep
%setup -q -n php-%{version}%{?rcver}

%patch5 -p1 -b .includedir
%patch6 -p1 -b .embed
%patch7 -p1 -b .recode
%patch8 -p1 -b .libdb

%patch21 -p1 -b .odbctimer
%patch22 -p1 -b .pdopgsql
%patch23 -p1 -b .gc
%patch24 -p1 -b .fpm
%patch25 -p1 -b .manpages
%patch26 -p1 -b .bug66987
%patch27 -p1 -b .bug50444
%patch28 -p1 -b .bug63595
%patch29 -p1 -b .bug62129
%patch30 -p1 -b .bug66762
%patch31 -p1 -b .bug65641
%patch32 -p1 -b .bug71089
%patch33 -p1 -b .bug66833
%patch34 -p1 -b .fix
%patch35 -p1 -b .bug66375

%patch40 -p1 -b .dlopen
%patch41 -p1 -b .easter
%patch42 -p1 -b .systzdata
%patch43 -p1 -b .headers
%if %{with_libzip}
%patch44 -p1 -b .systzip
%endif
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%patch45 -p1 -b .ldap_r
%endif
%patch46 -p1 -b .fixheader
%patch47 -p1 -b .phpinfo
%patch48 -p1 -b .aarch64select
%patch49 -p1 -b .curltls

%patch60 -p1 -b .pdotests

%patch100 -p1 -b .cve4113
%patch101 -p1 -b .cve4248
%patch102 -p1 -b .cve6420
%patch104 -p1 -b .cve1943
%patch105 -p1 -b .cve6712
%patch107 -p1 -b .cve2270
%patch108 -p1 -b .cve7345
%patch109 -p1 -b .cve0237
%patch110 -p1 -b .cve0238
%patch111 -p1 -b .cve3479
%patch112 -p1 -b .cve3480
%patch113 -p1 -b .cve4721
%patch114 -p1 -b .cve4049
%patch115 -p1 -b .cve3515
%patch116 -p1 -b .cve0207
%patch117 -p1 -b .cve3487
%patch118 -p1 -b .cve2497
%patch119 -p1 -b .cve3478
%patch120 -p1 -b .cve3538
%patch121 -p1 -b .cve3587
%patch122 -p1 -b .cve5120
%patch123 -p1 -b .cve4698
%patch124 -p1 -b .cve4670
%patch125 -p1 -b .cve3597
%patch126 -p1 -b .cve3668
%patch127 -p1 -b .cve3669
%patch128 -p1 -b .cve3670
%patch129 -p1 -b .cve3710
%patch130 -p1 -b .cve8142
%patch131 -p1 -b .cve0231
%patch132 -p1 -b .cve0232
%patch133 -p1 -b .cve9652
%patch134 -p1 -b .cve9709
%patch135 -p1 -b .cve0273
%patch136 -p1 -b .cve9705
%patch137 -p1 -b .cve2301
%patch138 -p1 -b .bug68095
%patch139 -p1 -b .cve2787
%patch140 -p1 -b .cve2348
%patch145 -p1 -b .cve4022
%patch146 -p1 -b .cve4021
%patch147 -p1 -b .cve4024
%patch148 -p1 -b .cve4025
%patch149 -p1 -b .cve3330
%patch150 -p1 -b .bug69353
%patch151 -p1 -b .cve2783
%patch152 -p1 -b .cve3329
%patch153 -p1 -b .bug68819
%patch154 -p1 -b .bug69152
%patch155 -p1 -b .cve5385
%patch156 -p1 -b .cve5766
%patch157 -p1 -b .cve5767
%patch158 -p1 -b .cve5768
%patch159 -p1 -b .cve5399
%patch160 -p1 -b .biguploads


# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp ext/ereg/regex/COPYRIGHT regex_COPYRIGHT
cp ext/gd/libgd/README libgd_README
cp ext/gd/libgd/COPYING libgd_COPYING
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/mbstring/oniguruma/COPYING oniguruma_COPYING
cp ext/mbstring/ucgendat/OPENLDAP_LICENSE ucgendat_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/phar/LICENSE phar_LICENSE
cp ext/bcmath/libbcmath/COPYING.LIB libbcmath_COPYING

# Multiple builds for multiple SAPIs
mkdir build-cgi build-apache build-embedded \
%if %{with_zts}
    build-zts build-ztscli \
%endif
%if %{with_fpm}
    build-fpm
%endif

# ----- Manage known as failed test -------
# php_egg_logo_guid() removed by patch41
rm -f tests/basic/php_egg_logo_guid.phpt
# affected by systzdata patch
rm -f ext/date/tests/timezone_location_get.phpt
# fails sometime
rm -f ext/sockets/tests/mcast_ipv?_recv.phpt

# Safety check for API version change.
pver=$(sed -n '/#define PHP_VERSION /{s/.* "//;s/".*$//;p}' main/php_version.h)
if test "x${pver}" != "x%{version}%{?rcver}"; then
   : Error: Upstream PHP version is now ${pver}, expecting %{version}%{?rcver}.
   : Update the version/rcver macros and rebuild.
   exit 1
fi

vapi=`sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h`
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=`sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h`
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

# Safety check for PDO ABI version change
vpdo=`sed -n '/#define PDO_DRIVER_API/{s/.*[ 	]//;p}' ext/pdo/php_pdo_driver.h`
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

# Check for some extension version
ver=$(sed -n '/#define PHP_FILEINFO_VERSION /{s/.* "//;s/".*$//;p}' ext/fileinfo/php_fileinfo.h)
if test "$ver" != "%{fileinfover}"; then
   : Error: Upstream FILEINFO version is now ${ver}, expecting %{fileinfover}.
   : Update the fileinfover macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_PHAR_VERSION /{s/.* "//;s/".*$//;p}' ext/phar/php_phar.h)
if test "$ver" != "%{pharver}"; then
   : Error: Upstream PHAR version is now ${ver}, expecting %{pharver}.
   : Update the pharver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_ZIP_VERSION_STRING /{s/.* "//;s/".*$//;p}' ext/zip/php_zip.h)
if test "$ver" != "%{zipver}"; then
   : Error: Upstream ZIP version is now ${ver}, expecting %{zipver}.
   : Update the zipver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
   : Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
   : Update the jsonver macro and rebuild.
   exit 1
fi

# https://bugs.php.net/63362 - Not needed but installed headers.
# Drop some Windows specific headers to avoid installation,
# before build to ensure they are really not needed.
rm -f TSRM/tsrm_win32.h \
      TSRM/tsrm_config.w32.h \
      Zend/zend_config.w32.h \
      ext/mysqlnd/config-win.h \
      ext/standard/winver.h \
      main/win32_internal_function_disabled.h \
      main/win95nt.h

# Fix some bogus permissions
find . -name \*.[ch] -exec chmod 644 {} \;
chmod 644 README.*

# php-fpm configuration files for tmpfiles.d
echo "d /run/php-fpm 755 root root" >php-fpm.tmpfiles

# bring in newer Red Hat config.guess and config.sub for aarch64/ppc64p7 support
cp -f /usr/lib/rpm/redhat/config.{guess,sub} .


%build
# aclocal workaround - to be improved
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4

# Force use of system libtool:
libtoolize --force --copy
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4

# Regenerate configure scripts (patches change config.m4's)
touch configure.in
./buildconf --force

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
export CFLAGS

# Install extension modules in %{_libdir}/php/modules.
EXTENSION_DIR=%{_libdir}/php/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{_datadir}/pear; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
# Old/recent bison version seems to produce a broken parser;
# upstream uses GNU Bison 2.3. Workaround:
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend
ln -sf ../configure
%configure \
	--cache-file=../config.cache \
        --with-libdir=%{_lib} \
	--with-config-file-path=%{_sysconfdir} \
	--with-config-file-scan-dir=%{_sysconfdir}/php.d \
	--disable-debug \
	--with-pic \
	--disable-rpath \
	--without-pear \
	--with-bz2 \
	--with-exec-dir=%{_bindir} \
	--with-freetype-dir=%{_prefix} \
	--with-png-dir=%{_prefix} \
	--with-xpm-dir=%{_prefix} \
	--enable-gd-native-ttf \
	--with-t1lib=%{_prefix} \
	--without-gdbm \
	--with-gettext \
	--with-gmp \
	--with-iconv \
	--with-jpeg-dir=%{_prefix} \
	--with-openssl \
        --with-pcre-regex=%{_prefix} \
	--with-zlib \
	--with-layout=GNU \
	--enable-exif \
	--enable-ftp \
	--enable-sockets \
	--with-kerberos \
	--enable-shmop \
	--enable-calendar \
        --with-libxml-dir=%{_prefix} \
	--enable-xml \
        --with-system-tzdata \
	--with-mhash \
	$* 
if test $? != 0; then 
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

# Build /usr/bin/php-cgi with the CGI SAPI, and all the shared extensions
pushd build-cgi

build --libdir=%{_libdir}/php \
      --enable-pcntl \
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-gd=shared \
      --enable-bcmath=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-tcadb=%{_prefix} \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysql=shared,mysqlnd \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared,%{_prefix} \
      --with-sqlite3=shared,%{_prefix} \
      --enable-json=shared \
%if %{with_zip}
      --enable-zip=shared \
%endif
%if %{with_libzip}
      --with-libzip \
%endif
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --enable-intl=shared \
      --with-icu-dir=%{_prefix} \
      --with-enchant=shared,%{_prefix} \
      --with-recode=shared,%{_prefix}
popd

without_shared="--without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-xmlreader --disable-xmlwriter \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --disable-json --without-pspell --disable-wddx \
      --without-curl --disable-posix \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=%{_httpd_apxs} \
      --libdir=%{_libdir}/php \
%if %{with_libmysql}
      --enable-pdo=shared \
      --with-mysql=shared,%{_prefix} \
      --with-mysqli=shared,%{mysql_config} \
      --with-pdo-mysql=shared,%{mysql_config} \
      --without-pdo-sqlite \
%else
      --without-mysql \
      --disable-pdo \
%endif
      ${without_shared}
popd

%if %{with_fpm}
# Build php-fpm
pushd build-fpm
build --enable-fpm \
      --with-fpm-systemd \
      --libdir=%{_libdir}/php \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd
%endif

# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp5.so
pushd build-embedded
build --enable-embed \
      --without-mysql --disable-pdo \
      ${without_shared}
popd

%if %{with_zts}
# Build a special thread-safe (mainly for modules)
pushd build-ztscli

EXTENSION_DIR=%{_libdir}/php-zts/modules
build --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      --enable-pcntl \
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-gd=shared \
      --enable-bcmath=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-tcadb=%{_prefix} \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysql=shared,mysqlnd \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
      --enable-mysqlnd-threading \
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared,%{_prefix} \
      --with-sqlite3=shared,%{_prefix} \
      --enable-json=shared \
%if %{with_zip}
      --enable-zip=shared \
%endif
%if %{with_libzip}
      --with-libzip \
%endif
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --enable-intl=shared \
      --with-icu-dir=%{_prefix} \
      --with-enchant=shared,%{_prefix} \
      --with-recode=shared,%{_prefix}
popd

# Build a special thread-safe Apache SAPI
pushd build-zts
build --with-apxs2=%{_httpd_apxs} \
      --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
%if %{with_libmysql}
      --enable-pdo=shared \
      --with-mysql=shared,%{_prefix} \
      --with-mysqli=shared,%{mysql_config} \
      --with-pdo-mysql=shared,%{mysql_config} \
      --without-pdo-sqlite \
%else
      --without-mysql \
      --disable-pdo \
%endif
      ${without_shared}
popd

### NOTE!!! EXTENSION_DIR was changed for the -zts build, so it must remain
### the last SAPI to be built.
%endif


%check
%if %runselftest
cd build-apache
# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
export SKIP_ONLINE_TESTS=1
unset TZ LANG LC_ALL
if ! make test; then
  set +x
  for f in `find .. -name \*.diff -type f -print`; do
    echo "TEST FAILURE: $f --"
    cat "$f"
    echo "-- $f result ends."
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_
%endif

%install
%if %{with_zts}
# Install the extensions for the ZTS version
make -C build-ztscli install \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# rename extensions build with mysqlnd
mv $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/mysqlnd_mysql.so
mv $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/mysqli.so \
   $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/mysqlnd_mysqli.so
mv $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/pdo_mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/pdo_mysqlnd.so

%if %{with_libmysql}
# Install the extensions for the ZTS version modules for libmysql
make -C build-zts install-modules \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# rename ZTS binary
mv $RPM_BUILD_ROOT%{_bindir}/php        $RPM_BUILD_ROOT%{_bindir}/zts-php
mv $RPM_BUILD_ROOT%{_bindir}/phpize     $RPM_BUILD_ROOT%{_bindir}/zts-phpize
mv $RPM_BUILD_ROOT%{_bindir}/php-config $RPM_BUILD_ROOT%{_bindir}/zts-php-config
%endif

# Install the version for embedded script language in applications + php_embed.h
make -C build-embedded install-sapi install-headers \
     INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with_fpm}
# Install the php-fpm binary
make -C build-fpm install-fpm \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# Install everything from the CGI SAPI build
make -C build-cgi install \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# rename extensions build with mysqlnd
mv $RPM_BUILD_ROOT%{_libdir}/php/modules/mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/php/modules/mysqlnd_mysql.so
mv $RPM_BUILD_ROOT%{_libdir}/php/modules/mysqli.so \
   $RPM_BUILD_ROOT%{_libdir}/php/modules/mysqlnd_mysqli.so
mv $RPM_BUILD_ROOT%{_libdir}/php/modules/pdo_mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/php/modules/pdo_mysqlnd.so

%if %{with_libmysql}
# Install the mysql extension build with libmysql
make -C build-apache install-modules \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# Install the default configuration file and icons
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_contentdir}/icons
install -m 644 php.gif $RPM_BUILD_ROOT%{_httpd_contentdir}/icons/php.gif

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/php

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_moddir}
install -m 755 build-apache/libs/libphp5.so $RPM_BUILD_ROOT%{_httpd_moddir}

%if %{with_zts}
# install the ZTS DSO
install -m 755 build-zts/libs/libphp5.so $RPM_BUILD_ROOT%{_httpd_moddir}/libphp5-zts.so
%endif

# Apache config fragment
%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# Single config file with httpd < 2.4 (fedora <= 17)
install -D -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%if %{with_zts}
cat %{SOURCE10} >>$RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%endif
cat %{SOURCE1} >>$RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%else
# Dual config file with httpd >= 2.4 (fedora >= 18)
install -D -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-php.conf
%if %{with_zts}
cat %{SOURCE10} >>$RPM_BUILD_ROOT%{_httpd_modconfdir}/10-php.conf
%endif
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%endif

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
%if %{with_zts}
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d
%endif
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/session

%if %{with_fpm}
# PHP-FPM stuff
# Log
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/log/php-fpm
install -m 755 -d $RPM_BUILD_ROOT/run/php-fpm
# Config
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf.default .
# tmpfiles.d
install -m 755 -d $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d
install -m 644 php-fpm.tmpfiles $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/php-fpm.conf
# install systemd unit files and scripts for handling server startup
install -m 755 -d $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}/
# LogRotate
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/php-fpm
# Environment file
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/php-fpm
%endif
# Fix the link
(cd $RPM_BUILD_ROOT%{_bindir}; ln -sfn phar.phar phar)

# Generate files lists and stub .ini files for each subpackage
for mod in pgsql odbc ldap snmp xmlrpc \
    mysqlnd mysqlnd_mysql mysqlnd_mysqli pdo_mysqlnd \
    mbstring gd dom xsl soap bcmath dba xmlreader xmlwriter \
    pdo pdo_pgsql pdo_odbc pdo_sqlite json %{zipmod} \
    sqlite3 \
    enchant phar fileinfo intl \
    pspell curl wddx \
    posix sysvshm sysvsem sysvmsg recode \
%if %{with_libmysql}
    mysql mysqli pdo_mysql \
%endif
    ; do
    cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
%if %{with_zts}
    cat > $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
%endif
    cat > files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/php/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php.d/${mod}.ini
%if %{with_zts}
%attr(755,root,root) %{_libdir}/php-zts/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php-zts.d/${mod}.ini
%endif
EOF
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx > files.xml

# The mysql and mysqli modules are both packaged in php-mysql
%if %{with_libmysql}
cat files.mysqli >> files.mysql
cat files.pdo_mysql >> files.mysql
%endif

# mysqlnd
cat files.mysqlnd_mysql \
    files.mysqlnd_mysqli \
    files.pdo_mysqlnd \
    >> files.mysqlnd

# Split out the PDO modules
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc

# sysv* and posix in packaged in php-process
cat files.sysv* files.posix > files.process

# Package sqlite3 and pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.pdo_sqlite >> files.pdo
cat files.sqlite3 >> files.pdo

# Package json, zip, curl, phar and fileinfo in -common.
cat files.json files.curl files.phar files.fileinfo > files.common
%if %{with_zip}
cat files.zip >> files.common
%endif

# Install the macros file:
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rpm
sed -e "s/@PHP_APIVER@/%{apiver}%{isasuffix}/" \
    -e "s/@PHP_ZENDVER@/%{zendver}%{isasuffix}/" \
    -e "s/@PHP_PDOVER@/%{pdover}%{isasuffix}/" \
    -e "s/@PHP_VERSION@/%{version}/" \
%if ! %{with_zts}
    -e "/zts/d" \
%endif
    < %{SOURCE3} > macros.php
install -m 644 -c macros.php \
           $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.php

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/php/modules/*.a \
       $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{_datadir}/pear \
       $RPM_BUILD_ROOT%{_libdir}/libphp5.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}


%if %{with_fpm}
%pre fpm
# Add the "apache" user as we don't require httpd
getent group  apache >/dev/null || \
  groupadd -g 48 -r apache
getent passwd apache >/dev/null || \
  useradd -r -u 48 -g apache -s /sbin/nologin \
    -d %{_httpd_contentdir} -c "Apache" apache
exit 0

%post fpm
%if 0%{?systemd_post:1}
%systemd_post php-fpm.service
%else
if [ $1 = 1 ]; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%endif

%preun fpm
%if 0%{?systemd_preun:1}
%systemd_preun php-fpm.service
%else
if [ $1 = 0 ]; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable php-fpm.service >/dev/null 2>&1 || :
    /bin/systemctl stop php-fpm.service >/dev/null 2>&1 || :
fi
%endif

%postun fpm
%if 0%{?systemd_postun_with_restart:1}
%systemd_postun_with_restart php-fpm.service
%else
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ]; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart php-fpm.service >/dev/null 2>&1 || :
fi
%endif

# Handle upgrading from SysV initscript to native systemd unit.
# We can tell if a SysV version of php-fpm was previously installed by
# checking to see if the initscript is present.
%triggerun fpm -- php-fpm
if [ -f /etc/rc.d/init.d/php-fpm ]; then
    # Save the current service runlevel info
    # User must manually run systemd-sysv-convert --apply php-fpm
    # to migrate them to systemd targets
    /usr/bin/systemd-sysv-convert --save php-fpm >/dev/null 2>&1 || :

    # Run these because the SysV package being removed won't do them
    /sbin/chkconfig --del php-fpm >/dev/null 2>&1 || :
    /bin/systemctl try-restart php-fpm.service >/dev/null 2>&1 || :
fi
%endif

%post embedded -p /sbin/ldconfig
%postun embedded -p /sbin/ldconfig

%files
%{_httpd_moddir}/libphp5.so
%if %{with_zts}
%{_httpd_moddir}/libphp5-zts.so
%endif
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%config(noreplace) %{_httpd_confdir}/php.conf
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/10-php.conf
%endif
%{_httpd_contentdir}/icons/php.gif

%files common -f files.common
%doc CODING_STANDARDS CREDITS EXTENSIONS LICENSE NEWS README*
%doc Zend/ZEND_* TSRM_LICENSE regex_COPYRIGHT
%doc libmagic_LICENSE
%doc phar_LICENSE
%doc php.ini-*
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%if %{with_zts}
%dir %{_sysconfdir}/php-zts.d
%dir %{_libdir}/php-zts
%dir %{_libdir}/php-zts/modules
%endif
%dir %{_localstatedir}/lib/php
%dir %{_datadir}/php

%files cli
%{_bindir}/php
%{_bindir}/php-cgi
%{_bindir}/phar.phar
%{_bindir}/phar
# provides phpize here (not in -devel) for pecl command
%{_bindir}/phpize
%{_mandir}/man1/php.1*
%{_mandir}/man1/php-cgi.1*
%{_mandir}/man1/phar.1*
%{_mandir}/man1/phar.phar.1*
%{_mandir}/man1/phpize.1*
%doc sapi/cgi/README* sapi/cli/README

%if %{with_fpm}
%files fpm
%doc php-fpm.conf.default
%doc fpm_LICENSE
%config(noreplace) %{_sysconfdir}/php-fpm.conf
%config(noreplace) %{_sysconfdir}/php-fpm.d/www.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/php-fpm
%config(noreplace) %{_sysconfdir}/sysconfig/php-fpm
%{_prefix}/lib/tmpfiles.d/php-fpm.conf
%{_unitdir}/php-fpm.service
%{_sbindir}/php-fpm
%dir %{_sysconfdir}/php-fpm.d
# log owned by apache for log
%attr(770,apache,root) %dir %{_localstatedir}/log/php-fpm
%dir /run/php-fpm
%{_mandir}/man8/php-fpm.8*
%dir %{_datadir}/fpm
%{_datadir}/fpm/status.html
%endif

%files devel
%{_bindir}/php-config
%{_includedir}/php
%{_libdir}/php/build
%if %{with_zts}
%{_bindir}/zts-php-config
%{_includedir}/php-zts
%{_bindir}/zts-phpize
# usefull only to test other module during build
%{_bindir}/zts-php
%{_libdir}/php-zts/build
%endif
%{_mandir}/man1/php-config.1*
%{_sysconfdir}/rpm/macros.php

%files embedded
%{_libdir}/libphp5.so
%{_libdir}/libphp5-%{embed_version}.so

%files pgsql -f files.pgsql
%if %{with_libmysql}
%files mysql -f files.mysql
%endif
%files odbc -f files.odbc
%files ldap -f files.ldap
%files snmp -f files.snmp
%files xml -f files.xml
%files xmlrpc -f files.xmlrpc
%files mbstring -f files.mbstring
%doc libmbfl_LICENSE
%doc oniguruma_COPYING
%doc ucgendat_LICENSE
%files gd -f files.gd
%doc libgd_README
%doc libgd_COPYING
%files soap -f files.soap
%files bcmath -f files.bcmath
%doc libbcmath_COPYING
%files dba -f files.dba
%files pdo -f files.pdo
%files pspell -f files.pspell
%files intl -f files.intl
%files process -f files.process
%files recode -f files.recode
%files enchant -f files.enchant
%files mysqlnd -f files.mysqlnd


%changelog
* Fri Aug  5 2016 Remi Collet <rcollet@redhat.com> - 5.4.16-42
- bz2: fix improper error handling in bzread() CVE-2016-5399
