from assets.lib.drawlib import *
fill_terminal(" ")



import random

import math

def lerp(a, b, t):
  return (1 - t) * a + t * b

def draw_curve(x1, y1, x2, y2, r):
  # Determine the length of the curve
  curve_length = int(math.sqrt((x1 - x2)**2 + (y1 - y2)**2))

  # Determine the maximum x coordinate
  max_x = max(x1, x2)

  # Iterate over each point on the curve and draw the ASCII character
  for i in range(curve_length):
    # Use the parametric equations for a circle to determine the y coordinate
    y = r * math.sin(2 * math.pi * i / curve_length)

    # Use linear interpolation to determine the x coordinate
    x = int(lerp(x1, x2, i / curve_length))

    # Write the spaces and the character
    print(" " * (max_x - x) + "*")

# Test the draw_curve function
draw_curve(0, 0, 20, 20, 10)



