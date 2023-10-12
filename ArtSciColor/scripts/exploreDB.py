#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
from colour import Color
import ArtSciColor as art
import constants as cst
from os.path import join

DB_FILE = cst.DB_PATH
PATH_OUT = "../media"
(width, height) = (750, 50)

db = art.loadDatabase(DB_FILE)
db


ix = 11
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
    entry = [
        f'<td>{e}</td>' for e in (
            artist, 
            f'<a href={url}>{title}</a>', 
            f'<img src="{palPth}" height="25">', 
            hname
        )
    ]
    mdRow = '\r\t<tr>'+' '.join(entry)+'</tr>'
    mdTexts.append(mdRow)
    
text = '''
<!DOCTYPE html>
<html>
<body>
<h2>Available Palettes</h2>
<table style="width:100%">
    <tr><th>Artist</th> <th>Title</th> <th>Palette</th> <th>ID</th></tr>{}
</table>
</body>
</html>
'''.format(''.join(mdTexts))

with open(join(PATH_OUT, f'README.md'), 'w') as f:
    f.write(text)