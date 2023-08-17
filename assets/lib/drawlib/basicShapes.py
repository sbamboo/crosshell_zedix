from .linedraw import *
from .coloring import autoNoneColor,getStdPalette

# Helper function to check the type of an object if its a type
def _isPoint(obj):
    if isinstance(obj,list) or isinstance(obj,point): return True
    else: return False

# Import the stdPalette from coloring
stdpalette = getStdPalette()

# Classes are for the ease of use of the basic shapes, they build on the linedrawing functions, which builds on pixelGroups, thus they take 'char'.
# They also take the generatorCoordinates and lastly some standard arguments:
# 'color':    Being a paletteKey.
# 'palette':  The palette to use, def drawlib.coloring.stdpalette.
# 'autoDraw': Auto calls the drawing method when classInstance is created.

class point():
    def __init__(self,char,x1,y1,color=None,palette=stdpalette,autoDraw=False):
        self.char = char
        self.x1 = x1
        self.y1 = y1
        self.ansi = autoNoneColor(color,palette)
        if autoDraw == True: self.draw()
    # Use the linedraw.draw_point function
    def draw(self):
        draw_point(self.char,self.x1,self.y1,self.ansi)

class line():
    def __init__(self,char,x1,y1,x2,y2,color=None,palette=stdpalette,autoDraw=False):
        self.char = char
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.ansi = autoNoneColor(color,palette)
        if autoDraw == True: self.draw()
    def draw(self):
        draw_line(self.char,self.x1,self.y1,self.x2,self.y2,self.ansi)

class triangle():
    def __init__(self,char,x1,y1,x2,y2,x3,y3,color=None,palette=stdpalette,autoDraw=False):
        self.char = char
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.ansi = autoNoneColor(color,palette)
        if autoDraw == True: self.draw()
    def draw(self):
        draw_triangle_coords(self.char,self.x1,self.y1,self.x2,self.y2,self.x3,self.y3,self.ansi)

class rectangle():
    def __init__(self,char,x1,y1,x2,y2,x3,y3,x4,y4,color=None,palette=stdpalette,autoDraw=False):
        self.char = char
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4
        self.ansi = autoNoneColor(color,palette)
        if autoDraw == True: self.draw()
    def draw(self):
        draw_line(self.char, self.x1,self.y1, self.x2,self.y2, self.ansi)
        draw_line(self.char, self.x2,self.y2, self.x3,self.y3, self.ansi)
        draw_line(self.char, self.x3,self.y3, self.x4,self.y4, self.ansi)
        draw_line(self.char, self.x4,self.y4, self.x1,self.y1, self.ansi)

class rectangle2():
    def __init__(self, char, c1, c2,color=None,palette=stdpalette,autoDraw=False):
        if _isPoint(c1) == False or _isPoint(c2) == False:
            raise ValueError("c1 and c2 must be points or lists of coords.")
        self.char = char
        self.c1 = c1
        self.c2 = c2
        self.ansi = autoNoneColor(color,palette)
        if autoDraw == True: self.draw()
    def draw(self):
        c1x = self.c1[0]
        c1y = self.c1[1]
        c2x = self.c2[0]
        c2y = self.c2[1]
        p1 = [c1x,c1y]
        p2 = [c2x,c1y]
        p3 = [c2x,c2y]
        p4 = [c1x,c2y]
        draw_line(self.char,*p1,*p2,self.ansi)
        draw_line(self.char,*p2,*p3,self.ansi)
        draw_line(self.char,*p3,*p4,self.ansi)
        draw_line(self.char,*p4,*p1,self.ansi)

class circle():
    def __init__(self, char, xM, yM, r, color=None,palette=stdpalette,autoDraw=False):
        self.char = char
        self.xM = xM
        self.yM = yM
        self.r = r
        self.ansi = autoNoneColor(color,palette)
        if autoDraw == True: self.draw()
    def draw(self):
        draw_circle(self.char,self.xM,self.yM,self.r,ansi=self.ansi)

class ellipse():
    def __init__(self, char, cX, cY, xRad, yRad, color=None,palette=stdpalette,autoDraw=False):
        self.char = char
        self.cX = cX
        self.cY = cY
        self.xRad = xRad
        self.yRad = yRad
        self.ansi = autoNoneColor(color,palette)
        if autoDraw == True: self.draw()
    def draw(self):
        draw_ellipse(self.char,self.cX,self.cY,self.xRad,self.yRad,self.ansi)

class quadBezier():
    def __init__(self, char, sX, sY, cX, cY, eX, eY, color=None,palette=stdpalette,autoDraw=False):
        self.char = char
        self.sX = sX
        self.sY = sY
        self.cX = cX
        self.cY = cY
        self.eX = eX
        self.eY = eY
        self.ansi = autoNoneColor(color,palette)
        if autoDraw == True: self.draw()
    def draw(self):
        draw_quadBezier(self.char,self.sX,self.sY,self.cX,self.cY,self.eX,self.eY,self.ansi)

class cubicBezier():
    def __init__(self, char, sX, sY, c1X, c1Y, c2X, c2Y, eX, eY, algorithm="step",modifier=None, color=None,palette=None,autoDraw=False):
        '''
        Alogrithm: "step" or "point"
        Modifier: With step algorithm, def: 0.01; With point algorithm, def: 100
        '''
        self.char = char
        self.sX = sX
        self.sY = sY
        self.c1X = c1X
        self.c1Y = c1Y
        self.c2X = c2X
        self.c2Y = c2Y
        self.eX = eX
        self.eY = eY
        self.algorithm = algorithm
        self.modifier = modifier
        self.ansi = autoNoneColor(color,palette)
        if autoDraw == True: self.draw()
    def draw(self):
        draw_cubicBezier(self.char,self.sX,self.sY,self.c1X,self.c1Y,self.c2X,self.c2Y,self.eX,self.eY,self.algorithm,self.modifier,self.ansi)

        