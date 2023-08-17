from . import assets
from . import coloring
from . import coreTypes
from . import legacy
from . import linedraw
from . import pointGroupAlgorithms
from . import basicShapes
from . import objects
from . import SimpleSpriteRenderer
from . import tools
from . import tui
from . import imaging

fill_terminal = linedraw.fill_terminal
stdpalette = coloring.getStdPalette()

class DrawlibRenderer():
    def __init__(self):
        self.assets = assets
        self.coloring = coloring
        self.coreTypes = coreTypes
        self.legacy = legacy
        self.linedraw = linedraw
        self.pointGroupAlgorithms = pointGroupAlgorithms
        self.basicShapes = basicShapes
        self.objects = objects
        self.simpleSpriteRenderer = SimpleSpriteRenderer
        self.tools = tools
        self.tui = tui
        self.stdpalette = stdpalette
        self.fill_terminal = linedraw.fill_terminal
        self.imaging = imaging
