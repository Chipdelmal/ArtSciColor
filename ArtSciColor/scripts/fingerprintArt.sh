#!/bin/bash

ARTIST="Kirchner"
###############################################################################
# Path Constants
###############################################################################
ITER_FILE="$HOME/Documents/GitHub/ArtSciColor/ArtSciColor/data/${ARTIST}.csv"
PTH_I="$HOME/Pictures/ArtSci/${ARTIST}/in/"
PTH_O="$HOME/Pictures/ArtSci/${ARTIST}/out/"
###############################################################################
# Color Constants
###############################################################################
LG='\033[1;34m'
NC='\033[0m'
###############################################################################
# Paintings Iterator
###############################################################################
while IFS=, read -r CNUM FNAME TITLE LINK; do 
    printf "${LG}* ${TITLE} "
    # echo "Clusters $CNUM :: Filename $FNAME :: Title $TITLE :: Link $LINK"; 
    outputString=$(python fprintPainting.py ${PTH_I} ${PTH_O} ${FNAME} ${CNUM})
    printf "${outputString}"
  done < $ITER_FILE