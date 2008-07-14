#Module-Specific definitions
%define mod_name mod_gzip_disk
%define mod_conf B29_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Serves pre-compressed HTML files to avoid compression on the fly
Name:		apache-%{mod_name}
Version:	0.03
Release:	%mkrel 4
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod-gzip-disk is a module for serving pre-compressed HTML files to clients to
avoid compression on the fly.

%prep

%setup -q -n %{mod_name}
cp %{SOURCE1} .

%build

%{_sbindir}/apxs -c %{mod_name}.c -lz

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

