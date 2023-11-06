#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import numpy as np
from PIL import Image
from colour import Color
import ArtSciColor as art
from os.path import join


if art.isNotebook():
    ARTIST = 'Other'
else:
    ARTIST = argv[1]
###############################################################################
# Setup Paths
###############################################################################
DB_FILE = art.PTH_DBBZ
PATH_OUT = art.PTH_SWCH
PATH_RDM = art.PTH_SWRM
PATH_SWT = art.PTH_SWBZ
(width, height) = (art.SWATCH_DIMS['width'], art.SWATCH_DIMS['height'])
###############################################################################
# Load Databases
###############################################################################
nArt = set.union(*list(art.CATEGORIES.values()))
db = art.loadDatabase(DB_FILE)
if ARTIST in art.ARTISTS_SET:
    db = db[db['artist']==ARTIST]
else:
    db = db[db['artist'].isin(art.CATEGORIES[ARTIST])]
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
    strPal = art.listPalToStr(pal)
    hexSwt = [Color(h) for h in pal]
    # Generate swatch img -----------------------------------------------------
    swatch = art.genColorSwatch(width, height, hexSwt)
    swtchImg = Image.fromarray(swatch.astype('uint8'), 'RGB')
    # Add swatch to hash database ---------------------------------------------
    hexSwatches[hname] = pal
    # Generate table html entry -----------------------------------------------
    palPth = join(PATH_OUT, f'{hname}.png')
    relPth = join('../media/swatches', f'{hname}.png')
    swtchImg.save(palPth)
    mdRow = art.generateHTMLEntry(artist, url, title, relPth, hname, strPal)
    mdTexts.append(mdRow)
###############################################################################
# Export Swatches
###############################################################################
art.dumpDatabase(hexSwatches, PATH_SWT)
###############################################################################
# Export HTML/MD data
###############################################################################
text = art.RDM_TEXT.format(ARTIST, ''.join(art.RDM_HEADER), ''.join(mdTexts))
# Write to disk ---------------------------------------------------------------
with open(join(PATH_RDM, f'{ARTIST}.md'), 'w') as f:
    f.write(text)
with open(join(PATH_RDM, f'{ARTIST}.html'), 'w') as f:
    f.write(text)
    
