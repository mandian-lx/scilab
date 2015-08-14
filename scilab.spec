%define __noautoreq 'libblas.so.3|jaxp_parser_impl'

Summary:	A high-level language for numerical computations
Name:		scilab
Version:	5.5.2
Release:	1
License:	CeCILL
Group:		Sciences/Mathematics
URL:		http://www.scilab.org/
Source0:	http://www.scilab.org/download/%{version}/%{name}-%{version}-src.tar.xz
Source1:	scilabsymbols.ttf
Source20:	scilab.el
# (tpg) doc build fails on x86_64 chroot, incerasing java memory heap size should help
Patch1:		%{name}-5.5.2-increase-java-heap-size.patch
# (tpg) correct LD_PRELOAD
Patch2:		%{name}-5.5.2-fix-ld-preload-paths.patch
# (tpg) add more paths
Patch3:		%{name}-5.5.2-add-more-paths-librarypath.patch
Patch6:		%{name}-5.3.3-modelica.patch
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	tcl-devel >= 8.5
BuildRequires:	tk-devel >= 8.5
BuildRequires:	xaw-devel
BuildRequires:	emacs-nox
BuildRequires:	gcc-gfortran
BuildRequires:	pkgconfig(gl)
BuildRequires:	libgomp-devel
BuildRequires:	ocaml
BuildRequires:	imagemagick
BuildRequires:	sablotron
BuildRequires:	lapack-devel
BuildRequires:	fftw3-devel
BuildRequires:	java-rpmbuild
BuildRequires:	ant
BuildRequires:	checkstyle
BuildRequires:	flexdock
BuildRequires:	jgoodies-looks
BuildRequires:	umfpack-devel
BuildRequires:	jogl2
# jhall == javahelp2
BuildRequires:	javahelp2
BuildRequires:	gluegen2
BuildRequires:	jrosetta
BuildRequires:	matio-devel
BuildRequires:	swig
BuildRequires:	ncurses-devel
BuildRequires:	pcre-devel
BuildRequires:	giws
BuildRequires:	docbook-style-xsl
BuildRequires:	batik
BuildRequires:	saxon
BuildRequires:	fop
BuildRequires:	jeuclid-core
BuildRequires:	python-libxml2
BuildRequires:	qdox
BuildRequires:	suitesparse-common-devel
BuildRequires:	xml-commons-apis
BuildRequires:	jgraphx
BuildRequires:	jlatexmath
BuildRequires:	antlr
BuildRequires:	jakarta-commons-beanutils
BuildRequires:	chrpath
BuildRequires:	hdf-java
BuildRequires:	hdf5-devel
BuildRequires:	xmlgraphics-commons
BuildRequires:	pkgconfig(arpack)
BuildConflicts:	termcap-devel
#BuildConflicts:	junit

# build of 5.3.3 with 5.3.0 installed fails in doc generation due to not
# finding class org/scilab/forge/scidoc/SciDocMain in call:
# modules/helptools/sci_gateway/cpp/sci_buildDocv2.cpp:
#	doc = new org_scilab_modules_helptools::SciDocMain(getScilabJavaVM());
BuildConflicts:	scilab
# FIXME there should be a better way like some environment variable or
# something to prevent it from using installed scilab files, and should
# have no issues in the build system, so, just add the BuildConflicts
# in case someone tries to rebuild outside of a chroot.

Requires:	arpack
Requires:	tcl >= 8.5
Requires:	tk >= 8.5
Requires:	ocaml
Requires:	gcc-gfortran
Requires:	flexdock
Requires:	jgoodies-looks
Requires:	jogl2
Requires:	jrosetta
Requires:	gluegen2
Requires:	javahelp2
Requires:	fop
Requires:	saxon
Requires:	batik
Requires:	jeuclid-core
Requires:	java > 1.5
Requires:	xerces-j2
Requires:	liblapack
Requires:	libblas
Requires:	fftw
Requires:	libmatio
Requires:	docbook-style-xsl
Requires:	swig
Requires:	giws
Requires:	sablotron
Requires:	jgraphx
Requires:	jlatexmath
Requires:	hdf-java
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Scilab is a high-level language, primarily intended for numerical
computations.  Scilab includes a number of toolboxes and on-line
documentation.

%package devel
Summary:	Development files for %{name}
Group:		Development/Other

%description devel
Development files and headers for %{name}.

%prep
%setup -q
%apply_patches

%build
%define _disable_ld_no_undefined 1
export LDFLAGS="%{ldflags} -Wl,--no-as-needed"
%define Werror_cflags %nil
export JAVA_HOME=%{java_home}

# patched configure.ac
# autoreconf -ifs

%configure2_5x \
	--with-tk-library=%{_libdir} \
	--with-tcl-library=%{_libdir} \
	--with-blas-library=%{_libdir} \
	--with-lapack-library=%{_libdir} \
	--with-jdk=%{java_home} \
	--disable-rpath \
	--without-emf \
	--without-umfpack \
	--enable-shared \
	--disable-static \
	--disable-static-system-lib \
	--with-gfortran \
	--with-gcc \
	--with-fftw \
	--enable-build-localization \
	--enable-build-help \
	--with-docbook="/usr/share/sgml/docbook/xsl-stylesheets-1.76.1" \
	--enable-build-swig \
	--enable-build-giws \
	--with-install-help-xml \
	--with-gui \
	--enable-relocatable

%make all
%make doc

cp -af %{SOURCE20} .
for i in emacs; do
	$i -batch -q -no-site-file -f batch-byte-compile %{name}.el
	mv %{name}.elc $i-%{name}.elc
done

%install
%makeinstall_std

# (tpg) delete empty dirs
find %{buildroot}%{_datadir}/%{name} -type d -empty -delete

# Icons
for i in "16x16" "32x32" "48x48"; do
    mkdir -p %{buildroot}%{_iconsdir}/hicolor/$i/apps
    convert desktop/%{name}.xpm -geometry $i %{buildroot}%{_iconsdir}/hicolor/$i/apps/%{name}.png ;
done

# (tpg) get rid of this
rm %{buildroot}%{_datadir}/%{name}/README_Windows.txt

# Menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Scilab
Comment=High-level language for numerical computations
Exec=scilab
Icon=scilab
Terminal=false
Type=Application
Categories=Science;Math;
EOF

# (X)emacs
for i in emacs; do
	mkdir -p %{buildroot}%{_datadir}/$i/site-lisp/
	mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp/
	install -m644 $i-%{name}.elc %{buildroot}%{_datadir}/$i/site-lisp/
	[[ $i = emacs ]] && install -m644 %{name}.el %{buildroot}%{_datadir}/emacs/site-lisp/
done

mkdir -p %{buildroot}/%{_sysconfdir}/emacs/site-start.d
install -m644 %{SOURCE20} %{buildroot}/%{_sysconfdir}/emacs/site-start.d/%{name}.el

# (tpg) correct path for *.so java libraries
sed -i -e 's#/usr/lib/jni/#%{_libdir}#g' %{buildroot}%{_datadir}/%{name}/etc/librarypath.xml

# (tpg) fonts
mkdir -p %{buildroot}%{_datadir}/%{name}/thirdparty/fonts
install -m644 %{SOURCE1} %{buildroot}%{_datadir}/%{name}/thirdparty/fonts/

# (tpg) nuke rpath
for file in %{buildroot}%{_bindir}/{intersci,scilab-bin,scilab-cli-bin}; do \
    chrpath -d $file; \
done

# (tpg) get rid of files with licenses
rm %{buildroot}%{_datadir}/%{name}/modules/*/license.txt
rm %{buildroot}%{_datadir}/%{name}/contrib/toolbox_skeleton/license.txt 
rm %{buildroot}%{_datadir}/%{name}/modules/tclsci/tcl/BWidget-*/LICENSE.txt
rm %{buildroot}%{_datadir}/%{name}/modules/tclsci/tcl/sciGUI/license.txt
rm %{buildroot}%{_datadir}/%{name}/modules/umfpack/TAUCS_license.txt 
rm %{buildroot}%{_datadir}/%{name}/modules/umfpack/UMFPACK_license.txt

%find_lang %{name}


%files -f %{name}.lang
%doc ACKNOWLEDGEMENTS CHANGES_5.3.X license.txt RELEASE_NOTES_5.3.X README_Unix
%{_bindir}/*
%{_libdir}/scilab
%{_iconsdir}/hicolor/*/*/%{name}.png
%config(noreplace) /etc/emacs/site-start.d/%{name}.el
%{_datadir}/*/site-lisp/*el*
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}

%files devel
%{_includedir}/%{name}
%{_libdir}/pkgconfig/*.pc
