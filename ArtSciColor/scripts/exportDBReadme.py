#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
from colour import Color
import ArtSciColor as art
from os.path import join

DB_FILE = art.PTH_DBBZ
PATH_OUT = art.PTH_SWCH
PATH_RDM = art.PTH_SWRM
PATH_SWT = art.PTH_SWBZ
(width, height) = (art.SWATCH_DIMS['width'], art.SWATCH_DIMS['height'])
###############################################################################
# Load Databases
###############################################################################
db = art.loadDatabase(DB_FILE)
hexSwatches = art.loadDatabase(PATH_SWT, df=False)
###############################################################################
# Export swatches and generate MD text
###############################################################################
mdTexts = []
for (ix, entry) in db.iterrows():
    (hname, artist, title, url) = [
        entry[c] for c in ('hash', 'artist', 'title', 'url')
    ]
    # Get swatch --------------------------------------------------------------
    pal = entry['palette'].split(',')
    hexSwt = [Color(h) for h in pal]
    # Generate swatch img -----------------------------------------------------
    dimg = np.zeros((height, width, 3))
    swatch = art.genColorSwatch(dimg, height, hexSwt, proportionalHeight=False)
    swtchImg = Image.fromarray(swatch.astype('uint8'), 'RGB')
    # Add swatch to hash database ---------------------------------------------
    hexSwatches[hname] = pal
    # Generate table html entry -----------------------------------------------
    palPth = join(PATH_OUT, f'{hname}.jpg')
    relPth = join('../media/swatches', f'{hname}.jpg')
    swtchImg.save(palPth)
    entry = [
        f'<td style="text-align: center; vertical-align: middle;">{e}</td>' 
        for e in (
            artist, 
            f'<a href={url}>{title}</a>', 
            f'<img style="border-radius: 10px;" src="{relPth}" height="25">', 
            hname
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
    for e in ('Artist', 'Title', 'Palette', 'ID')
]
text = '''
<!DOCTYPE html>
<html><body>
<h1>Art Palettes</h1>
<table style="width:100%">
<tr>{}</tr>{}
</table>
</body></html>
'''.format(''.join(th), ''.join(mdTexts))
# Write to disk ---------------------------------------------------------------
with open(join(PATH_RDM, f'Art.md'), 'w') as f:
    f.write(text)
with open(join(PATH_RDM, f'Art.html'), 'w') as f:
    f.write(text)