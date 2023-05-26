
import cv2
import colorsys
import numpy as np
from os.path import join
import ArtSciColor as art
from PIL import Image
from collections import Counter
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN

##############################################################################
# Setup paths and clusters number
##############################################################################
(FILENAME, CLST_NUM, CSORT) = ('mario.jpg', 7, True)
(I_PATH, O_PATH) = (
    '/Users/sanchez.hmsc/Documents/ArtSci/Fingerprint/in/', 
    '/Users/sanchez.hmsc/Documents/ArtSci/Fingerprint/out/'
)
RESIZE_FRC = 0.1
(BAR_HEIGHT, BUF_HEIGHT, BUF_COLOR) = (.05, .005, [255, 255, 255])
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
    # resized, cFun=AgglomerativeClustering, cArgs={'n_clusters': CLST_NUM}
    resized, cFun=DBSCAN, cArgs={'eps': 11}
)
swatch = art.getDominantSwatch(pixels, labels)
print(swatch)
if CSORT:
    swatch.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb[0].get_rgb()))
print(swatch)
##############################################################################
# Export
##############################################################################
newIMG = np.row_stack([
    img,
    # art.genColorBar(img.shape[1], 10, color=[0, 0, 0]),
    art.genColorSwatch(img, 0.1, swatch, proportionalHeight=True)   
])
imgOut = Image.fromarray(newIMG.astype('uint8'), 'RGB')
imgOut.save(join(O_PATH, FILENAME.split('.')[0]+'.png'))

