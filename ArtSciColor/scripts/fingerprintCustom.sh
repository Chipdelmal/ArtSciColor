#!/bin/bash

ARTISTS_SPLATOON=( "Splatoon1" "Splatoon2" "Splatoon3")
ARTISTS=( "chipdelmal" "coolors" "lospec")
###############################################################################
GRN='\033[0;32m'
NCL='\033[0m'
###############################################################################
for artist in ${ARTISTS_SPLATOON[*]} 
do
    echo -e "${GRN}* Processing ${artist}${NCL}"
    python "$(dirname "$0")/splatoonSwatches.py" "${artist}"
done
###############################################################################
for artist in ${ARTISTS[*]} 
do
    echo -e "${GRN}* Processing ${artist}${NCL}"
    python "$(dirname "$0")/customSwatches.py" "${artist}"
done