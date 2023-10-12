#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
from colour import Color
import ArtSciColor as art
import constants as cst
from os.path import join

DB_FILE = cst.DB_PATH
PATH_OUT = "../media/swatches"
PATH_RDM = "../media/"
(width, height) = (750, 50)

db = art.loadDatabase(DB_FILE)
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
    # Generate table html entry -----------------------------------------------
    palPth = join(PATH_OUT, f'{hname}.jpg')
    swtchImg.save(palPth)
    swPath = './swatches/'
    entry = [
        f'<td style="text-align: center; vertical-align: middle;">{e}</td>' for e in (
            artist, 
            f'<a href={url}>{title}</a>', 
            f'<img style="border-radius: 10px;" src="{palPth}" height="25">', 
            hname
        )
    ]
    mdRow = '\r\t<tr>'+' '.join(entry)+'</tr>'
    mdTexts.append(mdRow)
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
<h2>Available Palettes</h2>
<table style="width:100%">
    <tr>{}</tr>{}
</table>
</body></html>
'''.format(''.join(th), ''.join(mdTexts))
# Write to disk ---------------------------------------------------------------
with open(join(PATH_RDM, f'README.md'), 'w') as f:
    f.write(text)
with open(join(PATH_RDM, f'README.html'), 'w') as f:
    f.write(text)