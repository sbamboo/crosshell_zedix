from .coloring import autoNoneColor,getStdPalette
from .coreTypes import *
from .pointGroupAlgorithms import *
from .assets import *

# Get stdpalette
stdpalette = getStdPalette()

# Base-class to inherit from. Contains pixelGenerator and objectcreator
class drawlibObj():
    def __init__(self,char,color=None,palette=stdpalette):
        self.char = char
        self.genData = {} # SHOULD BE FILLED IN BY SUBCLASS
        self.drawData = {
            "color": color,
            "palette": palette
        }
        self.pixels = None
        self.pixelGroup = None
    def generate(self):
        pass # THIS SHOULD BE REPLACED IN SUBCLASS
    def objectify(self):
        color = self.drawData["color"]
        palette = self.drawData["palette"]
        self.pixelGroup = pixelGroup(self.char,self.pixels,color,palette)
    def make(self):
        if self.pixels == None: self.generate()
        if self.pixelGroup == None: self.objectify()
    def clear(self):
        self.pixels = None
        self.pixelGroup = None
    # Conversion Methods
    def asPixelGroup(self):
        if self.pixelGroup == None: self.make()
        return self.pixelGroup.asPixelGroup()
    def asCmpxPixelGroup(self):
        if self.pixelGroup == None: self.make()
        return self.pixelGroup.asCmpxPixelGroup()
    def asSprite(self,backgroundChar=" "):
        if self.pixelGroup == None: self.make()
        return self.pixelGroup.asSprite(backgroundChar)
    def asTexture(self,backgroundChar=" "):
        if self.pixelGroup == None: self.make()
        sprite = self.pixelGroup.asSprite(backgroundChar)
        return sprite_to_texture(sprite)
    # Draw
    def draw(self):
        if self.pixelGroup == None: self.make()
        self.pixelGroup.draw()
        return self

# Template object for custom generator function to be added by user
# template =  templateDrawlibObj(char="#")
# def customGenerator(self,x1,y1):
#     return [[x,y],[x,y],[x,y]]
# template._customGenerator = customGenerator
# template.draw()
class temlateDrawlibObj(drawlibObj):
    def __init__(self,char,color=None,palette=stdpalette,autoGenerate=False,autoDraw=False,**kwargs):
        super().__init__(char, color, palette)
        self.genData = kwargs
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def _customGenerator():
        raise Exception("templateDrawlibObj's must have a custom generate function defined (the '_customGenerator' method), that also takes the needed points and arguments to set 'self.pixels' to a pixelGroup")
    def generate(self,*args,**kwargs):
        self.pixels = self._customGenerator(*args,**kwargs)

# Drawlib objects:
class pointObj(drawlibObj):
    def __init__(self,char,x1,y1,color=None,palette=stdpalette,autoGenerate=False,autoDraw=False):
        super().__init__(char, color, palette)
        self.genData = {
            "x1": x1,
            "y1": y1
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        self.pixels = [[self.genData["x1"],self.genData["y1"]]]

class lineObj(drawlibObj):
    def __init__(self,char,x1,y1,x2,y2,color=None,palette=stdpalette,autoGenerate=False,autoDraw=False):
        super().__init__(char, color, palette)
        self.genData = {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        self.pixels = beethams_line_algorithm(**self.genData)

class triangleObj(drawlibObj):
    def __init__(self,char,x1,y1,x2,y2,x3,y3,color=None,palette=stdpalette,autoGenerate=False,autoDraw=False):
        super().__init__(char, color, palette)
        self.drawData = {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "x3": x3,
            "y3": y3
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        p1 = [self.genData["x1"],self.genData["y1"]]
        p2 = [self.genData["x2"],self.genData["y2"]]
        p3 = [self.genData["x3"],self.genData["y3"]]
        self.pixels =       beethams_line_algorithm(*p1,*p2)
        self.pixels.extend( beethams_line_algorithm(*p1,*p3) )
        self.pixels.extend( beethams_line_algorithm(*p2,*p3) )

class rectangleObj(drawlibObj):
    def __init__(self,char,x1,y1,x2,y2,x3,y3,x4,y4,color=None,palette=stdpalette,autoGenerate=False,autoDraw=False):
        super().__init__(char, color, palette)
        self.genData = {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "x3": x3,
            "y3": y3,
            "x4": x4,
            "y4": y4
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        p1 = [self.genData["x1"],self.genData["y1"]]
        p2 = [self.genData["x2"],self.genData["y2"]]
        p3 = [self.genData["x3"],self.genData["y3"]]
        p4 = [self.genData["x4"],self.genData["y4"]]
        self.pixels =       beethams_line_algorithm(*p1, *p2)
        self.pixels.extend( beethams_line_algorithm(*p2,*p3) )
        self.pixels.extend( beethams_line_algorithm(*p3,*p4) )
        self.pixels.extend( beethams_line_algorithm(*p4,*p1) )

class rectangleObj2(drawlibObj):
    def __init__(self,char,c1,c2,color=None,palette=stdpalette,autoGenerate=False,autoDraw=False):
        super().__init__(char, color, palette)
        self.genData = {
            "c1": c1,
            "c2": c2
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        c1x = self.genData["c1"][0]
        c1y = self.genData["c1"][1]
        c2x = self.genData["c2"][0]
        c2y = self.genData["c2"][1]
        p1 = [c1x,c1y]
        p2 = [c2x,c1y]
        p3 = [c2x,c2y]
        p4 = [c1x,c2y]
        self.pixels =       beethams_line_algorithm(*p1, *p2)
        self.pixels.extend( beethams_line_algorithm(*p2,*p3) )
        self.pixels.extend( beethams_line_algorithm(*p3,*p4) )
        self.pixels.extend( beethams_line_algorithm(*p4,*p1) )
        self.pixels = beethams_line_algorithm(**self.genData)

class circleObj(drawlibObj):
    def __init__(self, char, xM, yM, r, color=None,palette=stdpalette,autoGenerate=False,autoDraw=False):
        super().__init__(char, color, palette)
        self.genData = {
            "xM": xM,
            "yM": yM,
            "r": r
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        self.pixels = beethams_circle_algorithm(x_center=self.genData["xM"],y_center=self.genData["yM"],radius=self.genData["r"])

class ellipseObj(drawlibObj):
    def __init__(self, char, cX, cY, xRad, yRad, color=None,palette=stdpalette,autoGenerate=False,autoDraw=False):
        super().__init__(char, color, palette)
        self.genData = {
            "cX": cX,
            "cY": cY,
            "xRad": xRad,
            "yRad": yRad
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        self.pixels = beethams_ellipse_algorithm(self.genData["cX"],self.genData["cY"],xRadius=self.genData["xRad"],yRadius=self.genData["yRad"])

class quadBezierObj(drawlibObj):
    def __init__(self, char, sX,sY, cX,cY, eX,eY, color=None,palette=stdpalette,autoGenerate=False,autoDraw=False):
        super().__init__(char, color, palette)
        self.genData = {
            "x0": sX,
            "y0": sY,
            "x1": cX,
            "y1": cY,
            "x2": eX,
            "y2": eY
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        self.pixels = generate_quadratic_bezier(**self.genData)

class cubicBezierObj(drawlibObj):
    def __init__(self, char, sX,sY, c1X,c1Y, c2X,c2Y, eX,eY, algorithm="step",modifier=None, color=None,palette=stdpalette,autoGenerate=False,autoDraw=False):
        '''
        Alogrithm: "step" or "point"
        Modifier: With step algorithm, def: 0.01; With point algorithm, def: 100
        '''
        super().__init__(char, color, palette)
        self.genData = {
            "sX": sX,
            "sY": sY,
            "c1X": c1X,
            "c1Y": c1Y,
            "c2X": c2X,
            "c2Y": c2Y,
            "eX": eX,
            "eY": eY,
            "algorithm": algorithm,
            "modifier": modifier
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        self.pixels = generate_cubic_bezier(**self.genData)

# Assets classes are not based on the same dataType as the baseClass above to they get their own classes (these are based on sprites)
# But works the same.
class assetFileObj():
    def __init__(self, filepath, color=None,palette=stdpalette,autoGenerate=False,autoDraw=False):
        self.filepath = filepath
        self.drawData = {
            "color": color,
            "palette": palette
        }
        self.sprite = None
        self.spriteObj = None
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        # make texture
        posX,posY,texture,color = load_asset(self.filepath)
        # color
        if self.color == None:
            self.color = color
        # make sprite (NonClass)
        self.sprite = rawtexture_to_sprite(texture,xPos=posX,yPos=posY)
    def objectify(self):
        color = self.drawData["color"]
        palette = self.drawData["palette"]
        self.spriteObj = sprite(sprite=self.spriteObj,color=color,palette=palette)
    def make(self):
        if self.sprite == None: self.generate()
        if self.spriteObj == None: self.objectify()
    def clear(self):
        self.sprite = None
        self.spriteObj = None
    def asPixelGroup(self,char,exclusionChar=" "):
        if self.spriteObj == None: self.make()
        return self.spriteObj.asPixelGroup(char,exclusionChar)
    def asCmpxPixelGroup(self,exclusionChar=" "):
        if self.spriteObj == None: self.make()
        return self.spriteObj.asCmpxPixelGroup(exclusionChar)
    def asSprite(self):
        if self.spriteObj == None: self.make()
        return self.spriteObj.asSprite()
    def asTexture(self):
        if self.spriteObj == None: self.make()
        return sprite_to_texture(self.sprite)
    def draw(self):
        if self.spriteObj == None: self.make()
        self.spriteObj.draw()
        return self
    
class assetTexture():
    def __init__(self, filepath, color=None,palette=stdpalette,autoGenerate=False,autoDraw=False):
        self.filepath = filepath
        self.drawData = {
            "color": color,
            "palette": palette
        }
        self.texture = None
        self.textureObj = None
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        self.texture = load_texture(self.filepath)
    def objectify(self):
        color = self.drawData["color"]
        palette = self.drawData["palette"]
        self.textureObj = texture(texture=self.texture,color=color,palette=palette)
    def make(self):
        if self.texture == None: self.generate()
        if self.textureObj == None: self.objectify()
    def clear(self):
        self.texture = None
        self.textureObj = None
    def asPixelGroup(self,char,xPos=0,yPos=0,exclusionChar=" "):
        if self.textureObj == None: self.make()
        return self.textureObj.asPixelGroup(char,xPos,yPos,exclusionChar)
    def asCmpxPixelGroup(self,char,xPos=0,yPos=0,exclusionChar=" "):
        if self.textureObj == None: self.make()
        return self.textureObj.asCmpxPixelGroup(char,xPos,yPos,exclusionChar)
    def asSprite(self,xPos=0,yPos=0):
        if self.textureObj == None: self.make()
        return self.textureObj.asSprite(xPos,yPos)
    def asTexture(self):
        if self.textureObj == None: self.make()
        return sprite_to_texture(self.sprite)
    def draw(self,xPos=0,yPos=0):
        if self.textureObj == None: self.make()
        self.textureObj.draw(xPos,yPos)
        return self