#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join
import numpy as np
from sys import argv
from PIL import Image
from colour import Color
import ArtSciColor as art
import constants as cst

if art.isNotebook():
    CATEGORY = 'Other'
else:
    CATEGORY = argv[1]
DIMS = (500, 250)
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
artistsSet = art.CATEGORIES[CATEGORY]
db = db[db['artist'].isin(artistsSet)]
dims = art.SWATCH_DIMS
palsNum = db.shape[0]
fullSwatch = np.zeros((palsNum, dims['height'], 3))
###############################################################################
# Generate Swatch
###############################################################################
swatches = []
for ix in range(db.shape[0]):
    swatch = db.iloc[ix]['palette']
    hexSwt = [Color(c) for c in swatch.split(',')]
    dimg = np.zeros((DIMS[0], DIMS[1], 3))
    swatch = art.genColorSwatchFromImg(dimg, DIMS[1], hexSwt, proportionalHeight=False)
    swatches.append(swatch)
fullSwatch =np.transpose(np.vstack(swatches), axes=(1, 0, 2))
imgOut = Image.fromarray(fullSwatch.astype('uint8'), 'RGB')
###############################################################################
# Export Swatch
###############################################################################
imgOut.save(join(PATH_OUT, f'{CATEGORY}.png'), quality=95)