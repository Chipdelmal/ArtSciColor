#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import numpy as np
import pandas as pd
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
        "183413.png",
        "Picasso", 6
    )
    (I_PATH, O_PATH) = (
        f'../data/sources/{ARTIST}/in/', 
        f'../data/sources/{ARTIST}/out/'
    )
    (TITLE, URL) = (None, None)
    (ADD_TO_DB, SHOW) = (False, True)
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
(DB_FILE, DF_FILE) = (art.PTH_DBBZ, art.PTH_DBDF)
CLUSTERING = {
    'algorithm': AgglomerativeClustering, 
    'params': {
        'n_clusters': CLST_NUM, # 'distance_threshold': 2500, 
        'compute_full_tree': True
    } 
}
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
    art.sortSwatchHSV(swatch, hue_classes=HUE_CLASSES, gray_thresh=25)
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
hashName = art.hashFilename(''.join(sorted([i.hex for i in swatchHex])))
hashFile = f'{hashName}.png'
imgOut.save(join(O_PATH, hashFile), quality=95)
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
    db.sort_values(["artist", "title"], axis=0, inplace=True)
    db = db.reindex(list(art.DF_SORTING), axis=1)
    art.dumpDatabase(db, DB_FILE)
    art.exportDatabase(db, DF_FILE)

