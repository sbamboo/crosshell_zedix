# Simple sprite renderer by Simon Kalmi Claesson made for Drawlib
# This function can be imported using 'from SimpleSpriteRenderer import *'

# Imports used in the functions below
import os

# Function to render sprites, taking a multitude of keyword arguments (arguments with specific order and name)
# TextureFile can only be given a string and must be the first argument. It must be a string since it says '=str()'.
# ScreenCordX is the screen X cordinate, to render the top right corner of the sprite at. It is the width value and is an integer. Screen cordinates are often described with the Y value first so if you use them that way please switch them.
# ScreenCordY is the screen Y cordinate, to render the top right corner of the sprite at. It is the height value and is also an integer.
# Color is an optional argument it dosen't have to be used. But if you do please supply the ANSI color code (ONLY THE CODE) to use (this applies to the whole sprite). If it isn't specified the script won't apply any formatting
def rend(TextureFile=str(),ScreenCordX=int(),ScreenCordY=int(),Color=None):
    # Define the colorcode 
    colorcode = 0 # Default colorcode
    # If Color is defined set colorcode to it.
    if Color != "" and Color != None:
        colorcode = Color
    # Get the texture from the texture file path (if it exists)
    if os.path.exists(TextureFile):
        # Get the raw text content from the file.
        rawContent = open(TextureFile, 'r').read()
    # Split the rawContent into lines of text
    spriteLines = rawContent.split('\n')
    # Render the texture at the correct position
    print("\033[s") # Save the current cursor position using ANSI
    c = 0 # Set out counter to 0
    Original_ScreenCordY = int(ScreenCordY) # Save the original Y cordinate
    for line in spriteLines: # Iterate through the lines
        ScreenCordY = Original_ScreenCordY + c # Increment the Y cordinate
        ANSIprefix = "\033[" + str(ScreenCordY) + ";" + str(ScreenCordX) + "H" + "\033[" + str(colorcode) + "m" # Create the ansi formatted string to render the line
        line = line.replace("\\033","\033") # Fix in texture formatting
        line = line.replace("\033[0m",f"\033[{colorcode}m") # Fix 0m resetting things
        print(ANSIprefix, str(line), "\033[0m") # Print the line
        c += 1 # Increment the counter
    print("\033[u\033[2A") # Load cursor position
