# ArtSciColor

Creating a [python](https://www.python.org/) package with color palettes and utilities for their use in [matplotlib](https://matplotlib.org/), [seaborn](https://seaborn.pydata.org/), [plotly](https://plotly.com/python/), and others.

:construction: **WORK IN PROGRESS** :construction:


## Usage

To use a color palette simply load the package and run:

```bash
import ArtSciColor as art

hexPalette = art.getSwatch(SWATCH_ID)
```

where the `SWATCH_ID` should match one of the [palettes available](#available-palettes) in our package (see the following section for more info).

<a href='https://github.com/Chipdelmal/ArtSciColor/blob/main/ArtSciColor/swatches/Art.md'><img src="./ArtSciColor/media/demo_id.png" width='100%' align="middle"></a>


## Available Swatches

Have a look at currently-available palettes by selecting your favorite artist or category, and use one through its `ID`!

### [Art](./ArtSciColor/swatches/Art.md)

* [Miro](./ArtSciColor/swatches/Miro.md)
* [Nolde](./ArtSciColor/swatches/Nolde.md)
* [Kirchner](./ArtSciColor/swatches/Kirchner.md)
* [Warhol](./ArtSciColor/swatches/Kirchner.md)
* [Monet](./ArtSciColor/swatches/Monet.md)

<img src="./ArtSciColor/media/swatches/Art.png" height="30px" width='100%' align="middle"><br>

### [Movies](./ArtSciColor/swatches/Movies.md)

* [Studio Ghibli](./ArtSciColor/swatches/Ghibli.md)

<img src="./ArtSciColor/media/swatches/Movies.png" height="30px" width='100%' align="middle"><br>

### [Gaming](./ArtSciColor/swatches/Gaming.md)

* [Splatoon1](./ArtSciColor/swatches/Splatoon1.md)
* [Splatoon2](./ArtSciColor/swatches/Splatoon2.md)
* [Splatoon3](./ArtSciColor/swatches/Splatoon3.md)

<img src="./ArtSciColor/media/swatches/Gaming.png" height="30px" width='100%' align="middle"><br>

Full dataframe in CSV for available for download [here](./ArtSciColor/data/DB.csv)!

# Author and Notes

This package was initially inspired by [Blake R Mills'](https://github.com/BlakeRMills/MetBrewer) [R](https://www.r-project.org/about.html) packages ([MoMA Colors](https://github.com/BlakeRMills/MoMAColors) and [MetBrewer](https://github.com/BlakeRMills/MetBrewer)).

<img src="./ArtSciColor/media/about-pusheen.jpeg" height="150px" align="middle"><br>

[Héctor M. Sánchez C.](https://chipdelmal.github.io/)
