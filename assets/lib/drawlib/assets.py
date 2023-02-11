import re
from assets.lib.drawlib.internal import *

# De tokenising function (Variables in string)
def deTokenize(string):
	# Get tokens
	prepLine = str(string)
	tokens = re.findall(r'%.*?%',prepLine)
	# Get variable from token name and replace the token with the variables value
	for token in tokens:
		token = str(token)
		var = token.replace('%','')
		value = str(globals()[var])
		string = string.replace(token,value)
	# Return de-tokenised string
	return string


# Function to load a texture file to a list of texture_lines
def load_texture(filepath):
	# Get content from file
	rawContent = open(filepath, 'r', encoding="utf-8").read()
	splitContent = rawContent.split("\n")
	# Fix empty last-line issue
	if splitContent[-1] == "":
		splitContent.pop(-1)
	# Return content as a list
	return splitContent


# Asset loader loading a texture and texture-info from an asset file
def load_asset(filepath):
	# Get content from file
	rawContent = open(filepath, 'r', encoding="utf-8").read()
	splitContent = rawContent.split("\n") # Line splitter
	# Get asset configuration from file
	configLine = (splitContent[0]).split("#")[0]
	configLine_split = configLine.split(";")
	posX = configLine_split[0]
	posY = configLine_split[1]
	color = configLine_split[2]
	splitContent.pop(0)
	# Get texture
	texture = splitContent
	# Return config and texture
	return int(posX), int(posY), list(texture), str(color)


# Function to get a hexcode from a palette
def drawlib_asset_palette(): return {
    "white": "#ffffff",
    "black": "#000000",
    "red": "#ff0000",
    "green": "#00ff00",
    "blue": "#0000ff",
    "yellow": "#ffff00",
    "magenta": "#ff00ff",
    "cyan": "#00ffff",
    "gray": "#666666",
    "light_gray": "#999999",
    "light_red": "#ff6666",
    "light_green": "#66ff66",
    "light_yellow": "#ffff66",
    "light_blue": "#6666ff",
    "light_magenta": "#ff66ff",
    "light_cyan": "#66ffff",
    "brown": "#a52a2a",
    "orange": "#ffa500"
}

# Get ANSI code from palette
def getANSI (name):
	# Get hex value
	hex = drawlib_asset_palette()[name]
	hex = hex.replace("#",'')
	# Get RGB value
	lv = len(hex)
	rgb = tuple(int(hex[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
	rgbstr = str(rgb)
	rgbstr = rgbstr.replace(' ','')
	rgbstr = rgbstr.replace('(','')
	rgbstr = rgbstr.replace(')','')
	rgbdta = rgbstr.split(',')
	# Create ansi code string
	background=False
	ansi = '{};2;{};{};{}'.format(48 if background else 38, rgbdta[0], rgbdta[1], rgbdta[2])
	# Return ansi code string
	return ansi


# Render asset using pos, texture and color
def render_asset(posX,posY,texture,color,offsetX,offsetY):
    colorcode = getANSI(color)
    drawlib_internal_printmemsprite(texture,posX,posY,colorcode,offsetX,offsetY)