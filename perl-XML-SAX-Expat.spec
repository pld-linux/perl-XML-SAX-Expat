#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	XML
%define	pnam	SAX-Expat
Summary:	XML::SAX::Expat - SAX2 driver for Expat (XML::Parser)
Summary(pl):	XML::SAX::Expat - sterownik SAX2 dla modu³u Expat (XML::Parser)
Name:		perl-XML-SAX-Expat
Version:	0.37
Release:	1
# same as perl
License:	GPL or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	c48024d363a1ff9abaf8f9af592d38cd
BuildRequires:	perl-XML-NamespaceSupport >= 0.03
BuildRequires:	perl-XML-Parser >= 2.27
BuildRequires:	perl-XML-SAX >= 0.03
BuildRequires:	perl(XML::SAX::Base) >= 1.00
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an implementation of a SAX2 driver sitting on top of Expat
(XML::Parser).

%description -l pl
To jest implementacja sterownika SAX2 w oparciu o modu³ Expat
(XML::Parser).

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

# we want to add_parser in post, not on make install
head -n 16 Makefile.PL > Makefile.PL.tmp
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
if [ "$1" = "0" ]; then
	umask 022
	%{__perl} -MXML::SAX -e "XML::SAX->remove_parser(q(XML::SAX::Expat))->save_parsers()"
fi

%files
%defattr(644,root,root,755)
%doc Changes
%{perl_vendorlib}/XML/SAX/Expat.pm
%{_mandir}/man3/*
