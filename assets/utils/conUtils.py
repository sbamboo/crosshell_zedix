# Utility module by Simon Kalmi Claesson
# OBS! xterm needed on linux

# [Imports]
import os
import platform
import time
import sys

# Set console size
def setConSize(width,height):
    # Get platform
    platformv = platform.system()
    # Linux using resize
    if platformv == "Linux":
        #return "\033[31mError: Platform Linux not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    # Darwin using resize
    elif platformv == "Darwin":
        #return "\033[31mError: Platform Darwin not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    # mode for windows
    elif platformv == "Windows":
        #return "\033[31mError: Platform Windows not supported yet!\033[0m"
        os.system(f'mode con: cols={width} lines={height}') # Apply console size with windows.cmd.mode
    # Error message if platform isn't supported
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"

# Set console title
def setConTitle(title):
    # Get platform
    platformv = platform.system()
    # Linux using ANSI codes
    if platformv == "Linux":
        sys.stdout.write(f"\x1b]2;{title}\x07")
    # Mac not supported
    elif platformv == "Darwin":
        return "\033[31mError: Platform Darwin not supported yet!\033[0m"
    # Windows using the title command
    elif platformv == "Windows":
        #return "\033[31mError: Platform Windows not supported yet!\033[0m"
        os.system(f'title {title}') # Apply console size with windows.cmd.title
    # Error message if platform isn't supported
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"

# Clear the screen
def clear(supress=False):
    # If suppress eq True
    if supress == True:
        return ""
    # Get platform
    platformv = platform.system()
    # Linux using clear
    if platformv == "Linux":
        os.system("clear")
    # Mac using clear
    elif platformv == "Darwin":
        os.system(f"clear")
    # Windows using cls
    elif platformv == "Windows":
        os.system("CLS") # Apply console size with windows.cmd.cls
    # Error message if platform isn't supported
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"

# Pause
def pause():
    # Get platform
    platformv = platform.system()
    # Linux using resize
    if platformv == "Linux":
        os.system(f"read -p ''")
    # Mac using resize
    elif platformv == "Darwin":
        return "\033[31mError: Platform Darwin not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    # Windows using PAUSE
    elif platformv == "Windows":
        #return "\033[31mError: Platform Windows not supported yet!\033[0m"
            os.system("PAUSE > nul") # Apply console size with windows.cmd.cls
    # Error message if platform isn't supported
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"

# Debug boo function
def boo():
    print("Boo! Oh now you are scared :)")

# Dummy function (call a dummy dummy to protect my yumme yummy tummy tummy)
def dummy():
    pass

# Os checker functions
def IsWindows():
    # Get platform and return boolean value depending of platform
    platformv = platform.system()
    if platformv == "Linux":
        return False
    elif platformv == "Darwin":
        return False
    elif platformv == "Windows":
        return True
    else:
        return False
def IsLinux():
    # Get platform and return boolean value depending of platform
    platformv = platform.system()
    if platformv == "Linux":
        return True
    elif platformv == "Darwin":
        return False
    elif platformv == "Windows":
        return False
    else:
        return False
def IsMacOS():
    # Get platform and return boolean value depending of platform
    platformv = platform.system()
    if platformv == "Linux":
        return False
    elif platformv == "Darwin":
        return True
    elif platformv == "Windows":
        return False
    else:
        return False