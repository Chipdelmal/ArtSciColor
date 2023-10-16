#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import numpy as np
import pandas as pd
from sys import argv
from PIL import Image
from colour import Color
import ArtSciColor as art
import constants as cst


###############################################################################
# Setup Paths
###############################################################################
DB_FILE = art.PTH_DBBZ
PATH_OUT = art.PTH_SWCH
PATH_RDM = art.PTH_SWRM
PATH_SWT = art.PTH_SWBZ
(width, height) = (art.SWATCH_DIMS['width'], art.SWATCH_DIMS['height'])
###############################################################################
# Read Database
###############################################################################
db = art.loadDatabase(DB_FILE)
dims = art.SWATCH_DIMS
np.zeros((dims['width'], dims['height'], 3))


swatch = db.iloc[0]['palette']
palette = [Color(c).rgb for c in swatch.split(',')]