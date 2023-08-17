# [Imports]
from .linedraw import draw_point
from .coloring import autoNoneColor,getStdPalette

# [Variables]
stdpalette = getStdPalette()

# [Functions]
def pixelGroup_to_sprite(pixel_data, char="#", negChar=" "):
    # Return empty
    if not pixel_data:
        return []
    # Calculate minimum coords
    min_x = min(pixel[0] for pixel in pixel_data)
    max_x = max(pixel[0] for pixel in pixel_data)
    min_y = min(pixel[1] for pixel in pixel_data)
    max_y = max(pixel[1] for pixel in pixel_data)
    # Get some atributes
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    # fill in negChar's in rows
    rows = [[negChar for _ in range(width)] for _ in range(height)]
    # Add pixels by indexing
    for pixel in pixel_data:
        x, y = pixel
        rows[y - min_y][x - min_x] = char
    # Put the rows in the result
    result = []
    for row in rows:
        result.append("".join(row))
    # Create sprite and return it
    sprite = {"xPos":min_x, "yPos":min_y, "tx":result}
    return sprite

def cmpxPixelGroup_to_sprite(pixel_data, negChar=" "):
    # Sort out lowest values
    lowest_x = min(pixel['pos'][0] for pixel in pixel_data)
    lowest_y = min(pixel['pos'][1] for pixel in pixel_data)
    # Normalize the coordinates to top-left=0,0
    normalized_pixels = [{'char': pixel['char'], 'pos': [pixel['pos'][0] - lowest_x, pixel['pos'][1] - lowest_y]} for pixel in pixel_data]
    # Get some attributes
    width = max(pixel['pos'][0] for pixel in normalized_pixels) + 1
    height = max(pixel['pos'][1] for pixel in normalized_pixels) + 1
    # Made a grid from negChars
    grid = [[negChar for _ in range(width)] for _ in range(height)]
    # Fill in characters
    for pixel in normalized_pixels:
        x, y = pixel['pos']
        char = pixel['char']
        grid[y][x] = char
    # Put the rows in the result
    result = [''.join(row) for row in grid]
    # Create sprite and return it
    sprite = {"xPos":lowest_x, "yPos":lowest_y, "tx":result}
    return sprite

def sprite_to_pixelGroup(sprite, char, exclusionChar):
    # Get sprite data
    texture = sprite["tx"]
    xPos = sprite["xPos"]
    yPos = sprite["yPos"]
    # Check each cell, if not exlChar add to pixelGroup
    pixels = []
    for y, row in enumerate(texture):
        for x, cell in enumerate(row):
            if cell != exclusionChar:
                pixels.append([x+xPos, y+yPos])
    # Return
    return char, pixels

def sprite_to_cmpxPixelGroup(sprite, exclusionChar):
    # Get sprite data
    texture = sprite["tx"]
    xPos = sprite["xPos"]
    yPos = sprite["yPos"]
    pixel_list = []
    # Check each cell, if not exlChar add char and pos to cmpxPixelGroup
    for y, row in enumerate(texture):
        for x, char in enumerate(row):
            if char != exclusionChar:
                pixel = {"char": char, "pos": [x+xPos, y+yPos]}
                pixel_list.append(pixel)
    # Return
    return pixel_list

def render_sprite(sprite,ansi=None):
    # Get sprite data
    texture = sprite["tx"]
    xPos = sprite["xPos"]
    yPos = sprite["yPos"]
    # Use a modified sprite renderer
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
    # Draw points
    for pixel in pixelGroup:
        draw_point(char,pixel[0],pixel[1],ansi=ansi)

def render_cmpxPixelGroup(cmpxPixelGroup,ansi=None):
    # Get points and draw them
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
def listTexture_to_sprite(texture=list,xPos=0,yPos=0):
    return {"xPos":xPos, "yPos":yPos, "tx":texture}

def sprite_to_texture(sprite):
    return "\n".join(sprite["tx"])

def render_texture(xPos=0,yPos=0,texture=str,ansi=None):
    # Convert to sprite and render
    sprite = texture_to_sprite(texture,xPos,yPos)
    render_sprite(sprite,ansi=ansi)
def render_listTexture(xPos=0,yPos=0,texture=list,ansi=None):
    # Convert to sprite and render
    sprite = listTexture_to_sprite(texture,xPos,yPos)
    render_sprite(sprite,ansi=ansi)

def pixelStrip_to_cmpxPixelGroup(pixelStrip=dict):
    pixels = pixelStrip["po"]
    chars = list(pixelStrip["st"])
    cmpxPixelGroup = []
    for i,char in enumerate(chars):
        cmpxPixelGroup.append( {"char":char,"pos":pixels[i]} )
    return cmpxPixelGroup

def cmpxPixelGroup_to_pixelStrip(cmpxPixelGroup):
    strip = ""
    poss = []
    for pGroup in cmpxPixelGroup:
        strip += pGroup["char"]
        poss.append(pGroup["pos"])
    return {"st":strip,"po":poss}

def render_pixelStrip(pixelStrip=dict,ansi=None):
    cmpxPixelGroup = pixelStrip_to_cmpxPixelGroup(pixelStrip)
    render_cmpxPixelGroup(cmpxPixelGroup,ansi=ansi)

# [Classes]
# Theese classes are to allow more methods and conversions to bee avaliable between the dataTypes using the functions above.
# And have a few standard methods: asPixelGroup, asCmpxPixelGroup, asSprite, asTexture, draw
# (These take arguments if the conversion/method is missing parameters)

class pixelGroup():
    def __init__(self,char=str,pixels=list, color=None,palette=None):
        self.char = char
        self.pixels = pixels
        self.ansi = autoNoneColor(color,palette)
    def asPixelGroup(self):
        return self.char,self.pixels
    def asCmpxPixelGroup(self):
        return pixelGroup_to_cmpxPixelGroup(self.char,self.pixels)
    def asSprite(self,backgroundChar=" "):
        return pixelGroup_to_sprite(self.pixels,self.char,backgroundChar)
    def asTexture(self,backgroundChar=" "):
        sprite = pixelGroup_to_sprite(self.pixels,self.char,backgroundChar)
        return sprite_to_texture(sprite)
    def asPixelStrip(self,exclusionChar=" "):
        cmpxPixelGroup = pixelGroup_to_cmpxPixelGroup(self.char,self.pixels)
        return cmpxPixelGroup_to_pixelStrip(cmpxPixelGroup)
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
    def asPixelStrip(self,exclusionChar=" "):
        return cmpxPixelGroup_to_pixelStrip(self.cmpxPixelGroup)
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
    def asPixelGroup(self,char,exclusionChar=" "):
        return sprite_to_pixelGroup(self.sprite,char,exclusionChar)
    def asCmpxPixelGroup(self,exclusionChar=" "):
        return sprite_to_cmpxPixelGroup(self.sprite,exclusionChar)
    def asSprite(self):
        return self.sprite
    def asTexture(self):
        return sprite_to_texture(self.sprite)
    def asPixelStrip(self,exclusionChar=" "):
        cmpxPixelGroup = sprite_to_cmpxPixelGroup(self.sprite, exclusionChar)
        return cmpxPixelGroup_to_pixelStrip(cmpxPixelGroup)
    def draw(self):
        render_sprite(self.sprite,self.ansi)

class texture():
    def __init__(self,texture=str, color=None,palette=None):
        self.texture = texture
        self.ansi = autoNoneColor(color,palette)
    def asPixelGroup(self,char=str,xPos=0,yPos=0,exclusionChar=" "):
        sprite = texture_to_sprite(xPos=xPos,yPos=yPos,texture=self.texture)
        return sprite_to_pixelGroup(sprite,char,exclusionChar)
    def asCmpxPixelGroup(self,char=str,xPos=0,yPos=0,exclusionChar=" "):
        sprite = texture_to_sprite(xPos=xPos,yPos=yPos,texture=self.texture)
        return sprite_to_cmpxPixelGroup(sprite,char,exclusionChar)
    def asSprite(self,xPos=0,yPos=0):
        return texture_to_sprite(self.texture,xPos,yPos)
    def asTexture(self):
        return self.texture
    def asPixelStrip(self,exclusionChar=" "):
        sprite = texture_to_sprite(xPos=xPos,yPos=yPos,texture=self.texture)
        cmpxPixelGroup = sprite_to_cmpxPixelGroup(sprite, exclusionChar)
        return cmpxPixelGroup_to_pixelStrip(cmpxPixelGroup)
    def draw(self,xPos=0,yPos=0):
        render_texture(xPos,yPos,self.texture,self.ansi)

class pixelStrip():
    def __init__(self,strip=None,positions=None,pixelStrip=None, color=None,palette=None):
        if strip != None:
            if isinstance(strip, str) != True: raise ValueError("Strip must be a string!")
        if positions != None:
            if isinstance(positions, list) != True: raise ValueError("Positions must be a list!")
        if pixelStrip != None:
            if isinstance(pixelStrip, list) != True: raise ValueError("PixelStrip must be a dict!")
        self.strip = strip
        self.positions = positions
        if pixelStrip != None:
            self.strip = pixelStrip["st"]
            self.positions = pixelStrip["po"]
        self.ansi = autoNoneColor(color,palette)
    def asPixelGroup(self):
        return self.positions
    def asCmpxPixelGroup(self):
        pixelStrip_to_cmpxPixelGroup({"st":self.strip,"po":self.positions})
    def asSprite(self,exclusionChar=" "):
        cmpxPixelGroup = pixelStrip_to_cmpxPixelGroup({"st":self.strip,"po":self.positions})
        return cmpxPixelGroup_to_sprite(cmpxPixelGroup,exclusionChar)
    def asTexture(self,exclusionChar=" "):
        cmpxPixelGroup = pixelStrip_to_cmpxPixelGroup({"st":self.strip,"po":self.positions})
        sprite = cmpxPixelGroup_to_sprite(cmpxPixelGroup,exclusionChar)
        return sprite_to_texture(sprite)
    def asPixelStrip(self):
        return {"st":self.strip,"po":self.positions}
    def draw(self):
        render_pixelStrip(pixelStrip,self.ansi)