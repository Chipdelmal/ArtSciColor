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
    FNAME = 'Splatoon3'
    ADD_TO_DB = False
else:
    FNAME = argv[1]
    ADD_TO_DB = True
URL = 'https://splatoonwiki.org/wiki/Ink'
###############################################################################
# Setup Paths
###############################################################################
PATH_OUT = art.PTH_SWCH
PATH_RDM = art.PTH_SWRM
PATH_SWT = art.PTH_SWBZ
(DB_FILE, PTH_CSV) = (art.PTH_DBBZ, art.PTH_DATA)
(width, height) = (art.SWATCH_DIMS['width'], art.SWATCH_DIMS['height'])
###############################################################################
# Load Databases
###############################################################################
hexSwatches = art.loadDatabase(PATH_SWT, df=False)
(DB_FILE, DF_FILE) = (art.PTH_DBBZ, art.PTH_DBDF)
###############################################################################
# Load data
###############################################################################
NAMES = ('Name', 'Alpha', 'Beta', 'Gamma', 'Delta')
splat = pd.read_csv(join(PTH_CSV, f'{FNAME}.csv'), header=None, names=NAMES)
###############################################################################
# Iterate
###############################################################################
mdTexts = []
for (ix, entry) in splat.iterrows():
    row = [e.strip() for e in entry if isinstance(e, str)]
    (name, pal) = (row[0], row[1:])
    # Treat palette -----------------------------------------------------------
    hName = art.hashFilename(''.join(pal))
    hexSwt = [Color(h) for h in pal]
    # Generate swatch ---------------------------------------------------------
    dimg = np.zeros((height, width, 3))
    swatch = art.genColorSwatch(dimg, height, hexSwt, proportionalHeight=False)
    swtchImg = Image.fromarray(swatch.astype('uint8'), 'RGB')
    # Add swatch to hash database ---------------------------------------------
    hexSwatches[hName] = pal
    # Generate table html entry -----------------------------------------------
    palPth = join(PATH_OUT, f'{hName}.jpg')
    relPth = join('../media/swatches', f'{hName}.jpg')
    swtchImg.save(palPth)
    entry = [
        f'<td style="text-align: center; vertical-align: middle;">{e}</td>' 
        for e in (
            f'<a href={URL}>{name}</a>',
            f'<img style="border-radius: 10px;" src="{relPth}" height="25">', 
            hName
        )
    ]
    mdRow = '\r<tr>'+' '.join(entry)+'</tr>'
    mdTexts.append(mdRow)
    ###########################################################################
    # Update DataBase
    ###########################################################################
    if ADD_TO_DB:
        db = art.loadDatabase(DB_FILE)
        newEntry = pd.DataFrame({
            'artist': 'Splatoon', 
            'title': name,
            'palette': ','.join([c.hex.upper() for c in hexSwt]),
            'clusters': len(pal), 
            'clustering': "None",
            'filename': "None", 
            'hash': hName,
            'url': URL
        }, index=[0])
        db = pd.concat([
            db.loc[:], newEntry
        ]).reset_index(drop=True).drop_duplicates()
        db.sort_values("artist", axis=0, inplace=True)
        art.dumpDatabase(db, DB_FILE)
        art.exportDatabase(db, DF_FILE)
        art.dumpDatabase(hexSwatches, PATH_SWT)
###############################################################################
# Export HTML/MD data
###############################################################################
th = [
    f'<th style="text-align: center; vertical-align: middle;">{e}</th>'
    for e in ('Name', 'Palette', 'ID')
]
text = '''
<!DOCTYPE html>
<html><body>
<h1>{}</h1>
<table style="width:100%">
<tr>{}</tr>{}
</table>
</body></html>
'''.format(FNAME, ''.join(th), ''.join(mdTexts))
# Write to disk ---------------------------------------------------------------
with open(join(PATH_RDM, f'{FNAME}.md'), 'w') as f:
    f.write(text)
with open(join(PATH_RDM, f'{FNAME}.html'), 'w') as f:
    f.write(text)
