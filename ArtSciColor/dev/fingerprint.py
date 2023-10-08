
import cv2
import colorsys
import numpy as np
from os.path import join
import ArtSciColor as art
from colour import Color
import colorir as cir
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
from collections import Counter
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN

##############################################################################
# Setup paths and clusters number
##############################################################################
(FILENAME, CSORT, CLST_NUM) = (
    "banks_of_the_seine,_vetheuil_1963.10.177.jpg",  
    False,
    4
)
(I_PATH, O_PATH) = (
    '/Users/sanchez.hmsc/Documents/ArtSci/Fingerprint/Monet/in/', 
    '/Users/sanchez.hmsc/Documents/ArtSci/Fingerprint/Monet/out/'
)
RESIZE_FRC = 0.05
(BAR_HEIGHT, BUF_HEIGHT, BUF_COLOR) = (.15, .005, [255, 255, 255])
##############################################################################
# Preprocess image
##############################################################################
img = art.readCV2Image(join(I_PATH, FILENAME))
if img.shape[0] > img.shape[1]:
    resized = art.resizeCV2ImageAspect(img, width=150)
else:
    resized = art.resizeCV2ImageAspect(img, height=150)
(height, width, depth) = resized.shape
##############################################################################
# Cluster for Dominance
#   resized, cFun=DBSCAN, cArgs={'eps': CLST_NUM}
#   https://stackoverflow.com/questions/73172602/how-to-sort-colors-by-their-hue-in-python-without-mixing-shades-of-gray
##############################################################################
(pixels, labels) = art.calcDominantColors(
    resized, 
    cFun=AgglomerativeClustering, 
    cArgs={'n_clusters': CLST_NUM}
)
swatch = art.getDominantSwatch(pixels, labels)
# print(swatch)
if CSORT:
    swatch.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb[0].get_rgb()))
    swatchHex = [s[0] for s in swatch]
else:
    swatchHex = [s[0].hex for s in swatch]
    swatchHex.sort(key=cir.hue_sort_key(hue_classes=2, alt_lum=True))
    swatchHex = [Color(c) for c in swatchHex]
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
# print(file)
font = ImageFont.truetype(file, 100)
draw = ImageDraw.Draw(imgOut)
(W, H) = (imgOut.width/(len(swatch)), imgOut.height-(barsImg.shape[0])/2)
for (ix, hex) in enumerate(swatch):
    (colorHex, colorRGB) = (hex[0].hex, hex[0].rgb)
    tcol = (0, 0, 0) if (colorRGB[0]*0.299 + colorRGB[1]*0.587 + colorRGB[2]*0.114) > 0.65 else (255, 255, 255)
    bbox = draw.textbbox(xy=(0, 0), text=colorHex, font=font)
    (w, h) = (bbox[2]-bbox[0], bbox[3]-bbox[1])
    draw.text(
        ((((2*ix+1)*W-w)/2, H-h/1.75)), 
        colorHex, tcol, 
        font=font
    )
##############################################################################
# Export to Disk
##############################################################################
imgOut.save(join(O_PATH, FILENAME.split('.')[0]+'.png'))
imgOut