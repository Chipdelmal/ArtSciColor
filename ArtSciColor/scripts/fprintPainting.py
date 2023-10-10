#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import numpy as np
from sys import argv
from PIL import Image
from os.path import join, expanduser
import ArtSciColor as art
from pathlib import Path
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, HDBSCAN

##############################################################################
# Setup paths and clusters number
##############################################################################
if art.isNotebook():
    (FILENAME, CLST_NUM) = (
        "dance_hall_bellevue__obverse__1989.60.1.a.jpg", 
        6
    )
    (I_PATH, O_PATH) = (
        '~/Pictures/ArtSci/Kirchner/in/', 
        '~/Pictures/ArtSci/Kirchner/out/'
    )
else: 
    (I_PATH, O_PATH, FILENAME, CLST_NUM) = (argv[1], argv[2], argv[3], int(argv[4]))
    # print((I_PATH, O_PATH, FILENAME, CLST_NUM))
(I_PATH, O_PATH) = [expanduser(f) for f in (I_PATH, O_PATH)]
##############################################################################
# Constants
##############################################################################
CLUSTERING = {
    'algorithm': AgglomerativeClustering, 
    'params': {'n_clusters': CLST_NUM}
}
(BAR_HEIGHT, MAX_SPAN) = (.15, 100)
(FONT, FONT_SIZE, HUE_CLASSES, HSV_SORT) = (
    'Avenir', 75,
    math.ceil(CLST_NUM*0.4),
    True
)
##############################################################################
# Preprocess image
##############################################################################
fPath = join(I_PATH, FILENAME)
try:
    img = art.readCV2Image(fPath)
except:
    sys.exit(f"Error reading file: {fPath}")
resized = art.resizeCV2BySide(img, MAX_SPAN)
(height, width, depth) = resized.shape
##############################################################################
# Cluster for Dominance
##############################################################################
(pixels, labels) = art.calcDominantColors(
    resized, cFun=CLUSTERING['algorithm'], cArgs=CLUSTERING['params']
)
swatch = art.getDominantSwatch(pixels, labels)
swatchHex = (
    art.sortSwatchHSV(swatch, hue_classes=HUE_CLASSES)
    if HSV_SORT else
    art.sortSwatchByFrequency(swatch)
)
##############################################################################
# Generate Bars, add labels, and Stack to Image
##############################################################################
bars = art.genColorSwatch(img, BAR_HEIGHT, swatchHex, proportionalHeight=True)
barsImg = art.addHexColorText(
    Image.fromarray(bars.astype('uint8'), 'RGB'), 
    swatchHex, font=FONT, fontSize=FONT_SIZE
)
newIMG = np.row_stack([img, barsImg])
imgOut = Image.fromarray(newIMG.astype('uint8'), 'RGB')
# imgOut
##############################################################################
# Export to Disk
##############################################################################
noExtFName = Path(fPath).stem
hashName = art.hashFilename(noExtFName)
imgOut.save(join(O_PATH, f'{hashName}.png'))
imgOut.close()
print(hashName, file=sys.stderr)

