# region: Imports
import os
try:
    import pynput
except:
    os.system("python3 -m pip install pynput")
    import pynput
from assets.lib.drawlib.base import *
# endregion

# Declare globals
screenBuffer = []
lineBuffer = ""
line = 1

# Get the terminal size
columns, rows = os.get_terminal_size()

# Declare on press
def on_press(key):
    global lineBuffer
    global line
    # Declare exit statement
    if key == pynput.keyboard.KeyCode.from_char('\x03'):
        listener.stop()
        return False
    # Fix space
    if key == pynput.keyboard.Key.space: key = " "
    # Handle backspace
    if key == pynput.keyboard.Key.backspace:
        lineBuffer = lineBuffer[:-1]
    # Handle enter
    elif key == pynput.keyboard.Key.enter:
        line += 1
        screenBuffer.append(lineBuffer)
        lineBuffer = ""
    # Handle going up a line
    elif (key == pynput.keyboard.Key.backspace and lineBuffer == "") or key == pynput.keyboard.Key.up:
        if key == pynput.keyboard.Key.backspace and linebuffer == "":
    # Otherwise
    else:
        lineBuffer += str(key).strip("'")
    if "ctrl" not in str(key):
        print("\033[{};{}H{}".format(line+1, 1, " "*columns))
        print("\033[{};{}H{}".format(line+1, 1, lineBuffer))
    
# Deca
def on_release(key): pass
listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)

# Clear screen & print header
clear()
draw_point("\033[107m\033[30mSimple writer program: Write bellow :)\033[0m",1,1)
print()
# Start listener
listener.start()
listener.join()