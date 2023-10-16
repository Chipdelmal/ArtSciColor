#!/bin/bash

ARTISTS=( "Ghibli" "Nolde" "Warhol" "Monet" "Kirchner" "Miro" )
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
echo -e "${GRN}* Exporting README ${NCL}"
python "$(dirname "$0")/exportDBReadme.py" "Art"
python "$(dirname "$0")/exportDBReadme.py" "Movies"
python "$(dirname "$0")/exportDBReadme.py" "Gaming"
python "$(dirname "$0")/exportDBReadme.py" "Other"
###############################################################################
echo -e "${GRN}* Exporting README swatches ${NCL}"
python "$(dirname "$0")/swatchForReadme.py" "Art"
python "$(dirname "$0")/swatchForReadme.py" "Movies"
python "$(dirname "$0")/swatchForReadme.py" "Gaming"
python "$(dirname "$0")/swatchForReadme.py" "Other"