# Crosshell verification tool (service)
# Author: Simon Kalmi Claeson
version = 1.0
#


# [Imports]
import os
import socket
from assets.lib.drawlib.internal import drawlib_internal_printmemsprite
from assets.lib.drawlib.linedraw import draw_point
from assets.lib.conUtils import *

# [Prepare]
HelpText = [
            "This information is collected to allow the author -",
            " to have a list of people using the app,",
            "this is only needed since the app is in development -",
            " and will be removed later.",
            "To opt out simply don't write your name and press enter.",
            "Although it is appriciated if you opt in.",
            "Note! Only name and computer-name is send,",
            "and no other data will ever be collected,",
            "as a part of this tool.",
            "Note! If other data at some point is collected -",
            " it's sepparate, and will be informed about!",
            "THIRD PARTY COLLECTION IS NOT HANDLED BY THIS -",
            " TOOL AND DOSEN'T HAVE TO COMPLY WITH ABOVE!!"
            ]

def inputAtCords (posX, posY, text=None, color=None):
    # Save cursorPos
    print("\033[s")
    # Set ansi prefix
    ANSIprefix = "\033[" + str(posY) + ";" + str(posX) + "H" + "\033[" + str(color) + "m"
    inp = input(str(ANSIprefix + str(text)))
    print("\033[0m")
	# Load cursorPos
    print("\033[u\033[2A")
    return inp

def draw_background():
    draw_point("\033[31m", 0, 0)
    char = "█"
    for i in range(rows-1):
        print(char * columns)
    draw_point("\033[0m", 0, 0)
    print("\033[{};{}H{}".format(rows, 0, f"\033[33mCrosshell verification tool! Version: {version}\033[0m"), end="")


# [Collect stuff]
columns, rows = os.get_terminal_size()
computer = socket.gethostname()

# [Drawing]
middleX = (columns//2)-1
middleY = (rows//2)-1
draw_background()
print("\033[4;38H\033[41;97mWho is going to be using this install?")
print("\033[5;38H\033[41;97m▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔")
print(f"\033[6;38H\033[101;97mComputer: {computer}")
drawlib_internal_printmemsprite(HelpText,37,13,colorcode="41;91")
name = inputAtCords(38, 7, text="User of this install: ", color="101;97")


clear()
print(name)