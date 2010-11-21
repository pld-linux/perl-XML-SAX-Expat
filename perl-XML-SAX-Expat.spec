#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%include	/usr/lib/rpm/macros.perl
%define		pdir	XML
%define		pnam	SAX-Expat
Summary:	XML::SAX::Expat - SAX2 driver for Expat (XML::Parser)
Summary(pl.UTF-8):	XML::SAX::Expat - sterownik SAX2 dla modułu Expat (XML::Parser)
Name:		perl-XML-SAX-Expat
Version:	0.40
Release:	2
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/XML/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	ca58d1e26c437b31c52456b4b4ae5c4a
URL:		http://search.cpan.org/dist/XML-SAX-Expat/
BuildRequires:	perl(XML::SAX::Base) >= 1.00
BuildRequires:	perl-XML-NamespaceSupport >= 0.03
BuildRequires:	perl-XML-Parser >= 2.27
BuildRequires:	perl-XML-SAX >= 0.03
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an implementation of a SAX2 driver sitting on top of Expat
(XML::Parser).

%description -l pl.UTF-8
To jest implementacja sterownika SAX2 w oparciu o moduł Expat
(XML::Parser).

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

# we want to add_parser in post, not on make install
head -n 23 Makefile.PL > Makefile.PL.tmp
mv -f Makefile.PL.tmp Makefile.PL

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
%{__perl} -MXML::SAX -e "XML::SAX->add_parser(q(XML::SAX::Expat))->save_parsers()"

%postun
if [ "$1" = "0" ] && [ -x %{__perl} ]; then
	umask 022
	%{__perl} -MXML::SAX -e "XML::SAX->remove_parser(q(XML::SAX::Expat))->save_parsers()"
fi

%files
%defattr(644,root,root,755)
%doc Changes
%{perl_vendorlib}/XML/SAX/Expat.pm
%{_mandir}/man3/*
