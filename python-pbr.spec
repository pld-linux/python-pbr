#
# Conditional build:
%bcond_without	doc		# don't build doc
%bcond_with	tests	# tests are failing currently
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module

%define 	module	pbr
Summary:	Python Build Reasonableness
Name:		python-%{module}
Version:	0.10.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	http://pypi.python.org/packages/source/p/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	9e02dbfb5e49210c381fd4eea00cf7b7
URL:		http://pypi.python.org/pypi/pbr
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	rpm-pythonprov
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
%if %{with python2}
# very new required, when also using tests
BuildRequires:	python-Sphinx >= 1.1.3
BuildRequires:	python-d2to1 >= 0.2.10
BuildRequires:	python-devel
%endif
%if %{with tests}
BuildRequires:	python-testscenarios
BuildRequires:	python-testtools
# still not packaged yet:
BuildRequires:	python-coverage >= 3.6
BuildRequires:	python-discover
BuildRequires:	python-flake8
BuildRequires:	python-mock >= 1.0
BuildRequires:	python-subunit
BuildRequires:	python-testrepository >= 0.0.18
BuildRequires:	python-testresources
%endif
%if %{with python3}
BuildRequires:	python3-d2to1
BuildRequires:	python3-devel
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

%package -n python3-pbr
Summary:	Python Build Reasonableness
Group:		Libraries/Python

%description -n python3-pbr
Manage dynamic plugins for Python applications

%prep
%setup -q -n %{module}-%{version}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requiers_dist config
rm -rf {test-,}requirements.txt

# Remove bundled egg-info
rm -rf %{module}.egg-info

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%if %{with test}
%{__python} setup.py test
%endif

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc html README.rst LICENSE
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{py_sitescriptdir}/%{module}
%endif

%if %{with python3}
%files -n python3-pbr
%defattr(644,root,root,755)
%doc html README.rst LICENSE
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{py3_sitescriptdir}/%{module}
%endif
