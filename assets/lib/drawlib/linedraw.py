# Drawlib is a simple pixelart drawing library for python.
# And is made by Simon Kalmi Claesson, mostly to be used with/in Crosshell.
# Version 1.0
#
# You are not allowed to use this library unless through Crosshell or with personal permission from me.
#


# [Imports]
import os
from .tools import *
from .pointGroupAlgorithms import *
from .SimpleSpriteRenderer import rend

# Fill Screen
def fill_terminal(char):
  # Get the terminal size
  columns, rows = os.get_terminal_size()
  # Print the character repeatedly to fill the terminal
  print(char * columns)
  for i in range(rows - 1):
    print(char * columns)


# Draw a point of cords
def draw_point(char, x, y, ansi=None):
  if x != None and y != None and char != None:
    # Save the current position of the write head
    print("\033[s", end="")
    # Move the write head to the specified coordinates
    string = ""
    if ansi != None: string = ansi
    string += "\033[{};{}H{}".format(y, x, char)
    if ansi != None: string += "\033[0m"
    print(string, end="")
    # Return the write head to the original position
    print("\033[u", end="")


# Draw a line
def draw_line(char=str,x1=int,y1=int,x2=int,y2=int,ansi=None):
    # CapValues
    capIntsX([x1,x2])
    capIntsY([y1,y2])
    # Calculate Coordinates
    coordinates = beethams_line_algorithm(x1,y1,x2,y2)
    # Draw coordinates
    for coords in coordinates:
        x = coords[0]
        y = coords[1]
        draw_point(char,x,y,ansi=ansi)


# Draw a triangle
def draw_triangle_sides(char, s1, s2, s3, ansi=None):
  # side 1
  draw_line(char,*s1[0],*s1[1],ansi=ansi)
  # side 2
  draw_line(char,*s2[0],*s2[1],ansi=ansi)
  # side 3
  draw_line(char,*s3[0],*s3[1],ansi=ansi)

def draw_triangle_points(char, p1, p2, p3, ansi=None):
  draw_line(char,*p1,*p2,ansi=ansi)
  draw_line(char,*p1,*p3,ansi=ansi)
  draw_line(char,*p2,*p3,ansi=ansi)

def draw_triangle_coords(char, x1, y1, x2, y2, x3, y3, ansi=None):
  p1 = [x1,y1]
  p2 = [x2,y2]
  p3 = [x3,y3]
  draw_line(char,*p1,*p2,ansi=ansi)
  draw_line(char,*p1,*p3,ansi=ansi)
  draw_line(char,*p2,*p3,ansi=ansi)

def draw_circle(char=str,xM=int,yM=int,r=int,ansi=None):
  rigX = xM+r
  lefX = xM-r
  topY = yM+r
  botY = yM-r
  diam = (r*2)+1
  # CapValues
  capIntsX([xM,rigX,lefX])
  capIntsY([yM,topY,botY])
  # Calculate Coordinates
  coordinates = beethams_circle_algorithm(xM,yM,r)
  # Draw coordinates
  for coords in coordinates:
      x = coords[0]
      y = coords[1]
      draw_point(char,x,y,ansi=ansi)

def draw_ellipse(char=str,cX=int,cY=int,xRad=int,yRad=int,ansi=None):
  rigX = cX+xRad
  lefX = cX-xRad
  topY = cY+yRad
  botY = cY-yRad
  # CapValues
  capIntsX([cX,rigX,lefX])
  capIntsY([cY,topY,botY])
  # Calculate Coordinates
  coordinates = beethams_ellipse_algorithm(cX,cY,xRad,yRad)
  # Draw coordinates
  for coords in coordinates:
      x = coords[0]
      y = coords[1]
      draw_point(char,x,y,ansi=ansi)

def draw_quadBezier(char,sX=int,sY=int,cX=int,cY=int,eX=int,eY=int,ansi=None):
  # CapValues
  capIntsX([sX,cX,eX])
  capIntsY([sY,cY,eY])
  # Calculate Coordinates
  coordinates = generate_quadratic_bezier(sX,sY,cX,cY,eX,eY)
  # Draw coordinates
  for coords in coordinates:
      x = coords[0]
      y = coords[1]
      draw_point(char,x,y,ansi=ansi)

def draw_cubicBezier(char,sX=int,sY=int,c1X=int,c1Y=int,c2X=int,c2Y=int,eX=int,eY=int, algorithm="step",modifier=None,ansi=None):
  '''
  Alogrithm: "step" or "point"
  Modifier: With step algorithm, def: 0.01; With point algorithm, def: 100
  '''
  # CapValues
  capIntsX([sX,c1X,c2X,eX])
  capIntsY([sY,c1Y,c2Y,eY])
  # Calculate Coordinates
  coordinates = generate_cubic_bezier(sX, sY, c1X, c1Y, c2X, c2Y, eX, eY, algorithm,modifier)
  # Draw coordinates
  for coords in coordinates:
      x = coords[0]
      y = coords[1]
      draw_point(char,x,y,ansi=ansi)


# Function to use drawlibs SimpleSpriteRenderer
def draw_sprite(TextureFile=str(),ScreenCordX=int(),ScreenCordY=int(),Color=None):
    rend(TextureFile=str(),ScreenCordX=int(),ScreenCordY=int(),Color=None)