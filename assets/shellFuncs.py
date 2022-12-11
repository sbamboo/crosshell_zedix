# Functions for crosshell (Zedix Core)
# Author: Simon Kalmi Claesson

from assets.utils.conUtils import *
from assets.coreFuncs import *
import os

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

def cs_writeProfile(basedir,globalInput):
    msgProfileFile = os.path.realpath(f"{basedir}{os.sep}assets{os.sep}profile.msg")
    pyProfileFile = os.path.realpath(f"{basedir}{os.sep}assets{os.sep}profile.py")
    if os.path.exists(pyProfileFile):
        exec(open(pyProfileFile).read(), globalInput)
    elif os.path.exists(msgProfileFile):
        content = open(msgProfileFile,"r").read()
        if content != "":
            for line in content.split("\n"):
                eval(f"print('{line}')")
    else:
        print("\033[33mOBS! No profile file, please add: '/assets/profile.msg'\033[0m")

def cs_writeHead(versionData=dict(),basedir=str(),globalInput=dict()):
    hasMoreLines = False
    # Channel Messages
    channel = versionData["channel"]
    if channel != "Release" and channel != "Stable":
        hasMoreLines = True
    if channel == "Development":
        print("\033[31mYou are running a development version of crosshell, bugs may occure and some features migth be missing.\033[0m")
    elif channel == "Alpha":
        print("\033[33mYou are running a alpha version of crosshell, bugs may occure and some features migth be missing.\033[0m")
    elif channel == "Beta":
        print("\033[33mYou are running a beta version of crosshell, although these are stabler then alpha versions buggs may still occure.\033[0m")
    elif channel == "Viva":
        print("\033[33mYou are running the current version of Crosshell-VIVA, these are generally stable but may contain bugs.\033[0m")
    else:
        print("\033[31mThe version channel of your crosshell installation is not reconized, this may be a bug\033[0m")
    # More lines line
    if hasMoreLines == True: print("")
    # Profile
    cs_writeProfile(basedir,globalInput)
    # Welcome
    hasShownGuideStateFile = os.path.realpath(f"{basedir}{os.sep}assets{os.sep}hasshownguide.empty")
    if os.path.exists(hasShownGuideStateFile):
        print("\033[32mWelcome, write 'help' for help. To add messages to here edit: /assets/profile.ps1\033[0m")
    else:
        print("\033[32mWelcome, for a guide on how to use crosshell write 'guide' or for command help write 'help'.\033[0m") 

def saveTitle(title=str(),filepath=str()):
    cs_persistance("set","cs_title",filepath,title)
    setConTitle(title)