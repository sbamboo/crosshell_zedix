# Utility module by Simon Kalmi Claesson
# OBS! xterm needed on linux

import os
import platform
import time
import sys

# Set console size
def setConSize(width,height):
    platformv = platform.system()
    if platformv == "Linux":
        #return "\033[31mError: Platform Linux not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    elif platformv == "Darwin":
        #return "\033[31mError: Platform Darwin not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    elif platformv == "Windows":
        #return "\033[31mError: Platform Windows not supported yet!\033[0m"
        os.system(f'mode con: cols={width} lines={height}') # Apply console size with windows.cmd.mode
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"

# Set console title
def setConTitle(title):
    platformv = platform.system()
    if platformv == "Linux":
        sys.stdout.write(f"\x1b]2;{title}\x07")
    elif platformv == "Darwin":
        return "\033[31mError: Platform Darwin not supported yet!\033[0m"
    elif platformv == "Windows":
        #return "\033[31mError: Platform Windows not supported yet!\033[0m"
        os.system(f'title {title}') # Apply console size with windows.cmd.title
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"

# Clear the screen
def clear(supress=False):
    if supress == True:
        return ""
    platformv = platform.system()
    if platformv == "Linux":
        os.system("clear")
    elif platformv == "Darwin":
        os.system(f"clear")
    elif platformv == "Windows":
        os.system("CLS") # Apply console size with windows.cmd.cls
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"

# Pause
def pause():
    platformv = platform.system()
    if platformv == "Linux":
        return "\033[31mError: Platform Linux not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    elif platformv == "Darwin":
        return "\033[31mError: Platform Darwin not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    elif platformv == "Windows":
        #return "\033[31mError: Platform Windows not supported yet!\033[0m"
            os.system("PAUSE > nul") # Apply console size with windows.cmd.cls
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"

# Debug boo function
def boo():
    print("Boo has run!")

