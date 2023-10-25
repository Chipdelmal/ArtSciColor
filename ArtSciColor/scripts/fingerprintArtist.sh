#!/bin/bash

ARTIST=$1
###############################################################################
# Path Constants
###############################################################################
DATA_PATH="$HOME/Documents/GitHub/ArtSciColor/ArtSciColor/data"
ITER_FILE="${DATA_PATH}/${ARTIST}.csv"
PTH_I="${DATA_PATH}/sources/${ARTIST}/in/"
PTH_O="${DATA_PATH}/sources/${ARTIST}/out/"
###############################################################################
# Color Constants
###############################################################################
LG='\033[1;34m'
NC='\033[0m'
###############################################################################
# Paintings Iterator
###############################################################################
while IFS=, read -r CNUM FNAME TITLE LINK; do 
    printf "${LG}\t${TITLE} "
    outputString=$(
        python "$(dirname "$0")/fprintPainting.py" \
            ${PTH_I} ${PTH_O} ${FNAME} \
            ${CNUM} \
            "${LINK}" "${ARTIST}" "${TITLE}"
    )
    printf "${outputString}"
  done < $ITER_FILE