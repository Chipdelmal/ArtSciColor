#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import numpy as np
import pandas as pd
from os.path import join
from PIL import Image
from colour import Color
import ArtSciColor as art

if art.isNotebook():
    FNAME = 'chipdelmal'
    ADD_TO_DB = False
else:
    FNAME = argv[1]
    ADD_TO_DB = True
###############################################################################
# Setup Paths
###############################################################################
PATH_OUT = art.PTH_SWCH
PATH_RDM = art.PTH_SWRM
PATH_SWT = art.PTH_SWBZ
(DB_FILE, PTH_CSV, DF_FILE) = (art.PTH_DBBZ, art.PTH_DATA, art.PTH_DBDF)
(width, height) = (art.SWATCH_DIMS['width'], art.SWATCH_DIMS['height'])
###############################################################################
# Load Databases
###############################################################################
hexSwatches = art.loadDatabase(PATH_SWT, df=False)
###############################################################################
# Load data
###############################################################################
NAMES = (
    'Name', 'URL', 
    'Hex01', 'Hex02', 'Hex03', 'Hex04', 'Hex05', 
    'Hex06', 'Hex07', 'Hex08', 'Hex09', 'Hex10',
    'Hex11', 'Hex12', 'Hex13', 'Hex14', 'Hex15',
    'Hex16', 'Hex17', 'Hex18', 'Hex19', 'Hex20',
    'Hex21', 'Hex22', 'Hex23', 'Hex24', 'Hex25',
    'Hex26', 'Hex27', 'Hex28', 'Hex29', 'Hex30',
)
splat = pd.read_csv(join(PTH_CSV, f'{FNAME}.csv'), header=None, names=NAMES)
###############################################################################
# Iterate
###############################################################################
mdTexts = []
for (ix, entry) in splat.iterrows():
    row = [e.strip() for e in entry if isinstance(e, str)]
    (name, url, pal) = (row[0], row[1], row[2:])
    strPal = art.listPalToStr(pal)
    # Treat palette -----------------------------------------------------------
    hName = art.hashFilename(''.join(sorted(pal)))
    hexSwt = [Color(h) for h in pal]
    # Generate swatch ---------------------------------------------------------
    dimg = np.zeros((height, width, 3))
    swatch = art.genColorSwatch(dimg, height, hexSwt, proportionalHeight=False)
    swtchImg = Image.fromarray(swatch.astype('uint8'), 'RGB')
    # Add swatch to hash database ---------------------------------------------
    hexSwatches[hName] = pal
    # Generate table html entry -----------------------------------------------
    palPth = join(PATH_OUT, f'{hName}.png')
    relPth = join('../media/swatches', f'{hName}.png')
    swtchImg.save(palPth, quality=95)
    mdRow = art.generateHTMLEntry(FNAME, url, name, relPth, hName, strPal)
    mdTexts.append(mdRow)
    ###########################################################################
    # Update DataBase
    ###########################################################################
    if ADD_TO_DB:
        db = art.loadDatabase(DB_FILE)
        newEntry = pd.DataFrame({
            'artist': FNAME, 
            'title': name,
            'palette': ','.join([c.hex.upper() for c in hexSwt]),
            'clusters': len(pal), 
            'clustering': "None",
            'filename': "None", 
            'hash': hName,
            'url': url
        }, index=[0])
        db = pd.concat([
            db.loc[:], newEntry
        ]).reset_index(drop=True).drop_duplicates()
        db.sort_values(["artist", "title"], axis=0, inplace=True)
        db = db.reindex(list(art.DF_SORTING), axis=1)
        art.dumpDatabase(db, DB_FILE)
        art.exportDatabase(db, DF_FILE)
        art.dumpDatabase(hexSwatches, PATH_SWT)
###############################################################################
# Export HTML/MD data
###############################################################################
text = art.RDM_TEXT.format(FNAME, ''.join(art.RDM_HEADER), ''.join(mdTexts))
# Write to disk ---------------------------------------------------------------
with open(join(PATH_RDM, f'{FNAME}.md'), 'w') as f:
    f.write(text)
with open(join(PATH_RDM, f'{FNAME}.html'), 'w') as f:
    f.write(text)
