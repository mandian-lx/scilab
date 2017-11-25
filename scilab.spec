%define __noautoreq 'libblas.so.3|libatlas.so.3|jaxp_parser_impl'
%define _disable_ld_no_undefined 1

# Disable this to use external scirenderer (still unpackaged)
%bcond_without	scirenderer

Summary:	A high-level language for numerical computations
Name:		scilab
Version:	6.0.0
Release:	0
License:	GPLv2 and BSD
Group:		Sciences/Mathematics
URL:		http://www.scilab.org/
Source0:	http://www.scilab.org/download/%{version}/%{name}-%{version}-src.tar.gz
Source1:	scilabsymbols.ttf
Source20:	scilab.el
Source50:	dot.depend
Source100:	%{name}.rpmlintrc
# (tpg) doc build fails on x86_64 chroot, incerasing java memory heap size should help
#Patch1:	%{name}-5.5.2-increase-java-heap-size.patch
# (tpg) correct LD_PRELOAD
Patch2:		%{name}-5.5.2-fix-ld-preload-paths.patch
# (tpg) add more paths
Patch3:		%{name}-6.0.0-add-more-paths-librarypath.patch
Patch4:		%{name}-6.0.0-fix-type.patch
Patch5:		%{name}-6.0.0-fix-rpath-in-pkgconfig.patch
#Patch6:	%{name}-5.3.3-modelica.patch
# adapted from http://gitweb.scilab.org/?p=scilab.git;a=commitdiff;h=c188bb392d1dd8441d1a4132004f77b63a3353df
Patch100:	scilab-0002-jogl-2.3.2.patch
# adapted from http://gitweb.scilab.org/?p=scilab.git;a=commitdiff;h=962fe026f1c44f7f76435db0b4838b0d936994c8
Patch101:	%{name}-6.0.0-fix-build-with-ocaml-4.0.4.patch
Patch300:	%{name}-6.0.0-port-to-lucene-4.patch
Patch301:	%{name}-6.0.0-port-to-libhdf5-1.10.patch
Patch302:	%{name}-6.0.0-port-to-batik-1.9.patch
Patch303:	%{name}-6.0.0-port-to-lapack-3.6.0.patch

# configure
BuildRequires:  intltool

# compiler
BuildRequires:  gcc-gfortran

# java configuration
BuildRequires:	ant
BuildRequires:	java-rpmbuild
BuildRequires:	java-devel

# core
BuildRequires:	hdf5-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(libpcreposix)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ncurses)

# modelica
BuildRequires:	ocaml

# numerical libraries
BuildRequires:	pkgconfig(arpack)
BuildRequires:	pkgconfig(lapack)

# java dependencies
BuildRequires:  apache-commons-logging
BuildRequires:	ecj
BuildRequires:	flexdock
BuildRequires:	gluegen2
# NOTE: jhall == javahelp2
BuildRequires:	javahelp2
BuildRequires:	jeuclid-core
BuildRequires:	jgoodies-looks
BuildRequires:	jgraphx
BuildRequires:	jlatexmath
BuildRequires:	jogl2
BuildRequires:	jrosetta
BuildRequires:  lucene
BuildRequires:  lucene-analysis
BuildRequires:  lucene-queryparser
BuildRequires:	pkgconfig(gl)
%if %{without scirenderer}
BuildRequires:	scirenderer
%endif

# code quality (optional)
BuildRequires:	antlr-tool
BuildRequires:	apache-commons-beanutils
BuildRequires:	checkstyle
BuildRequires:	cobertura
BuildRequires:	hamcrest12
BuildRequires:	junit

# documentation
BuildRequires:  apache-commons-io
BuildRequires:	avalon-framework
BuildRequires:	batik
BuildRequires:	fop
BuildRequires:	jlatexmath
BuildRequires:	xml-commons-apis
BuildRequires:	xmlgraphics-commons

# documentation build
#BuildRequires:  doxygen
BuildRequires:  docbook-style-xsl
BuildRequires:  fonts-ttf-liberation
BuildRequires:  saxon

# OpenMp
BuildRequires:	libgomp-devel

# TCL/TK
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(x11)

# scirenderer
%if %{with scirenderer}
BuildRequires:	gluegen2
BuildRequires:	jogl2
BuildRequires:	jlatexmath
%endif

# regenerate Scilab's parser
BuildRequires:	byacc
BuildRequires:	flex

# recompile Scilab from scratch
BuildRequires:	giws
BuildRequires:	swig

# optional
BuildRequires:	gettext
BuildRequires:	libxml2-utils
BuildRequires:	jhdf5
BuildRequires:	mpi-devel
BuildRequires:  pkgconfig(eigen3)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(matio)
BuildRequires:	umfpack-devel

# emacs
BuildRequires:	emacs-nox

# packaginh
BuildRequires:	chrpath
BuildRequires:  desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:  appstream-util
#BuildRequires:	python-libxml2
BuildRequires:	valgrind
#BuildRequires:	qdox
#BuildRequires:	pkgconfig(xaw7)
#BuildRequires:	sablotron


BuildConflicts:	termcap-devel

# build of 5.3.3 with 5.3.0 installed fails in doc generation due to not
# finding class org/scilab/forge/scidoc/SciDocMain in call:
# modules/helptools/sci_gateway/cpp/sci_buildDocv2.cpp:
#	doc = new org_scilab_modules_helptools::SciDocMain(getScilabJavaVM());
BuildConflicts:	scilab
# FIXME there should be a better way like some environment variable or
# something to prevent it from using installed scilab files, and should
# have no issues in the build system, so, just add the BuildConflicts
# in case someone tries to rebuild outside of a chroot.
#    echo     "  -nouserstartup  : do not execute the user startup files SCIHOME/.scilab or SCIHOME/scilab.ini."

Requires:	batik
Requires:       bwidget
Requires:	docbook-style-xsl
Requires:	gcc-gfortran
Requires:	ecj
Requires:	flexdock
Requires:	fop
Requires:	gluegen2
Requires:	java > 1.8
Requires:	javahelp2
Requires:	jeuclid-core
Requires:	jgoodies-looks
Requires:	jgraphx
Requires:	jlatexmath
Requires:	jrosetta
Requires:	ocaml
Requires:	sablotron
Requires:	saxon
Requires:	tcl >= 8.5
Requires:	jogl2
Requires:	tk >= 8.5
Requires:	xerces-j2

%description
Scilab is a high-level language, primarily intended for numerical
computations.  Scilab includes a number of toolboxes and on-line
documentation.

%files -f %{name}.lang
%doc ACKNOWLEDGEMENTS CHANGES.md COPYING COPYING-BSD README.md
%config(noreplace) /etc/emacs/site-start.d/%{name}.el
%{_bindir}/*
%{_libdir}/scilab
%{_iconsdir}/hicolor/*/apps/*.png
%{_iconsdir}/hicolor/*/mimetypes/application-x-%{name}-*.png
%{_datadir}/*/site-lisp/*el*
%{_datadir}/applications/*.desktop
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/mime/packages/*.xml
%{_datadir}/%{name}

#---------------------------------------------------------------------------

%package devel
Summary:	Development files for %{name}
Group:		Development/Other

%description devel
Development files and headers for %{name}.

%files devel
%{_includedir}/%{name}
%{_libdir}/pkgconfig/*.pc

#---------------------------------------------------------------------------

%prep
%setup -q

# patch requires .depend
%apply_patches

# .depend is required for autoreconf
cp %{SOURCE50} modules/scicos/.depend

# fix class-path-in-manifest
sed -i -e '/name="Class-Path"/d' build.incl.xml

%build
export JAVA_HOME=%{java_home}

# patched configure.ac
#autoreconf -ifs
autoreconf -fivs

# for openmpi (lapack)
export CC=gcc
export CXX=g++

%configure \
	--disable-static-system-lib \
	--enable-relocatable \
	--without-mpi \
	--without-emf \
	%{nil}

# NOTE: modelica module (ocaml) breaks paralle compilation
make -O all

# documentation
%make doc

# (X)emacs
cp -af %{SOURCE20} .
for i in emacs; do
	$i -batch -q -no-site-file -f batch-byte-compile %{name}.el
	mv %{name}.elc $i-%{name}.elc
done

%install
%makeinstall_std

# (tpg) delete empty dirs
find %{buildroot}%{_datadir}/%{name} -type d -empty -delete

# (X)emacs
for i in emacs; do
	install -dm 0755 %{buildroot}%{_datadir}/$i/site-lisp/
	install -pm 0644 $i-%{name}.elc %{buildroot}%{_datadir}/$i/site-lisp/
	[[ $i = emacs ]] && install -pm 0644 %{name}.el %{buildroot}%{_datadir}/emacs/site-lisp/
done
install -dm 0755 %{buildroot}/%{_sysconfdir}/emacs/site-start.d
install -pm 0644 %{SOURCE20} %{buildroot}/%{_sysconfdir}/emacs/site-start.d/%{name}.el

# (tpg) correct path for *.so java libraries
sed -i -e 's#/usr/lib/jni/#%{_libdir}#g' %{buildroot}%{_datadir}/%{name}/etc/librarypath.xml

# (tpg) fonts
install -dm 0755 %{buildroot}%{_datadir}/%{name}/thirdparty/fonts
install -pm 0644 %{SOURCE1} %{buildroot}%{_datadir}/%{name}/thirdparty/fonts/

# (tpg) nuke rpath
# intersci
for file in %{buildroot}%{_bindir}/{scilab-bin,scilab-cli-bin}; do \
    chrpath -d $file; \
done

# (tpg) get rid of files with licenses
rm %{buildroot}%{_datadir}/%{name}/modules/*/license.txt
rm %{buildroot}%{_datadir}/%{name}/contrib/toolbox_skeleton/license.txt 
rm %{buildroot}%{_datadir}/%{name}/modules/tclsci/tcl/sciGUI/license.txt
rm %{buildroot}%{_datadir}/%{name}/modules/umfpack/TAUCS_license.txt 
rm %{buildroot}%{_datadir}/%{name}/modules/umfpack/UMFPACK_license.txt

# locales
%find_lang %{name}

%check
%make check-TESTS || true

# .desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

# .appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml

