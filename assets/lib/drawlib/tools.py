# [Imports]
import shutil

# [Tools]
# Caps an int to the terminal size for X (for coordinates)
def capIntsX(values=list):
    sc_width, _ = shutil.get_terminal_size()
    for value in values:
        if type(value) == int:
            if value > sc_width or value < 0:
                raise ValueError("X cappedInt's value must be inside terminalResolution")
# Caps an int to the terminal size for Y (for coordinates)
def capIntsY(values=list):
    _, sc_height = shutil.get_terminal_size()
    for value in values:
        if type(value) == int:
            if value > sc_height or value < 0:
                raise ValueError("Y cappedInt's value must be inside terminalResolution")

# To fix an issue since the drawlib rectangle needs the points in order of TL,TR,BR,BL and this function organies them in that order
def arrange_coordinates_to_rectangle(x1, y1, x2, y2, x3, y3, x4, y4):
    # Find the center point
    center_x = (x1 + x2 + x3 + x4) / 4
    center_y = (y1 + y2 + y3 + y4) / 4
    # Calculate the distances from the center to each point
    distances = [(x - center_x)**2 + (y - center_y)**2 for x, y in [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]]
    # Sort the points based on their distances from the center
    sorted_indices = sorted(range(4), key=lambda i: distances[i])
    # Arrange the points to form a rectangle
    p1 = (x1, y1)
    p2 = (x2, y2)
    p3 = (x3, y3)
    p4 = (x4, y4)
    sorted_points = [p1, p2, p3, p4]
    arranged_points = [sorted_points[i] for i in sorted_indices]
    _x1, _y1 = arranged_points[0][0],arranged_points[0][1]
    _x2, _y2 = arranged_points[1][0],arranged_points[1][1]
    _x3, _y3 = arranged_points[2][0],arranged_points[3][1]
    _x4, _y4 = arranged_points[3][0],arranged_points[3][1]
    return _x1,_y1,_x2,_y2,_x3,_y3,_x4,_y4