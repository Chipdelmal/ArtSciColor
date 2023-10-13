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
    FNAME = 'Splatoon2'
else:
    FNAME = argv[1]
###############################################################################
# Setup Paths
###############################################################################
PATH_OUT = art.PTH_SWCH
PATH_RDM = art.PTH_SWRM
PATH_SWT = art.PTH_SWBZ
(DB_FILE, PTH_CSV) = (art.PTH_DBBZ, art.PTH_DATA)
(width, height) = (art.SWATCH_DIMS['width'], art.SWATCH_DIMS['height'])
###############################################################################
# Load data
###############################################################################
NAMES = ('Name', 'Alpha', 'Beta', 'Gamma', 'Delta')
db = pd.read_csv(join(PTH_CSV, f'{FNAME}.csv'), header=None, names=NAMES)
###############################################################################
# Iterate
###############################################################################
(mdTexts, hexSwatches) = ([], dict())
for (ix, entry) in db.iterrows():
    row = [e.strip() for e in entry if isinstance(e, str)]
    (name, pal) = (row[0], row[1:])
    # Treat palette -----------------------------------------------------------
    hName = art.hashFilename(FNAME+name+''.join(pal))
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
        f'<td style="text-align: center; vertical-align: middle;">{e}</td>' for e in (
            name, 
            f'<img style="border-radius: 10px;" src="{relPth}" height="25">', 
            hName
        )
    ]
    mdRow = '\r<tr>'+' '.join(entry)+'</tr>'
    mdTexts.append(mdRow)
###############################################################################
# Export Swatches
###############################################################################
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