#!/bin/bash

ARTISTS=( "Monet" "Kirchner" "Miro" )
###############################################################################
GRN='\033[0;32m'
NCL='\033[0m'
###############################################################################
for artist in ${ARTISTS[*]} 
do
    echo -e "${GRN}* Processing ${artist}${NCL}"
    bash fingerprintArt.sh "${artist}"
done
python exportDBReadme.py