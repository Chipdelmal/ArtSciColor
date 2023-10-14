#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import pkg_resources
from os.path import join
import ArtSciColor.paths as pth
import ArtSciColor.auxiliary as aux

SWATCH_DIMS = {'width': 750, 'height': 50}
NOT_ART = set(('Splatoon', ))
###############################################################################
# Load Serialized data
#   https://stackoverflow.com/questions/779495/access-data-in-package-subdirectory
#   https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
###############################################################################
DATA_PATH = pkg_resources.resource_filename('ArtSciColor', 'data/')
(PT_SW, PT_DF) = (join(DATA_PATH, 'SWATCHES.bz'), join(DATA_PATH, 'DB.csv'))
SWATCHES = aux.loadDatabase(PT_SW, df=False)
SWATCHES_DF = pd.read_csv(PT_DF)