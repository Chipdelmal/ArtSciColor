
import cv2
import numpy as np
from os.path import join
import ArtSciColor as art
from collections import Counter
from sklearn.cluster import KMeans, AgglomerativeClustering

##############################################################################
# Setup paths and clusters number
##############################################################################
FILENAME = 'nausicaa.jpg'
(I_PATH, O_PATH) = ('../media/', './out/')
(CLST_NUM, RESIZE_FRC, MAX_ITER) = (10, 0.1, 1000)
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
    resized, cFun=AgglomerativeClustering, cArgs={'n_clusters': CLST_NUM}
)
art.getDominantSwatch(pixels, labels)


