
import matplotlib
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


def rgbToHex(rgb):
    return '#'+'%02x%02x%02x' % tuple([int(i*255) for i in rgb])


def hexToRgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))