
import colorsys
import colorir as cir
from colour import Color
from matplotlib import font_manager
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap


def addHexOpacity(colors, alpha='1A'):
    return [c+alpha for c in colors]


def replaceHexOpacity(colors, alpha='FF'):
    return [i[:-2]+alpha for i in colors]


def generateAlphaColorMapFromColor(color):
    alphaMap = LinearSegmentedColormap.from_list(
        'cmap',
        [(0.0, 0.0, 0.0, 0.0), color],
        gamma=0
    )
    return alphaMap


def colorPaletteFromHexList(clist):
    c = mcolors.ColorConverter().to_rgb
    clrs = [c(i) for i in clist]
    rvb = mcolors.LinearSegmentedColormap.from_list("", clrs)
    return rvb


def sortSwatchByFrequency(freqSwatch):
    freqSwatch.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb[0].get_rgb()))
    swatchHex = [s[0] for s in freqSwatch]
    return swatchHex


def sortSwatchHSV(
        freqSwatch,
        hue_classes=None, gray_thresh=255, 
        gray_start=True, alt_lum=True, invert_lum=False
    ):
    swatchHex = [s[0].hex for s in freqSwatch]
    swatchHex.sort(
        key=cir.hue_sort_key(
            hue_classes=hue_classes, gray_thresh=gray_thresh,
            gray_start=gray_start, alt_lum=alt_lum, invert_lum=invert_lum
        )
    )
    swatchHex = [Color(c) for c in swatchHex]
    return swatchHex


def getTextColor(hexBackground, threshold=0.55):
    (r, g, b) = hexBackground.rgb
    tcol = (0, 0, 0) if (r*0.299+g*0.587+b*0.114)>threshold else (1, 1, 1)
    return Color(rgb=tcol)


def getFontFile(family, weight='regular'):
    font = font_manager.FontProperties(family=family, weight=weight)
    file = font_manager.findfont(font)
    return file