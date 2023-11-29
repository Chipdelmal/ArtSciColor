#!/bin/bash

ARTISTS=(
    "UmbertoBoccioni" "DarbyBannard" "VanGogh" "Signac" "EdnaAndrade" 
    "Kandinsky" "Matisse" "Picasso" "Nolde" "Warhol" "Monet" "Kirchner" "Miro" 
    "Ghibli" "Disney"
)
###############################################################################
GRN='\033[0;32m'
NCL='\033[0m'
###############################################################################
for artist in ${ARTISTS[*]} 
do
    echo -e "${GRN}* Processing ${artist}${NCL}"
    bash "$(dirname "$0")/fingerprintArtist.sh" "${artist}"
    python "$(dirname "$0")/exportDBReadme.py" "${artist}"
done
###############################################################################
CATEGORIES=( "Art" "Movies" "Gaming" "Other" )
for cat in ${CATEGORIES[*]} 
do
    echo -e "${GRN}* Exporting README ${NCL}"
    python "$(dirname "$0")/exportDBReadme.py" "${cat}"
    python "$(dirname "$0")/swatchForReadme.py" "${cat}"
done