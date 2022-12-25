# [Imports]
import os
import math

# [Functions]
# Fill Screen
def fill_terminal(char):
  # Get the terminal size
  columns, rows = os.get_terminal_size()

  # Print the character repeatedly to fill the terminal
  print(char * columns)
  for i in range(rows - 1):
    print(char * columns)



# Draw a point of cords
def draw_point(char, x, y):
  if x != None and y != None and char != None:
    # Save the current position of the write head
    print("\033[s", end="")

    # Move the write head to the specified coordinates
    print("\033[{};{}H{}".format(y, x, char), end="")

    # Return the write head to the original position
    print("\033[u", end="")




# Draw a line
def draw_line(char, start_x, start_y, end_x, end_y):
  # Save the current position of the write head
  print('\033[s', end='')

  # Calculate the distance between the two points
  x_distance = end_x - start_x
  y_distance = end_y - start_y

  # Determine the slope of the line
  if x_distance == 0:
    slope = float('inf')
  else:
    slope = y_distance / x_distance

  # Iterate over the points on the line
  if abs(slope) <= 1:
    # Iterate over the x-values of the line
    for x in range(int(start_x), int(end_x) + 1):
      # Calculate the y-value of the line at this x-value
      y = start_y + slope * (x - start_x)

      # Round the y-value to the nearest integer
      y = int(round(y))

      # Move the write head to the x, y position
      print('\033[{};{}H'.format(y + 1, x + 1), end='')

      # Print the character at the x, y position
      print(char, end='')
  else:
    # Iterate over the y-values of the line
    for y in range(int(start_x), int(end_x) + 1):
      # Calculate the x-value of the line at this y-value
      x = start_x + (y - start_y) / slope

      # Round the x-value to the nearest integer
      x = int(round(x))

      # Move the write head to the x, y position
      print('\033[{};{}H'.format(y + 1, x + 1), end='')

      # Print the character at the x, y position
      print(char, end='')

  # Return the write head to its original position
  print('\033[u', end='')


# Draw a triangle
def draw_triangle(char, x1, y1, x2, y2, x3, y3):
  p1 = [x1,y1]
  p2 = [x2,y2]
  p3 = [x3,y3]
  draw_line(char,*p1,*p2)
  draw_line(char,*p1,*p3)
  draw_line(char,*p2,*p3)