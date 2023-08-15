import math

def drawlib_internal_printmemsprite(texture,posX,posY,colorcode,offsetX=None,offsetY=None):
  if offsetX != None: posX = posX + offsetX
  if offsetY != None: posY = posY + offsetY
  print("\033[s") # Save cursorPos
  c = 0
  OposY = int(posY)
  for line in texture:
    posY = OposY + c
    ANSIprefix = "\033[" + str(posY) + ";" + str(posX) + "H" + "\033[" + str(colorcode) + "m"
    print(ANSIprefix, str(line), "\033[0m")
    c += 1
  print("\033[u\033[2A") # Load cursorPos


# Internal function to generate a texture of a curve, taking center points, radius and character.
def drawlib_internal_draw_curve(center=tuple(), radius=int(), char=str()):
    # Initialize an empty list to store the curve
    rows = []
    # Create a list with the same number of rows and columns as the size of the curve (Nested lists for al cells)
    for _ in range(2*(center[1] + radius) + 1):
        rows.append([" " for _ in range(2*(center[0] + radius) + 1)])
    # Iterate over all angles between 0 and 90 degrees (to only get one quadrant)
    for angle in range(0, 90):
        # Calculate the x and y coordinates of the point on the curve for the current angle
        x = center[0] + int(radius * math.cos(math.radians(angle))) * 2
        y = center[1] + int(radius * math.sin(math.radians(angle)))
        # Set the character of the point at the calculated coordinates
        rows[y][x] = char
    # Join each row of the list into a single string and return it
    return "\n".join("".join(row) for row in rows)


def draw_fillcircle(char,posX,posY,diameter):
  colorcode = "33"
  # Generate a memSprite
  radius = diameter / 2 - .5
  r = (radius + .25)**2 + 1
  memsprite = ""
  for i in range(diameter):
    y = (i - radius)**2
    for j in range(diameter):
      x = (j - radius)**2
      if x + y <= r:
        memsprite = memsprite + f'{char}{char}'
      else:
        memsprite = memsprite + '  '
    memsprite = memsprite + '\n'
  # Print memsprite
  drawlib_internal_printmemsprite( memsprite.split('\n'),posX,posY,colorcode )

# Function that draws a curve at the given cordinates (top-right) taking radius char.
def draw_curve(cordinates=tuple(), radius=int(), char=str(), quadrant=int()):
    flipped_texture = []
    curve_texture = ( drawlib_internal_draw_curve((0,0), radius, char) ).split("\n")
    if quadrant == 1 or quadrant == 4:
        flipped_texture = reversed(curve_texture)
    else:
        flipped_texture = curve_texture
    if quadrant == 4 or quadrant == 3:
        curve_texture = flipped_texture
        flipped_texture = []
        for line in curve_texture:
            line = ''.join(reversed(list(str(line))))
            flipped_texture.append(line)
    flipped_texture = [s for s in flipped_texture if s.strip()]
    drawlib_internal_printmemsprite(flipped_texture,cordinates[0],cordinates[1],"0")
