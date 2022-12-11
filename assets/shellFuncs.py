# Functions for crosshell (Zedix Core)
# Author: Simon Kalmi Claesson

from assets.utils.conUtils import *
from assets.coreFuncs import *

def cs_builtins(inputs=str(),allowedFileTypes=list()):
    # Exit
    if inputs == "exit":
        exit()
    # Cls
    elif inputs == "cls":
        clear()
    else:
        return "\033[33mInfo: Not Built in\033[0m"
    return "True"

def cs_writeHead():
    print("\033[32mWelcome to crosshell (Zedix core)\033[0m")

def saveTitle(title=str(),filepath=str()):
    cs_persistance("set","cs_title",filepath,title)
    setConTitle(title)