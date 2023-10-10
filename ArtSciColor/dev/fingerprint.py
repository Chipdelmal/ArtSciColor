
import cv2
import math
import colorsys
import numpy as np
from os.path import join
import ArtSciColor as art
from colour import Color
import colorir as cir
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
from collections import Counter
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, HDBSCAN

##############################################################################
# Setup paths and clusters number
##############################################################################
(FILENAME, HSV_SORT, CLST_NUM) = (
    "chestnut_trees_in_moonlight_2012.92.134.png",  
    True,
    6
)
(I_PATH, O_PATH) = (
    '/Users/sanchez.hmsc/Documents/ArtSci/Fingerprint/Kirchner/in/', 
    '/Users/sanchez.hmsc/Documents/ArtSci/Fingerprint/Kirchner/out/'
)
RESIZE_FRC = 0.05
(BAR_HEIGHT, BUF_HEIGHT, BUF_COLOR) = (.15, .005, [255, 255, 255])
##############################################################################
# Preprocess image
##############################################################################
img = art.readCV2Image(join(I_PATH, FILENAME))
MAX_SPAN = 150
if img.shape[0] > img.shape[1]:
    resized = art.resizeCV2ImageAspect(img, width=MAX_SPAN)
else:
    resized = art.resizeCV2ImageAspect(img, height=MAX_SPAN)
(height, width, depth) = resized.shape
##############################################################################
# Cluster for Dominance
#   resized, cFun=DBSCAN, cArgs={'eps': CLST_NUM}
#   https://stackoverflow.com/questions/73172602/how-to-sort-colors-by-their-hue-in-python-without-mixing-shades-of-gray
##############################################################################
(pixels, labels) = art.calcDominantColors(
    resized, 
    # cFun=HDBSCAN, cArgs={'min_cluster_size': 12, 'max_cluster_size': 10}
    cFun=AgglomerativeClustering, cArgs={'n_clusters': CLST_NUM}
)
swatch = art.getDominantSwatch(pixels, labels)
if HSV_SORT:
    swatchHex = art.sortSwatchHSV(swatch, hue_classes=math.ceil(CLST_NUM*0.4))
else:
    swatchHex = art.sortSwatchByFrequency(swatch)
##############################################################################
# Generate Array
##############################################################################
barsImg = art.genColorSwatch(img, BAR_HEIGHT, swatchHex, proportionalHeight=True)
newIMG = np.row_stack([img, barsImg])
imgOut = Image.fromarray(newIMG.astype('uint8'), 'RGB')
##############################################################################
# Generate labels
##############################################################################
font = font_manager.FontProperties(family='Avenir', weight='regular')
file = font_manager.findfont(font)
font = ImageFont.truetype(file, 75)
draw = ImageDraw.Draw(imgOut)
(W, H) = (imgOut.width/(len(swatchHex)), imgOut.height-(barsImg.shape[0])/2)
for (ix, hex) in enumerate(swatchHex):
    (colorHex, colorRGB) = (hex.hex.upper(), hex.rgb)
    tcol = art.getTextColor(hex)
    bbox = draw.textbbox(xy=(0, 0), text=colorHex, font=font)
    (w, h) = (bbox[2]-bbox[0], bbox[3]-bbox[1])
    draw.text(
        ((((2*ix+1)*W-w)/2, H-h/1.75)), 
        colorHex, tuple([int(255*i) for i in tcol.rgb]), 
        font=font
    )
##############################################################################
# Export to Disk
##############################################################################
imgOut.save(join(O_PATH, "".join(FILENAME.split('.')[0:-1])+'.png'))
imgOut

