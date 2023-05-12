
import cv2
import numpy as np
from os.path import join
import ArtSciColor as art
from collections import Counter
from sklearn.cluster import KMeans, AgglomerativeClustering, SpectralClustering

##############################################################################
# Setup paths and clusters number
##############################################################################
FILENAME = 'nausicaa.jpg'
(I_PATH, O_PATH) = ('../media/', './out/')
(CLST_NUM, RESIZE_PCT, MAX_ITER) = (6, 10, 1000)
(BAR_HEIGHT, BUF_HEIGHT, BUF_COLOR) = (.05, .005, [255, 255, 255])
##############################################################################
# Preprocess image
##############################################################################
# Load image ----------------------------------------------------------------
bgr = cv2.imread(join(I_PATH, FILENAME))
img = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
# Rescale image -------------------------------------------------------------
(width, height) = (
    int(img.shape[1]*RESIZE_PCT/100),
    int(img.shape[0]*RESIZE_PCT/100)
)
dim = (width, height)
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
(height, width, depth) = resized.shape
##############################################################################
# Cluster for Dominance
##############################################################################
(frame, labels) = art.calcDominantColors(
    resized, cFun=SpectralClustering, cArgs={'n_clusters': CLST_NUM}
)
sortedLabels = [i[0] for i in Counter(labels).most_common()]
clusters = [frame[labels==i] for i in np.unique(sortedLabels)]
[art.rgb_to_hex(art.calcColorClusterCentroid(c)) for c in clusters]



    
['#6b6eb1', '#e8e0b0', '#633f58', '#bf8b77', '#949fcd', '#361d26']
['#6a73b5', '#dfab70', '#885981', '#9e9bca', '#4a2b3b', '#e7ddc2']