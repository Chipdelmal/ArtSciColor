#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import numpy as np
import pandas as pd
from os import path
from sys import argv
from PIL import Image
from os.path import join, expanduser
from pathlib import Path
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, HDBSCAN
import ArtSciColor as art
import constants as cst

##############################################################################
# Setup paths and clusters number
##############################################################################
if art.isNotebook():
    (FILENAME, ARTIST, CLST_NUM) = (
        "183381.png",
        "Miro",
        6
    )
    (I_PATH, O_PATH) = (
        f'~/Documents/GitHub/ArtSciColor/ArtSciColor/data/sources/{ARTIST}/in/', 
        f'~/Documents/GitHub/ArtSciColor/ArtSciColor/data/sources/{ARTIST}/out/'
    )
    (ARTIST, TITLE, URL) = (None, None, None)
    (ADD_TO_DB, SHOW) = (False, True)
    SHOW = True
else: 
    (I_PATH, O_PATH, FILENAME, CLST_NUM, URL, ARTIST, TITLE) = (
        argv[1], argv[2], argv[3], int(argv[4]), argv[5] , argv[6] , argv[7]
    )
    (ADD_TO_DB, SHOW) = (True, False)
    # print((I_PATH, O_PATH, FILENAME, CLST_NUM))
(I_PATH, O_PATH) = [expanduser(f) for f in (I_PATH, O_PATH)]
##############################################################################
# Constants
##############################################################################
(DB_FILE, DF_FILE) = (cst.DB_PATH, cst.DF_PATH)
CLUSTERING = {
    'algorithm': AgglomerativeClustering, 
    'params': {'n_clusters': CLST_NUM}
}
# CLUSTERING = {
#     'algorithm': HDBSCAN, 
#     'params': {
#         'min_cluster_size': 20, 'min_samples': 10, 'cluster_selection_epsilon': 7
#     }
# }
# CLUSTERING = {
#     'algorithm': DBSCAN, 'params': {'eps': CLST_NUM, 'min_samples': 50}
# }
(FONT, FONT_SIZE, HUE_CLASSES, HSV_SORT) = (
    'Avenir', 50,
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
resized = art.resizeCV2BySide(img, cst.IMG_RESIZE)
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
bars = art.genColorSwatch(
    img, cst.BAR_HEIGHT, swatchHex, 
    proportionalHeight=True
)
barsImg = art.addHexColorText(
    Image.fromarray(bars.astype('uint8'), 'RGB'), 
    swatchHex, font=FONT, fontSize=FONT_SIZE
)
newIMG = np.row_stack([img, barsImg])
imgOut = Image.fromarray(newIMG.astype('uint8'), 'RGB')
if SHOW:
    imgOut.show()
##############################################################################
# Export to Disk
##############################################################################
noExtFName = Path(fPath).stem
hashName = art.hashFilename(noExtFName)
hashFile = f'{hashName}.png'
imgOut.save(join(O_PATH, hashFile))
imgOut.close()
##############################################################################
# Update DataBase
##############################################################################
print(hashName, file=sys.stderr)
if ADD_TO_DB and ARTIST and ARTIST!="":
    db = art.loadDatabase(DB_FILE)
    newEntry = pd.DataFrame({
        'artist': ARTIST, 
        'title': TITLE,
        'palette': ','.join([c.hex.upper() for c in swatchHex]),
        'clusters': CLST_NUM, 
        'clustering': str(CLUSTERING['algorithm'].__name__),
        'filename': FILENAME, 
        'hash': hashName,
        'url': URL
    }, index=[0])
    db = pd.concat([db.loc[:], newEntry]).reset_index(drop=True).drop_duplicates()
    db.sort_values("artist", axis=0, inplace=True)
    art.dumpDatabase(db, DB_FILE)
    art.exportDatabase(db, DF_FILE)

