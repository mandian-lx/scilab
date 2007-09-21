%define flavor emacs

Summary: A high-level language for numerical computations
Name:	 scilab
Version: 4.1.1
Release: %mkrel 1
License: SCILAB
Group: Sciences/Mathematics
Source0: http://www.scilab.org/download/%{version}/%{name}-%{version}-src.tar.gz
Source20: scilab.el
Patch1:	0001-UseStandardXaw.patch
URL: http://www.scilab.org/
BuildRequires: perl tcl-devel tk-devel vte-devel 
BuildRequires: emacs-nox libgcj-devel gcc3.3-g77
BuildRequires: gcc-java ocaml
BuildRequires: ImageMagick sablotron
BuildRequires: libpvm-devel 
Requires: pvm tcl tk gcc-gfortran
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
Scilab is a high-level language, primarily intended for numerical
computations.  Scilab includes a number of toolboxes and on-line
documentation.

%prep
rm -rf %{buildroot}
%setup -q 

%patch1 -p1 -b .xaw

%build
%configure2_5x	\
	--enable-shared \
	--with-g77 \
	--with-java \
	--enable-static=no

# fix java include path
perl -pi -e "s/JAVAINC=.*/JAVAINC=/" routines/Javasci/Makefile

make all

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
install -d %{buildroot}/%{_menudir}
cat << EOF > %{buildroot}/%{_menudir}/%{name}
?package(%{name}):command="%{_bindir}/%{name}" icon="%{name}.png" \
                needs="X11" section="More Applications/Sciences/Mathematics" \
		title="Scilab" \
                longtitle="Environment for numerical computations" \
		xdg="true"
EOF

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

%post
%{update_menus}

%postun
%{clean_menus}


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ACKNOWLEDGEMENTS CHANGES license.txt licence.txt
%_bindir/*
%_libdir/scilab-*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_menudir}/%{name}
%config(noreplace) /etc/emacs/site-start.d/%{name}.el
%{_datadir}/*/site-lisp/*el*
%_datadir/applications/*

