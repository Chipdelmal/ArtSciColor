#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from math import ceil, floor
import random
import numpy as np
import pandas as pd
from sys import argv
from PIL import Image
from os.path import join, expanduser
from pathlib import Path
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, HDBSCAN
import ArtSciColor as art
import constants as cst

SEED=174887
random.seed(SEED)
np.random.seed(SEED)
##############################################################################
# Setup paths and clusters number
##############################################################################
if art.isNotebook():
    (FILENAME, ARTIST, CLST_NUM, TITLE) = (
        "183473.png",
        "DarbyBannard", 2,
        None
    )
    (I_PATH, O_PATH) = (
        f'../data/sources/{ARTIST}/in/', 
        f'../data/sources/{ARTIST}/out/'
    )
    URL = None
    (ADD_TO_DB, SHOW) = (False, True)
else: 
    (I_PATH, O_PATH, FILENAME, CLST_NUM, URL, ARTIST, TITLE) = (
        argv[1], argv[2], argv[3], int(argv[4]), argv[5] , argv[6] , argv[7]
    )
    (ADD_TO_DB, SHOW) = (True, False)
(I_PATH, O_PATH) = [expanduser(f) for f in (I_PATH, O_PATH)]
##############################################################################
# Constants
##############################################################################
(DB_FILE, DF_FILE) = (art.PTH_DBBZ, art.PTH_DBDF)
CLUSTERING = {
    'algorithm': AgglomerativeClustering, 
    'params': {
        'n_clusters': CLST_NUM,
        'compute_full_tree': True,
        'linkage': 'ward'
    } 
}
(FONT, FONT_SIZE, HSV_SORT, HUE_CLASSES) = (
    'Avenir', 50,
    True, ceil(CLST_NUM*0.4)
)
##############################################################################
# Process Image
##############################################################################
fPath = join(I_PATH, FILENAME)
try:
    img = art.readCV2Image(fPath)
except:
    sys.exit(f"Error reading file: {fPath}")
# Cluster colors -------------------------------------------------------------
imgClustered = art.getSwatchedImage(
    img, maxSide=cst.IMG_RESIZE, 
    cFun=CLUSTERING['algorithm'], cArgs=CLUSTERING['params'],
    grpFun=np.median, 
    HSVSort=HSV_SORT, hueClasses=HUE_CLASSES, grayThreshold=25,
    barHeight=cst.BAR_HEIGHT, barProportional=True,
    font=FONT, fontSize=FONT_SIZE
)
(swatchHex, imgOut) = (imgClustered['swatch'], imgClustered['image'])
if SHOW:
    imgOut.show()
##############################################################################
# Export to Disk
##############################################################################
if TITLE is not None:
    noExtFName = Path(fPath).stem
    # hashName = art.hashFilename(''.join(sorted([i.hex for i in swatchHex])))
    hashName = art.hashFilename(''.join([ARTIST, TITLE]))
    hashFile = f'{hashName}.png'
    imgOut.save(join(O_PATH, hashFile), quality=95)
    imgOut.close()
    print(hashName, file=sys.stderr)
##############################################################################
# Update DataBase
##############################################################################
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

