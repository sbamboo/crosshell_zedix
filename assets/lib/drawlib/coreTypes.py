# [Imports]
from .linedraw import draw_point
from .coloring import autoNoneColor,getStdPalette

# [Variables]
stdpalette = getStdPalette()

# [Functions]
def pixelGroup_to_sprite(pixel_data, char="#", negChar=" "):
    if not pixel_data:
        return []
    min_x = min(pixel[0] for pixel in pixel_data)
    max_x = max(pixel[0] for pixel in pixel_data)
    min_y = min(pixel[1] for pixel in pixel_data)
    max_y = max(pixel[1] for pixel in pixel_data)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    rows = [[negChar for _ in range(width)] for _ in range(height)]
    for pixel in pixel_data:
        x, y = pixel
        rows[y - min_y][x - min_x] = char
    result = []
    for row in rows:
        result.append("".join(row))
    sprite = {"xPos":min_x, "yPos":min_y, "tx":result}
    return sprite

def cmpxPixelGroup_to_sprite(pixel_data, negChar=" "):
    lowest_x = min(pixel['pos'][0] for pixel in pixel_data)
    lowest_y = min(pixel['pos'][1] for pixel in pixel_data)
    normalized_pixels = [{'char': pixel['char'], 'pos': [pixel['pos'][0] - lowest_x, pixel['pos'][1] - lowest_y]} for pixel in pixel_data]
    width = max(pixel['pos'][0] for pixel in normalized_pixels) + 1
    height = max(pixel['pos'][1] for pixel in normalized_pixels) + 1
    grid = [[negChar for _ in range(width)] for _ in range(height)]
    for pixel in normalized_pixels:
        x, y = pixel['pos']
        char = pixel['char']
        grid[y][x] = char
    result = [''.join(row) for row in grid]
    sprite = {"xPos":lowest_x, "yPos":lowest_y, "tx":result}
    return sprite

def sprite_to_pixelGroup(sprite, char, exclusionChar):
    texture = sprite["tx"]
    xPos = sprite["xPos"]
    yPos = sprite["yPos"]
    pixels = []
    for y, row in enumerate(texture):
        for x, cell in enumerate(row):
            if cell != exclusionChar:
                pixels.append([x+xPos, y+yPos])
    return char, pixels

def sprite_to_cmpxPixelGroup(sprite, exclusionChar):
    texture = sprite["tx"]
    xPos = sprite["xPos"]
    yPos = sprite["yPos"]
    pixel_list = []
    for y, row in enumerate(texture):
        for x, char in enumerate(row):
            if char != exclusionChar:
                pixel = {"char": char, "pos": [x+xPos, y+yPos]}
                pixel_list.append(pixel)
    return pixel_list

def render_sprite(sprite,ansi=None):
    texture = sprite["tx"]
    xPos = sprite["xPos"]
    yPos = sprite["yPos"]
    print("\033[s") # Save cursorPos
    c = 0
    OposY = int(yPos)
    for line in texture:
        yPos = OposY + c
        ANSIprefix = "\033[" + str(yPos) + ";" + str(xPos) + "H"
        if ansi != None:
            ANSIprefix += "\033[" + str(ansi)
            if str(ansi).endswith("m") != True: ANSIprefix += "m"
        print(ANSIprefix, str(line), "\033[0m")
        c += 1
    print("\033[u\033[2A") # Load cursorPos

def render_pixelGroup(char,pixelGroup,ansi=None):
    for pixel in pixelGroup:
        draw_point(char,pixel[0],pixel[1],ansi=ansi)

def render_cmpxPixelGroup(cmpxPixelGroup,ansi=None):
    for pixel in cmpxPixelGroup:
        char = pixel["char"]
        pos = pixel["pos"]
        draw_point(char,pos[0],pos[1],ansi=ansi)

def pixelGroup_to_cmpxPixelGroup(char,pixelGroup):
    cmpxPixelGroup = []
    for pixel in pixelGroup:
        cmpxPixelGroup.append({"char":char,"pos":pixel})
    return cmpxPixelGroup

def cmpxPixelGroup_to_pixelGroup(char,cmpxPixelGroup):
    pixels = []
    for pixel in cmpxPixelGroup:
        pos = pixel["pos"]
        pixels.append(pos)
    return char,pixels

def texture_to_sprite(texture,xPos=0,yPos=0):
    return {"xPos":xPos, "yPos":yPos, "tx":texture.split("\n")}
def rawtexture_to_sprite(texture=list,xPos=0,yPos=0):
    return {"xPos":xPos, "yPos":yPos, "tx":texture}

def sprite_to_texture(sprite):
    return "\n".join(sprite["tx"])

def render_texture(xPos=0,yPos=0,texture=str,ansi=None):
    sprite = texture_to_sprite(texture,xPos,yPos)
    render_sprite(sprite,ansi=ansi)

# [Classes]
class pixelGroup():
    def __init__(self,char=str,pixels=list, color=None,palette=None):
        self.char = char
        self.pixels = pixels
        self.ansi = autoNoneColor(color,palette)
    def asPixelGroup(self):
        return self.char,self.pixels
    def asCmpxPixelGroup(self):
        return pixelGroup_to_cmpxPixelGroup(self.pixels)
    def asSprite(self,backgroundChar=" "):
        return pixelGroup_to_sprite(self.pixels,self.char,backgroundChar)
    def asTexture(self,backgroundChar=" "):
        sprite = pixelGroup_to_sprite(self.pixels,self.char,backgroundChar)
        return sprite_to_texture(sprite)
    def draw(self):
        render_pixelGroup(self.char,self.pixels,self.ansi)
    
class cmpxPixelGroup():
    def __init__(self,cmpxPixelGroup=list, color=None,palette=None):
        self.cmpxPixelGroup = cmpxPixelGroup
        self.ansi = autoNoneColor(color,palette)
    def asPixelGroup(self,char=str):
        return cmpxPixelGroup_to_pixelGroup(self.char,self.cmpxPixelGroup)
    def asCmpxPixelGroup(self):
        return self.cmpxPixelGroup
    def asSprite(self,backgroundChar=" "):
        return cmpxPixelGroup_to_sprite(self.cmpxPixelGroup,backgroundChar)
    def asTexture(self,backgroundChar=" "):
        sprite = cmpxPixelGroup_to_sprite(self.cmpxPixelGroup,backgroundChar)
        return sprite_to_texture(sprite)
    def draw(self):
        render_cmpxPixelGroup(self.cmpxPixelGroup,self.ansi)

class sprite():
    def __init__(self,xPos=None,yPos=None,spriteTexture=None,sprite=None, color=None,palette=None):
        if sprite != None:
            self.sprite = sprite
        else:
            if xPos == None or yPos == None or spriteTexture == None:
                raise ValueError("When not defining a sprite, al three variables must be defined: xPos, yPos, spriteTexture")
            self.sprite = {"xPos":xPos,"yPos":yPos,"tx":spriteTexture}
        self.ansi = autoNoneColor(color,palette)
    def asPixelGroup(self,char,exclusionChar):
        return sprite_to_pixelGroup(self.sprite,char,exclusionChar)
    def asCmpxPixelGroup(self,exclusionChar):
        return sprite_to_cmpxPixelGroup(self.sprite,exclusionChar)
    def asSprite(self):
        return self.sprite
    def asTexture(self):
        return sprite_to_texture(self.sprite)
    def draw(self):
        render_sprite(self.sprite,self.ansi)

class texture():
    def __init__(self,texture=str, color=None,palette=None):
        self.texture = texture
        self.ansi = autoNoneColor(color,palette)
    def asPixelGroup(self,char=str,xPos=0,yPos=0,exclusionChar=str):
        sprite = texture_to_sprite(xPos=xPos,yPos=yPos,texture=self.texture)
        return sprite_to_pixelGroup(sprite,char,exclusionChar)
    def asCmpxPixelGroup(self,char=str,xPos=0,yPos=0,exclusionChar=str):
        sprite = texture_to_sprite(xPos=xPos,yPos=yPos,texture=self.texture)
        return sprite_to_cmpxPixelGroup(sprite,char,exclusionChar)
    def asPixelGroup(self,xPos=0,yPos=0,exclusionChar=str):
        sprite = texture_to_sprite(xPos=xPos,yPos=yPos,texture=self.texture)
        return sprite_to_cmpxPixelGroup(sprite,exclusionChar)
    def asSprite(self,xPos=0,yPos=0):
        return texture_to_sprite(self.texture,xPos,yPos)
    def asTexture(self):
        return self.texture
    def draw(self,xPos=0,yPos=0):
        render_texture(xPos,yPos,self.texture,self.ansi)