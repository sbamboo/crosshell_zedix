# Drawlib

## Drawlib is a simple CLI/TUI drawing library (renderer) made in python.

Author:  Simon Kalmi Claesson
* For version information see lib.json

### Files:
    __init__.py: Contains the renderer wrapper class. (As well as functioning as the package root)
    assets.py: Asset/TextureAsset rendering and handling functions.
    coloring.py: Mostly internal but contains functions and palettes for handling colors in drawlib.
    coreTypes.py: Contains classes for drawlibs OOP classes.
    legacy.py: Contains legacy functions and previous systems, now depricated or now having better alternatives.
    linedraw.py: Contains the main functions for drawing.
    pointGroupAlgorithms.py: Mostly internal but contains functions for included pointGroup generators.
    basicShapes.py: Contains classes for basic shapes.
    objects.py: Contains classes for shapes that uses the dataTypes to provide more features, tex: ImageManipulation with sprites.
    SimpleSpriteRenderer.py: Contains drawlibs simple spriteRenderer function.
    tools.py: Mostly internal but contains functions needed throughout drawlib.
    tui.py: Contains tui-specific utility-functions and likewise.
    imaging.py: Contains image rendering stuff.



### Examples:
#### Class Import
```
from drawlib import DrawlibRenderer
renderer = DrawlibRenderer()

renderer.fill_terminal(" ")
renderer.objects.circleObj("#",20,20,7,"f_red",renderer.stdpalette).draw()
renderer.basicShapes.circle("#",30,20,7,"f_blue",renderer.stdpalette).draw()
renderer.objects.pointObj("#",10,10,"f_magenta",renderer.stdpalette).draw()
renderer.objects.ellipseObj("#",70,15,15,5,"f_yellow",renderer.stdpalette).draw()
renderer.objects.quadBezierObj("#",30,30,0,0,50,0,"f_darkred",renderer.stdpalette).draw()
renderer.objects.cubicBezierObj("#",30,20,30,0,70,0,70,20).draw()
```

#### As Import
```
import drawlib as renderer

renderer.fill_terminal(" ")
renderer.objects.circleObj("#",20,20,7,"f_red",renderer.stdpalette).draw()
renderer.basicShapes.circle("#",30,20,7,"f_blue",renderer.stdpalette).draw()
renderer.objects.pointObj("#",10,10,"f_magenta",renderer.stdpalette).draw()
renderer.objects.ellipseObj("#",70,15,15,5,"f_yellow",renderer.stdpalette).draw()
renderer.objects.quadBezierObj("#",30,30,0,0,50,0,"f_darkred",renderer.stdpalette).draw()
renderer.objects.cubicBezierObj("#",30,20,30,0,70,0,70,20).draw()
```

#### Star Import
```
from drawlib import *

fill_terminal(" ")
objects.circleObj("#",20,20,7,"f_red",stdpalette).draw()
basicShapes.circle("#",30,20,7,"f_blue",stdpalette).draw()
objects.pointObj("#",10,10,"f_magenta",stdpalette).draw()
objects.ellipseObj("#",70,15,15,5,"f_yellow",stdpalette).draw()
objects.quadBezierObj("#",30,30,0,0,50,0,"f_darkred",stdpalette).draw()
objects.cubicBezierObj("#",30,20,30,0,70,0,70,20).draw()
```