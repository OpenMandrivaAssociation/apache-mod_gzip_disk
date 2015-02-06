#Module-Specific definitions
%define mod_name mod_gzip_disk
%define mod_conf B29_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Serves pre-compressed HTML files to avoid compression on the fly
Name:		apache-%{mod_name}
Version:	0.5
Release:	7
Group:		System/Servers
License:	Apache License
URL:		http://www.s5h.net/code/mod-gzip/
Source0:	http://www.s5h.net/code/mod-gzip/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:  apache-devel >= 2.2.0

%description
mod-gzip-disk is a module for serving pre-compressed HTML files to clients to
avoid compression on the fly.

%prep

%setup -q -n %{mod_name}

cp %{SOURCE1} .

%build

%{_bindir}/apxs -c %{mod_name}.c -lz

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}



%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.5-6mdv2012.0
+ Revision: 772663
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.5-5
+ Revision: 678322
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5-4mdv2011.0
+ Revision: 588006
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5-3mdv2010.1
+ Revision: 516124
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.5-2mdv2010.0
+ Revision: 406593
- rebuild

* Sun Jun 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.5-1mdv2010.0
+ Revision: 387701
- 0.5

* Wed Jan 07 2009 Oden Eriksson <oeriksson@mandriva.com> 0.03-5mdv2009.1
+ Revision: 326491
- fix build with -Werror=format-security

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.03-4mdv2009.0
+ Revision: 234957
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.03-3mdv2009.0
+ Revision: 215585
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 0.03-2mdv2008.1
+ Revision: 181756
- rebuild

* Wed Feb 13 2008 Oden Eriksson <oeriksson@mandriva.com> 0.03-1mdv2008.1
+ Revision: 167137
- import apache-mod_gzip_disk


* Wed Feb 13 2008 Oden Eriksson <oeriksson@mandriva.com> 0.03-1mdv2008.1
- initial Mandriva package
