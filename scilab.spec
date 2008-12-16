%define _requires_exceptions libblas.so.3\\|jaxp_parser_impl\\|

Summary:	A high-level language for numerical computations
Name:		scilab
Version:	5.0.3
Release:	%mkrel 11
License:	CeCILL
Group:		Sciences/Mathematics
URL:		http://www.scilab.org/
Source0:	http://www.scilab.org/download/%{version}/%{name}-%{version}-src.tar.gz
Source1:	scilabsymbols.ttf
Source2:	scilab_fr_FR_help.jar
Source3:	scilab_en_US_help.jar
Source20:	scilab.el
Patch1:		0001-UseStandardXaw.patch
Patch2:		0002-file-menu.patch
# Fixes: scilab broken : missing symlink and error message
# https://qa.mandriva.com/show_bug.cgi?id=40116
Patch3:		0003-scipad.diff
# Fixes: scilab crashed when trying export graph
# https://qa.mandriva.com/show_bug.cgi?id=40910
Patch4:		0004-Xdefaults.patch
Patch5:		%{name}-5.0.3-find-jgoodies-looks.patch
Patch6:		%{name}-5.0.3-find-jhall.patch
Patch7:		%{name}-5.0.3-find-batik.patch
Patch8:		%{name}-5.0.3-find-jeuclid-core.patch
Patch9:		%{name}-5.0.3-adapt-to-newer-jeuclid-core.patch
# Kludge (not fix) build for Tcl 8.6 (interp->result usage, TIP #330)
# - AdamW 2008/12
Patch10:	%{name}-5.0.3-tcl86.patch
Patch11:	%{name}-5.0.3-jre-path.patch
# (tpg) scilab tries to link against devel library libfftw.so instead of libfftw3.so.3, this patch fixes this
Patch12:	%{name}-5.0.3-link-against-main-libfftw3-library.patch
Patch13:	%{name}-5.0.3-correct-LD_LIBRARY_PATH.patch
BuildRequires:	tcl-devel >= 8.5
BuildRequires:	tk-devel >= 8.5
BuildRequires:	xaw-devel
BuildRequires:	emacs-nox
BuildRequires:	gcc-gfortran
BuildRequires:	ocaml
BuildRequires:	imagemagick
BuildRequires:	sablotron
BuildRequires:	blas-devel
BuildRequires:	lapack-devel
BuildRequires:	fftw3-devel
BuildRequires:	java-rpmbuild
BuildRequires:	ant
BuildRequires:	flexdock
BuildRequires:	jgoodies-looks
BuildRequires:	umfpack-devel
BuildRequires:	jogl
# jhall == javahelp2
BuildRequires:	javahelp2
BuildRequires:	gluegen
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
BuildRequires:	suitesparse-common-devel
Requires:	tcl >= 8.5
Requires:	tk >= 8.5
Requires:	ocaml
Requires:	gcc-gfortran
Requires:	flexdock
Requires:	jgoodies-looks
Requires:	jogl
Requires:	jrosetta
Requires:	gluegen
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
Requires:	libumfpack
Requires:	docbook-style-xsl
Requires:	swig
Requires:	giws
Requires:	sablotron
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

#%patch1 -p1 -b .xaw
#%patch2 -p1 -b .filemenu
#%patch3 -p1 -b .scipad
#%patch4 -p1 -b .xdefaults
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p0
%patch9 -p1
%patch10 -p1 -b .tcl86
%patch11 -p0
%patch12 -p0
%patch13 -p0

%build
%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed 1
%define Werror_cflags %nil
export JAVA_HOME=%{java_home}

#(tpg) without this hack scilab fails if compiled with macro for configure script
sed -i -e 's/#undef exp10//g' modules/core/includes/machine.h.in

#(tpg) fix giws filename
sed -i -e 's/giws.py/giws/g' configure

# (tpg) get rid of double shalshes in path
sed -i -e 's#/usr/share/java/#/usr/share/java#g' -e 's#/usr/lib/java/#/usr/lib/java#g' configure

%configure2_5x \
	--with-tk-library=%{_libdir} \
	--with-tcl-library=%{_libdir} \
	--with-blas-library=%{_libdir} \
	--with-lapack-library=%{_libdir} \
	--with-jdk=%{java_home} \
	--with-umfpack \
	--enable-shared \
	--disable-static \
	--with-gfortran \
	--with-gcc \
	--with-ocaml \
	--with-fftw \
	--enable-build-localization \
	--enable-build-help \
	--with-docbook="/usr/share/sgml/docbook/xsl-stylesheets-1.73.2" \
	--enable-build-swig \
	--enable-build-giws \
	--with-install-help-xml

%make

cp -af %{SOURCE20} .
for i in emacs; do
	$i -batch -q -no-site-file -f batch-byte-compile %{name}.el
	mv %{name}.elc $i-%{name}.elc
done

%install
rm -rf %{buildroot}
%makeinstall_std

# Icons
for i in "16x16" "32x32" "48x48"; do
    mkdir -p %{buildroot}%{_iconsdir}/hicolor/$i/apps
    convert X11_defaults/%{name}.xpm -geometry $i %{buildroot}%{_iconsdir}/hicolor/$i/apps/%{name}.png ;
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

# (tpg) help files
install -m644 %{SOURCE2} %{buildroot}%{_datadir}/%{name}/modules/helptools/jar/
install -m644 %{SOURCE3} %{buildroot}%{_datadir}/%{name}/modules/helptools/jar/

%find_lang %{name}

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc ACKNOWLEDGEMENTS CHANGES_5.0.X license.txt RELEASE_NOTES README_Unix
%{_bindir}/*
%{_libdir}/scilab
%{_iconsdir}/hicolor/*/*/%{name}.png
%config(noreplace) /etc/emacs/site-start.d/%{name}.el
%{_datadir}/*/site-lisp/*el*
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}
%{_libdir}/pkgconfig/*.pc
