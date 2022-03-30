#
# Conditional build:
%bcond_without	doc		# Sphinx documentation
%bcond_with	tests		# test target [fails on one wheel/wsgi test]
%bcond_with	bootstrap	# disable tests for bootstrap (circular build dependencies)
%bcond_without	python2	 	# CPython 2.x module
%bcond_without	python3		# CPython 3.x module

%if %{with bootstrap}
%undefine	with_tests
%undefine	with_doc
%endif
%define 	module	pbr
Summary:	Python Build Reasonableness
Summary(pl.UTF-8):	Python Build Reasonableness - rozsądne budowanie modułów pythonowych
Name:		python-%{module}
Version:	5.8.1
Release:	4
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pbr/
Source0:	https://files.pythonhosted.org/packages/source/p/pbr/%{module}-%{version}.tar.gz
# Source0-md5:	9ab99a85202af94990ef44ebcd2bf196
URL:		https://launchpad.net/pbr
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
%if %{with tests}
BuildRequires:	python-coverage >= 4.0
BuildRequires:	python-fixtures >= 3.0.0
BuildRequires:	python-mock >= 2.0.0
BuildRequires:	python-reno >= 2.5.0
BuildRequires:	python-six >= 1.12.0
BuildRequires:	python-stestr >= 2.1.0
BuildRequires:	python-testrepository >= 0.0.18
BuildRequires:	python-testresources >= 2.0.0
BuildRequires:	python-testscenarios >= 0.4
BuildRequires:	python-testtools >= 2.2.0
BuildRequires:	python-virtualenv >= 20.0.3
BuildRequires:	python-wheel >= 0.32.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.5
%if %{with tests}
BuildRequires:	python3-coverage >= 4.0
BuildRequires:	python3-fixtures >= 3.0.0
%if "%{py3_ver}" >= "3.6"
BuildRequires:	python3-hacking >= 1.1.0
BuildRequires:	python3-hacking < 4.0.0
%endif
BuildRequires:	python3-reno >= 2.5.0
BuildRequires:	python3-six >= 1.12.0
BuildRequires:	python3-stestr >= 2.1.0
BuildRequires:	python3-testrepository >= 0.0.18
BuildRequires:	python3-testresources >= 2.0.0
BuildRequires:	python3-testscenarios >= 0.4
BuildRequires:	python3-testtools >= 2.2.0
BuildRequires:	python3-virtualenv >= 20.0.3
BuildRequires:	python3-wheel >= 0.32.0
%endif
%endif
%if %{with doc}
BuildRequires:	python3-openstackdocstheme >= 1.18.1
BuildRequires:	python3-reno >= 2.5.0
BuildRequires:	python3-six >= 1.12.0
BuildRequires:	python3-sphinxcontrib-apidoc >= 0.2.0
BuildRequires:	sphinx-pdg-3 >= 1.6.2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PBR is a library that injects some useful and sensible default
behaviors into your setuptools run. It started off life as the chunks
of code that were copied between all of the OpenStack projects. Around
the time that OpenStack hit 18 different projects each with at least 3
active branches, it seems like a good time to make that code into a
proper re-usable library.

%description -l pl.UTF-8
PBR to biblioteka wstrzykująca trochę przydatnych i sensownych
domyślnych zachowań przy uruchomieniu setuptools. Początki wywodzą się
z fragmentów kodu kopiowanych między wszystkimi projektami OpenStacka.
Kiedy OpenStack dorobił się 18 różnych projektów, z których każdy miał
przynajmniej 3 aktywne gałęzie, uznano to za dobry moment na
wydzielenie kodu do biblioteki.

%package -n python3-pbr
Summary:	Python Build Reasonableness
Summary(pl.UTF-8):	Python Build Reasonableness - rozsądne budowanie modułów pythonowych
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5
Conflicts:	python-pbr < 5.8.1

%description -n python3-pbr
PBR is a library that injects some useful and sensible default
behaviors into your setuptools run. It started off life as the chunks
of code that were copied between all of the OpenStack projects. Around
the time that OpenStack hit 18 different projects each with at least 3
active branches, it seems like a good time to make that code into a
proper re-usable library.

%description -n python3-pbr -l pl.UTF-8
PBR to biblioteka wstrzykująca trochę przydatnych i sensownych
domyślnych zachowań przy uruchomieniu setuptools. Początki wywodzą się
z fragmentów kodu kopiowanych między wszystkimi projektami OpenStacka.
Kiedy OpenStack dorobił się 18 różnych projektów, z których każdy miał
przynajmniej 3 aktywne gałęzie, uznano to za dobry moment na
wydzielenie kodu do biblioteki.

%package doc
Summary:	Documentation for Python pbr package
Summary(pl.UTF-8):	Dokumentacja do pakietu Pythona pbr
Group:		Documentation

%description doc
Documentation for Python pbr package (both user and API
documentation).

%description doc -l pl.UTF-8
Dokumentacja do pakietu Pythona pbr (zarówno dokumentacja użytkownika,
jak i API).

%prep
%setup -q -n %{module}-%{version}

# Move away the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%{__mv} test-requirements.txt{,.disabled}

# Remove bundled egg-info
%{__rm} -r %{module}.egg-info

%build
%if %{with python2}
%py_build %{?with_tests:test}

%{?with_tests:%{__rm} -r .testrepository}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}

%{?with_tests:%{__rm} -r .testrepository}
%endif

%if %{with doc}
# generate html docs
sphinx-build-3 doc/source html
# remove the sphinx-build leftovers
%{__rm} -r html/{_sources,.doctrees,.buildinfo}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pbr{,-2}
%endif

%if %{with python3}
%py3_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pbr{,-3}
%endif

%if %{with python2}
ln -sf pbr-2 $RPM_BUILD_ROOT%{_bindir}/pbr
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE README.rst
%attr(755,root,root) %{_bindir}/pbr-2
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{py_sitescriptdir}/%{module}
%endif

%if %{with python3}
%files -n python3-pbr
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE README.rst
%attr(755,root,root) %{_bindir}/pbr
%attr(755,root,root) %{_bindir}/pbr-3
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{py3_sitescriptdir}/%{module}
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc html/*
%endif
