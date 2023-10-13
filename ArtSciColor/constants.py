#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ArtSciColor.paths as pth
import ArtSciColor.auxiliary as aux

SWATCH_DIMS = {'width': 750, 'height': 50}
SWATCHES = aux.loadDatabase(pth.PTH_SWBZ, df=False)
SWATCHES_DF = aux.loadDatabase(pth.PTH_DBBZ, df=True)