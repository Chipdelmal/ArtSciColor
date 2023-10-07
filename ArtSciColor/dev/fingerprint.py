
import cv2
import colorsys
import numpy as np
from os.path import join
import ArtSciColor as art
from PIL import Image, ImageDraw, ImageFont
from collections import Counter
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN

##############################################################################
# Setup paths and clusters number
##############################################################################
(FILENAME, CLST_NUM, CSORT) = (
    "the_artist's_garden_in_argenteuil_(a_corner_of_the_garden_with_dahlias)_1991.27.1.jpg", 
    6, 
    False
)
(I_PATH, O_PATH) = (
    '/Users/sanchez.hmsc/Documents/ArtSci/Fingerprint/MoNeT/in/', 
    '/Users/sanchez.hmsc/Documents/ArtSci/Fingerprint/MoNeT/out/'
)
RESIZE_FRC = 0.05
(BAR_HEIGHT, BUF_HEIGHT, BUF_COLOR) = (.25, .005, [255, 255, 255])
##############################################################################
# Preprocess image
##############################################################################
img = art.readCV2Image(join(I_PATH, FILENAME))
resized = art.resizeCV2Image(img, RESIZE_FRC)
(height, width, depth) = resized.shape
##############################################################################
# Cluster for Dominance
##############################################################################
(pixels, labels) = art.calcDominantColors(
    resized, cFun=AgglomerativeClustering, cArgs={'n_clusters': CLST_NUM}
    # resized, cFun=DBSCAN, cArgs={'eps': CLST_NUM}
)
swatch = art.getDominantSwatch(pixels, labels)
print(swatch)
if CSORT:
    swatch.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb[0].get_rgb()))
print(swatch)
##############################################################################
# Export
##############################################################################
barsImg = art.genColorSwatch(img, BAR_HEIGHT, swatch, proportionalHeight=True)  
newIMG = np.row_stack([
    img,
    # art.genColorBar(img.shape[1], 10, color=[0, 0, 0]),
    barsImg
])
imgOut = Image.fromarray(newIMG.astype('uint8'), 'RGB')



font = ImageFont.truetype("Arial Narrow.ttf", 150)

colorHex = '#FFFFFF'
draw = ImageDraw.Draw(imgOut)
(w, h) = draw.textsize(colorHex)
(W, H) = (
    imgOut.width/(len(swatch)+1),
    imgOut.height+(barsImg.shape[0])/2
)
draw.text(
    (((W-w)/2, H-h/2)), 
    colorHex, (255, 255, 255), 
    font=font
)
imgOut


imgOut.save(join(O_PATH, FILENAME.split('.')[0]+'.png'))

