#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
from PIL import Image
from os.path import join
import ArtSciColor as art
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, HDBSCAN

##############################################################################
# Setup paths and clusters number
##############################################################################
(FILENAME, HSV_SORT, CLST_NUM) = (
    "dancing_couple_in_the_snow__reverse__1989.60.1.b.png",  
    True, 6
)
(I_PATH, O_PATH) = (
    '/Users/sanchez.hmsc/Documents/ArtSci/Fingerprint/Kirchner/in/', 
    '/Users/sanchez.hmsc/Documents/ArtSci/Fingerprint/Kirchner/out/'
)
##############################################################################
# Constants
##############################################################################
CLUSTERING = {
    'algorithm': AgglomerativeClustering, 
    'params': {'n_clusters': CLST_NUM}
}
(BAR_HEIGHT, MAX_SPAN) = (.15, 100)
(FONT, FONT_SIZE, HUE_CLASSES) = (
    'Avenir', 75,
    math.ceil(CLST_NUM*0.4)
)
##############################################################################
# Preprocess image
##############################################################################
img = art.readCV2Image(join(I_PATH, FILENAME))
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
##############################################################################
# Export to Disk
##############################################################################
# imgOut
imgOut.save(join(O_PATH, "".join(FILENAME.split('.')[0:-1])+'.png'))
imgOut.close()
