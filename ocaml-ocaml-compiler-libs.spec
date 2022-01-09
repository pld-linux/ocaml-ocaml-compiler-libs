# TODO: docs using ocaml-odoc
#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	ocaml-compiler-libs
Summary:	OCaml compiler libraries repackaged
Summary(pl.UTF-8):	Przepakowane biblioteki kompilatora OCamla
# Yes, double "ocaml-": first is standard prefix for ocaml libraries, the second is a part of original library name;
# ocaml-library-libs package name is already occupied by "compiler-libs" ocaml library packaged in ocaml.spec
Name:		ocaml-ocaml-compiler-libs
Version:	0.12.4
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/janestreet/ocaml-compiler-libs/releases
Source0:	https://github.com/janestreet/ocaml-compiler-libs/releases/download/v%{version}/ocaml-compiler-libs-v%{version}.tbz
# Source0-md5:	db4698885b07bc848684f727625d7c55
URL:		https://github.com/janestreet/ocaml-compiler-libs
BuildRequires:	ocaml >= 1:4.04.1
BuildRequires:	ocaml-dune >= 2.8
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
This library exposes the OCaml compiler libraries repackaged under
the toplevel names Ocaml_common, Ocaml_bytecomp, Ocaml_optcomp...

This package contains files needed to run bytecode executables using
ocaml-compiler-libs library.

%description -l pl.UTF-8
Ta biblioteka udostępnia biblioteki kompilatora OCamla przepakowane
pod nazwami głównego poziomu Ocaml_common, Ocaml_bytecomp,
Ocaml_optcomp...

Ten pakiet zawiera binaria potrzebne do uruchamiania programów
używających biblioteki ocaml-compiler-libs.

%package devel
Summary:	ocaml-compiler-libs binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania ocaml-compiler-libs dla OCamla - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
ocaml-compiler-libs library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki ocaml-compiler-libs.

%prep
%setup -q -n ocaml-compiler-libs-v%{version}

%if %{without ocaml_opt}
# %{_libdir}/ocaml/compiler-libs/ocamloptcomp.cma not available
%{__rm} src/ocaml_optcomp/dune
%endif

%build
dune build --verbose

%install
rm -rf $RPM_BUILD_ROOT

dune install --destdir=$RPM_BUILD_ROOT

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/ocaml-compiler-libs/*/*.ml
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/ocaml-compiler-libs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE.md README.org
%dir %{_libdir}/ocaml/ocaml-compiler-libs
%{_libdir}/ocaml/ocaml-compiler-libs/META
%dir %{_libdir}/ocaml/ocaml-compiler-libs/bytecomp
%dir %{_libdir}/ocaml/ocaml-compiler-libs/common
%dir %{_libdir}/ocaml/ocaml-compiler-libs/shadow
%dir %{_libdir}/ocaml/ocaml-compiler-libs/toplevel
%{_libdir}/ocaml/ocaml-compiler-libs/bytecomp/*.cma
%{_libdir}/ocaml/ocaml-compiler-libs/common/*.cma
%{_libdir}/ocaml/ocaml-compiler-libs/shadow/*.cma
%{_libdir}/ocaml/ocaml-compiler-libs/toplevel/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/ocaml-compiler-libs/bytecomp/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/ocaml-compiler-libs/common/*.cmxs
%dir %{_libdir}/ocaml/ocaml-compiler-libs/optcomp
%{_libdir}/ocaml/ocaml-compiler-libs/optcomp/*.cma
%attr(755,root,root) %{_libdir}/ocaml/ocaml-compiler-libs/optcomp/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/ocaml-compiler-libs/shadow/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/ocaml-compiler-libs/toplevel/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/ocaml-compiler-libs/dune-package
%{_libdir}/ocaml/ocaml-compiler-libs/opam
%{_libdir}/ocaml/ocaml-compiler-libs/bytecomp/*.cmi
%{_libdir}/ocaml/ocaml-compiler-libs/bytecomp/*.cmt
%{_libdir}/ocaml/ocaml-compiler-libs/common/*.cmi
%{_libdir}/ocaml/ocaml-compiler-libs/common/*.cmt
%{_libdir}/ocaml/ocaml-compiler-libs/shadow/*.cmi
%{_libdir}/ocaml/ocaml-compiler-libs/shadow/*.cmt
%{_libdir}/ocaml/ocaml-compiler-libs/toplevel/*.cmi
%{_libdir}/ocaml/ocaml-compiler-libs/toplevel/*.cmt
%if %{with ocaml_opt}
%{_libdir}/ocaml/ocaml-compiler-libs/bytecomp/*.a
%{_libdir}/ocaml/ocaml-compiler-libs/bytecomp/*.cmx
%{_libdir}/ocaml/ocaml-compiler-libs/bytecomp/*.cmxa
%{_libdir}/ocaml/ocaml-compiler-libs/common/*.a
%{_libdir}/ocaml/ocaml-compiler-libs/common/*.cmx
%{_libdir}/ocaml/ocaml-compiler-libs/common/*.cmxa
%{_libdir}/ocaml/ocaml-compiler-libs/optcomp/*.a
%{_libdir}/ocaml/ocaml-compiler-libs/optcomp/*.cmi
%{_libdir}/ocaml/ocaml-compiler-libs/optcomp/*.cmt
%{_libdir}/ocaml/ocaml-compiler-libs/optcomp/*.cmx
%{_libdir}/ocaml/ocaml-compiler-libs/optcomp/*.cmxa
%{_libdir}/ocaml/ocaml-compiler-libs/shadow/*.a
%{_libdir}/ocaml/ocaml-compiler-libs/shadow/*.cmx
%{_libdir}/ocaml/ocaml-compiler-libs/shadow/*.cmxa
%{_libdir}/ocaml/ocaml-compiler-libs/toplevel/*.a
%{_libdir}/ocaml/ocaml-compiler-libs/toplevel/*.cmx
%{_libdir}/ocaml/ocaml-compiler-libs/toplevel/*.cmxa
%endif
