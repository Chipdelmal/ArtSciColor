
SHELL=bash
python=python
pip=pip
tests=.
version:=$(shell $(python) version.py)
sdist_name:=PlotMAPQ-$(version).tar.gz


###############################################################################
# Dev Operations
############################################################################### 
develop:
	$(pip) install -e .

clean_develop:
	- $(pip) uninstall -y ArtSciColor
	- rm -rf *.egg-info

clean_sdist:
	- rm -rf dist

clean: clean_develop clean_pypi

check_build_reqs:
	@$(python) -c 'import pytest' \
                || ( printf "$(redpip)Build requirements are missing. Run 'make prepare' to install them.$(normal)" ; false )

pypi: clean clean_sdist
	set -x \
	&& $(python) setup.py sdist bdist_wheel \
	&& twine check dist/* \
	&& twine upload --repository-url https://test.pypi.org/legacy/ dist/*

clean_pypi:
	- rm -rf build/

###############################################################################
# Evaluate palettes
############################################################################### 
fingerprint:
	- bash ./ArtSciColor/scripts/fingerprintSplatoon.sh
	- bash ./ArtSciColor/scripts/fingerprintArt.sh
