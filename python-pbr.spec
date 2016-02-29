#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# tests are failing currently
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	pbr
Summary:	Python Build Reasonableness
Summary(pl.UTF-8):	Python Build Reasonableness - rozsądne budowanie modułów pythonowych
Name:		python-%{module}
Version:	1.8.1
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/pypi/pbr
Source0:	https://pypi.python.org/packages/source/p/pbr/%{module}-%{version}.tar.gz
# Source0-md5:	c8f9285e1a4ca6f9654c529b158baa3a
URL:		https://launchpad.net/pbr
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
%if %{with python2}
# very new required, when also using tests
BuildRequires:	python-Sphinx >= 1.1.3
BuildRequires:	python-devel >= 1:2.6
%if %{with tests}
# some still not packaged yet:
BuildRequires:	python-coverage >= 3.6
BuildRequires:	python-discover
BuildRequires:	python-fixtures >= 1.3.1
BuildRequires:	python-hacking >= 0.10.0
BuildRequires:	python-hacking < 0.11
BuildRequires:	python-mock >= 1.2
BuildRequires:	python-six >= 1.9.0
BuildRequires:	python-subunit >= 0.0.18
BuildRequires:	python-testrepository >= 0.0.18
BuildRequires:	python-testresources >= 0.2.4
BuildRequires:	python-testscenarios >= 0.4
BuildRequires:	python-testtools >= 1.4.0
BuildRequires:	python-virtualenv
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.3
%if %{with tests}
BuildRequires:	python3-coverage >= 3.6
BuildRequires:	python3-discover
BuildRequires:	python3-fixtures >= 1.3.1
BuildRequires:	python3-hacking >= 0.10.0
BuildRequires:	python3-hacking < 0.11
BuildRequires:	python3-mock >= 1.2
BuildRequires:	python3-six >= 1.9.0
BuildRequires:	python3-subunit >= 0.0.18
BuildRequires:	python3-testrepository >= 0.0.18
BuildRequires:	python3-testresources >= 0.2.4
BuildRequires:	python3-testscenarios >= 0.4
BuildRequires:	python3-testtools >= 1.4.0
BuildRequires:	python3-virtualenv
%endif
%endif
Requires:	python-pip
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
Requires:	python3-pip

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

%prep
%setup -q -n %{module}-%{version}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%{__rm} test-requirements.txt

# Remove bundled egg-info
%{__rm} -r %{module}.egg-info

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
# generate html docs
sphinx-build doc/source html
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

ln -sf pbr-2 $RPM_BUILD_ROOT%{_bindir}/pbr

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc %{?with_doc:html} README.rst LICENSE
%attr(755,root,root) %{_bindir}/pbr
%attr(755,root,root) %{_bindir}/pbr-2
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{py_sitescriptdir}/%{module}
%endif

%if %{with python3}
%files -n python3-pbr
%defattr(644,root,root,755)
%doc %{?with_doc:html} README.rst LICENSE
%attr(755,root,root) %{_bindir}/pbr-3
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{py3_sitescriptdir}/%{module}
%endif
