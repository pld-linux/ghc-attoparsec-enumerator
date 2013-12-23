#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	attoparsec-enumerator
Summary:	Pass input from an enumerator to an Attoparsec parser
Summary(pl.UTF-8):	Przekazywanie wejścia z enumeratora do analizatora Attoparsec
Name:		ghc-%{pkgname}
Version:	0.3.1
Release:	2
License:	MIT
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/attoparsec-enumerator
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	6748ce61ed642c0cf95d246075d42282
URL:		http://hackage.haskell.org/package/attoparsec-enumerator
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-attoparsec >= 0.10
BuildRequires:	ghc-attoparsec < 0.11
BuildRequires:	ghc-base >= 4.0
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-enumerator >= 0.4
BuildRequires:	ghc-enumerator < 0.5
BuildRequires:	ghc-text
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-attoparsec-prof >= 0.10
BuildRequires:	ghc-attoparsec-prof < 0.11
BuildRequires:	ghc-base-prof >= 4.0
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-enumerator-prof >= 0.4
BuildRequires:	ghc-enumerator-prof < 0.5
BuildRequires:	ghc-text-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_releq	ghc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This library allows an Attoparsec parser to receive input
incrementally from an enumerator. This could be used for parsing
large files, or implementing binary network protocols.

%description -l pl.UTF-8
Ta biblioteka pozwala analizatorowi Attoparsec odbierać dane wejściowe
przyrostowo od enumeratora. Jest to przydatne na przykład przy
analizie dużych plików lub implementowaniu binarnych protokołów
sieciowych.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSattoparsec-enumerator-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSattoparsec-enumerator-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSattoparsec-enumerator-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/*.p_hi
%endif
