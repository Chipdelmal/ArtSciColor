
SHELL=bash
python=python
pip=pip
tests=.
version:=$(shell $(python) version.py)
sdist_name:=PlotMAPQ-$(version).tar.gz


###############################################################################
# Dev Operations
############################################################################### 
dev:
	- python -m pip install .

clean_develop:
	- python -m pip uninstall -y ArtSciColor
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
	&& twine upload dist/* \
	&& pip install .

clean_pypi:
	- rm -rf build/

###############################################################################
# Evaluate palettes
############################################################################### 
fingerprint:
	- rm -f ./ArtSciColor/data/DB.bz
	- rm -f ./ArtSciColor/data/DB.csv
	- rm -f ./ArtSciColor/data/SWATCHES.bz
	- rm -f ./ArtSciColor/media/swatches/*
	- bash ./ArtSciColor/scripts/fingerprintSplatoon.sh
	- bash ./ArtSciColor/scripts/fingerprintArt.sh
