from .imageRenderer.ImageRenderer_Beta import ImageRenderer
from .coreTypes import render_listTexture

class asciiImage():
    def __init__(self,imagePath=str,mode="standard",char=None,pc=False,method="lum",invert=False,monochrome=False,width=None,height=None,resampling="lanczos",textureCodec=None,xPos=None,yPos=None):
        # Req Arguments
        self.imagePath = imagePath
        # Presets
        self.type = "ascii"
        self.texture = None
        # Set other arguments
        self.mode = mode
        self.char = char
        self.pc = pc
        self.method = method
        self.invert = invert
        self.monochrome = monochrome
        self.width = width
        self.height = height
        self.resampling = resampling
        self.textureCodec = textureCodec
        self.xPos = xPos
        self.yPos = yPos
    def _getTexture(self,asTexture=True):
        self.texture = ImageRenderer(image=self.imagePath,type=self.type,mode=self.mode,char=self.char,pc=self.pc,method=self.method,invert=self.invert,monochrome=self.monochrome,width=self.width,height=self.height,resampling=self.resampling,textureCodec=self.textureCodec, asTexture=asTexture,colorMode="pythonAnsi")
    def resize(self,width=int,height=int,resampling=None):
        if resampling != None: self.resampling = resampling
        self.width = width
        self.height = height
        self.texture = None
    def print(self):
        self._getTexture(asTexture=False)
        self.texture = None
    def asTexture(self):
        if self.texture == None: self._getTexture()
        return self.texture
    def draw(self,xPos=None,yPos=None):
        if xPos == None: xPos = self.xPos
        if xPos == None: raise ValueError("xPos not defined!")
        if yPos == None: yPos = self.yPos
        if yPos == None: raise ValueError("yPos not defined!")
        if self.texture == None: self._getTexture()
        render_listTexture(xPos,yPos,texture)

class boxImage():
    def __init__(self,imagePath=str,mode="foreground",char=None,monochrome=False,width=None,height=None,resampling="lanczos",textureCodec=None,xPos=None,yPos=None):
        # Req Arguments
        self.imagePath = imagePath
        # Presets
        self.type = "box"
        self.texture = None
        # Set other arguments
        self.mode = mode
        self.char = char
        self.monochrome = monochrome
        self.width = width
        self.height = height
        self.resampling = resampling
        self.textureCodec = textureCodec
        self.xPos = xPos
        self.yPos = yPos
    def _getTexture(self,asTexture=True):
        self.texture = ImageRenderer(image=self.imagePath,type=self.type,mode=self.mode,char=self.char,monochrome=self.monochrome,width=self.width,height=self.height,resampling=self.resampling,textureCodec=self.textureCodec, asTexture=asTexture,colorMode="pythonAnsi")
    def resize(self,width=int,height=int,resampling=None):
        if resampling != None: self.resampling = resampling
        self.width = width
        self.height = height
        self.texture = None
    def print(self):
        self._getTexture(asTexture=False)
        self.texture = None
    def asTexture(self):
        if self.texture == None: self._getTexture()
        return self.texture
    def draw(self,xPos=None,yPos=None):
        if xPos == None: xPos = self.xPos
        if xPos == None: raise ValueError("xPos not defined!")
        if yPos == None: yPos = self.yPos
        if yPos == None: raise ValueError("yPos not defined!")
        if self.texture == None: self._getTexture()
        render_listTexture(xPos,yPos,self.texture)