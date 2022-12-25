from assets.lib.drawlib import *
fill_terminal(" ")



import random

def ascii_curve(x1, y1, x2, y2):
  # Calculate the slope of the line connecting the two points
  m = (y2 - y1) / (x2 - x1)

  # Iterate over the x values between x1 and x2
  for x in range(x1, x2 + 1):
    # Calculate the y value for the current x value using the slope
    y = m * (x - x1) + y1

    # Increment the y value by 2 towards the middle of the curve
    if x < (x1 + x2) / 2:
      y += 2
    elif x > (x1 + x2) / 2:
      y -= 2

    # Print the appropriate number of spaces and hashes to draw the curve
    # If x is at the edges, increment y by 0 to keep the curve circular
    if x == x1 or x == x2:
      print(' ' * int(y) + '#')
    else:
      print(' ' * int(y) + '##')

# Example usage
ascii_curve(0, 0, 20, 20)


