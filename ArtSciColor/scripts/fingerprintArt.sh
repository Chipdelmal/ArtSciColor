#!/bin/bash

ARTISTS=( "Warhol" "Monet" "Kirchner" "Miro" )
###############################################################################
GRN='\033[0;32m'
NCL='\033[0m'
###############################################################################
for artist in ${ARTISTS[*]} 
do
    echo -e "${GRN}* Processing ${artist}${NCL}"
    bash "$(dirname "$0")/fingerprintArtist.sh" "${artist}"
done
python "$(dirname "$0")/exportDBReadme.py"