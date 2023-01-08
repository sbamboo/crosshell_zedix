# Import libaries
try:
    import pyautogui
except:
    os.system("py -m pip install pyautogui")
    import pyautogui
try:
    from screeninfo import get_monitors
except:
    os.system("py -m pip install screeninfo")
    from screeninfo import get_monitors

# Get resulotion
for m in get_monitors():
    # Currently force use of primary monitor
    if m.is_primary == True:
        hres, vres = m.width, m.height
    # Fall back to 1920x1080
    else:
        hres, vres = 1920, 1080


# Get mouse position (In screen cords)
x, y = pyautogui.position()

# Get Console size
colums, lines = os.get_terminal_size()

# Calculate how many pixels (mouse positions) there is per console cell
points_in_colum = hres/colums
points_in_line = vres/lines

# Calculate the cordinates and round in case
xcord = round( x/points_in_colum )
ycord = round( y/points_in_line )

# Print out the result
print(xcord,ycord)