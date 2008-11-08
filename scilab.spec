%define flavor emacs
%define	pvmlib %{_datadir}/pvm3/lib

Summary: A high-level language for numerical computations
Name:	 scilab
Version: 5.0.3
Release: %mkrel 1
License: SCILAB
Group: Sciences/Mathematics
Source0: http://www.scilab.org/download/%{version}/%{name}-%{version}-src.tar.gz
Source20: scilab.el
Patch1:	0001-UseStandardXaw.patch
Patch2: 0002-file-menu.patch
# Fixes: scilab broken : missing symlink and error message
# https://qa.mandriva.com/show_bug.cgi?id=40116
Patch3: 0003-scipad.diff
# Fixes: scilab crashed when trying export graph
# https://qa.mandriva.com/show_bug.cgi?id=40910
Patch4: 0004-Xdefaults.patch
Patch5:	scilab-5.0.3-find-jgoodies-looks.patch
URL: http://www.scilab.org/
BuildRequires:	perl
BuildRequires:	vte-devel
BuildRequires:	tcl-devel >= 8.5
BuildRequires:	tk-devel >= 8.5
BuildRequires:	xaw-devel
BuildRequires:	emacs-nox
BuildRequires:	libgcj-devel
BuildRequires:	gcc-gfortran
BuildRequires:	gcc-java
BuildRequires:	ocaml
BuildRequires:	imagemagick
BuildRequires:	sablotron
BuildRequires:	libpvm-devel
BuildRequires:	blas-devel
BuildRequires:	lapack-devel
BuildRequires:	fftw3-devel
BuildRequires:	java-rpmbuild
BuildRequires:	ant
BuildRequires:	flexdock
BuildRequires:	jgoodies-looks
BuildRequires:	umfpack-devel
BuildRequires:	jogl
Requires:	tcl >= 8.5
Requires:	tk >= 8.5
Requires:	pvm
Requires:	ocaml
Requires:	gcc-gfortran
Requires:	jogl
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Scilab is a high-level language, primarily intended for numerical
computations.  Scilab includes a number of toolboxes and on-line
documentation.

%prep
rm -rf %{buildroot}
%setup -q 

#%patch1 -p1 -b .xaw
#%patch2 -p1 -b .filemenu
#%patch3 -p1 -b .scipad
#%patch4 -p1 -b .xdefaults
%patch5 -p0

%build
export JAVA_HOME="%{java_home}"

%configure2_5x \
	--with-tk-library=%{_libdir} \
	--with-tcl-library=%{_libdir} \
	--with-pvm-library=%{pvmlib}/`%{pvmlib}/pvmgetarch` \
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
	--enable-build-swig \
	--enable-build-giws
	

# fix java include path
perl -pi -e "s/JAVAINC=.*/JAVAINC=/" routines/Javasci/Makefile

%make

cp -af %SOURCE20 .
for i in %{flavor};do
	$i -batch -q -no-site-file -f batch-byte-compile %{name}.el
	mv %{name}.elc $i-%{name}.elc
done

%install
rm -rf %{buildroot}
install -d -m0755 %{buildroot}%{_bindir}
install -d -m0755 %{buildroot}%{_libdir}
perl -pi.orig -e '
		s|/usr/bin|%{buildroot}%{_bindir}|g;
		s|/usr/lib|%{buildroot}%{_libdir}|g;
		s|ln -fs \$\(PREFIX\)/lib|ln -fs %{_libdir}|g;
		s|$\(PREFIX\)/)lib|$1%{_lib}|g;
	' Makefile

perl -pi -e 's|/bin/sh5|/bin/sh|g;' bin/dold
make install PREFIX="%{buildroot}%{_prefix}" LIBPREFIX="%{buildroot}%{_libdir}"

# Duplicated documentation
rm -fr %{buildroot}/%{_defaultdocdir}/%{name}-%{version}

perl -pi -e ' s|%{buildroot}||g;' %{buildroot}%{_libdir}/scilab-%{version}/bin/*

# Icons
install -d %{buildroot}/%{_miconsdir}
install -d %{buildroot}/%{_liconsdir}
convert X11_defaults/%{name}.xpm -geometry 48x48 %{buildroot}%{_liconsdir}/%{name}.png
convert X11_defaults/%{name}.xpm -geometry 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert X11_defaults/%{name}.xpm -geometry 16x16 %{buildroot}%{_miconsdir}/%{name}.png

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
Categories=X-MandrivaLinux-MoreApplications-Sciences-Mathematics;
EOF


# (X)emacs
for i in %{flavor};do
	mkdir -p %{buildroot}%{_datadir}/$i/site-lisp/
	mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp/
	install -m644 $i-%{name}.elc %{buildroot}%{_datadir}/$i/site-lisp/
	[[ $i = emacs ]] && install -m644 %{name}.el %{buildroot}%{_datadir}/emacs/site-lisp/
done

mkdir -p %{buildroot}/%{_sysconfdir}/emacs/site-start.d
install -m644 %{SOURCE20} %{buildroot}/%{_sysconfdir}/emacs/site-start.d/%{name}.el

# Links libtk8.5.so.0 to scilab's bindir to avoid runtime warnings about
# devel files not installed
ln -sf %{_libdir}/libtk8.5.so.0 %{buildroot}/%{_libdir}/%{name}-%{version}/bin/libtk8.5.so

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

%files
%defattr(-,root,root)
%doc ACKNOWLEDGEMENTS CHANGES license.txt licence.txt
%{_bindir}/*
%{_libdir}/scilab-*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%config(noreplace) /etc/emacs/site-start.d/%{name}.el
%{_datadir}/*/site-lisp/*el*
%{_datadir}/applications/*
